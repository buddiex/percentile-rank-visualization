import os
import datetime as dt
from datetime import date
from dateutil.rrule import rrule, YEARLY
from flask import Flask, url_for, redirect, flash, render_template, request, jsonify
import flask_admin as admin
from flask_admin import helpers, BaseView, expose
from flask_admin.contrib import sqla
import flask_login as login
from flask_wtf import form
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import fields, validators
from wtforms.validators import DataRequired
import flask_excel as excel
from werkzeug.security import generate_password_hash
from flask_sqlalchemy import SQLAlchemy
from bokeh.models import HoverTool, LabelSet, Label
from bokeh.plotting import figure, ColumnDataSource
from bokeh.embed import components
from utils import *
import pandas as pd


from models import *
from database import db_session, engine


# Create Flask application
def create_app():
    app = Flask(__name__)
    app.config.from_object('config')
    return app

app = create_app()
db = SQLAlchemy(app)


# Create user model.
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    login = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120))
    password = db.Column(db.String(64))

    # Flask-Login integration
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    # Required for administrative interface
    def __unicode__(self):
        return self.username


# Define login and registration forms (for flask-login)
class LoginForm(form.Form):
    login = fields.StringField(validators=[validators.required()])
    password = fields.PasswordField(validators=[validators.required()])

    def validate_login(self, field):
        user = self.get_user()

        if user is None:
            raise validators.ValidationError('Invalid user')

        if not check_password_hash(user.password, self.password.data):
            raise validators.ValidationError('Invalid password')

    def get_user(self):
        return db.session.query(User).filter_by(login=self.login.data).first()


class UploadStats(form.Form):
    kpi_name = fields.SelectField('Category', coerce=int)
    year = fields.SelectField('Select Year', choices=sorted([(yr.strftime("%Y"), yr.strftime("%Y"))
                                                             for yr in rrule(YEARLY, dtstart=date(2016, 1, 1), until=dt.datetime.now())],
                                                              reverse = True))
    file = FileField(validators=[
                    FileRequired(),
                    FileAllowed(['xls', 'xlsx'], 'Excel files only!')
                ])

    def validate_login(self, field):
        if db.session.query(User).filter_by(login=self.login.data).count() > 0:
            raise validators.ValidationError('Duplicate username')


class SearchForm(form.Form):
    county = fields.SelectField(coerce=int)
    # year = fields.SelectField('Select Year', choices=sorted([(yr.strftime("%Y"), yr.strftime("%Y"))
    #                                                          for yr in rrule(YEARLY, dtstart=date(2016, 1, 1), until=dt.datetime.now())],
    #                                                           reverse = True))
    year = fields.SelectField('Select Year', choices=sorted([(str(value[0]), value[0])
                                                              for value in db_session.query(PercentileRank.year).distinct()]
                                                             ))

# Create customized model view class
class MyModelView(sqla.ModelView):
    def is_accessible(self):
        return login.current_user.is_authenticated


class PercentileRankView(MyModelView):
    # column_select_related_list = (KpiTable.name, County.County_name)
    column_auto_select_related = True
    column_list = ('kpi_table.name','year', 'county.FIPS','county.County_name', 'county.state', 'percentage','percentile_rank')
    column_labels = {'percentage':'Percentage',
                     'county.FIPS': 'FIPS',
                     'county.County_name':'County',
                     'county.state':'Sate','kpi_table.name':'Health KPI'}
    column_searchable_list = ('county.state', 'county.County_name')
    can_create = False
    can_edit = False
    can_delete = False


class KPIVew(MyModelView):
    form_args = dict(
        name=dict(label='Name', validators=[DataRequired()])
    )


def init_login():
    login_manager = login.LoginManager()
    login_manager.init_app(app)

    # Create user loader function
    @login_manager.user_loader
    def load_user(user_id):
        return db.session.query(User).get(user_id)


def show_graph(kpi_id,  year, count_id=None):
    TOOLS = "save,hover"
    kpis = KpiTable.query.filter(KpiTable.id == kpi_id).one()
    stats_sql = """
                  select kp.name, cy.id, cy.county_name, cy.state, cy.county_name||' - '||cy.state display_county ,
                   prk.percentage, prk.percentile_rank from
                  percentile_rank prk, county cy, kpi_table kp
                  where prk.county_id = cy.id
                  and prk.kpi_table_id = kp.id
                  and prk.year = {}
                  and prk.kpi_table_id = {};
                """.format(year,kpis.id)
    df = pd.read_sql(stats_sql, engine.connect())
    df_ranked = df[['state', 'County_name', 'percentage', 'percentile_rank','display_county', 'id']].sort_values("percentile_rank")

    plot = figure(title="{} {} Percentile Rankings ".format(year, kpis.name).upper(), tools=TOOLS)
    source = ColumnDataSource(
        data=dict(
            x=df_ranked.percentile_rank,
            y=df_ranked.percentage,
            state=df_ranked.state,
            county=df_ranked.County_name,
            # position=df_ranked.index
        )
    )

    plot.line('x', 'y', source=source, name="all")

    if count_id:
        county_df = df_ranked[(df.id==count_id)]
        source = ColumnDataSource(
            data=dict(
                cx=county_df.percentile_rank,
                cy=county_df.percentage,
                cstate=county_df.state,
                # ccounty=county_df.display_county,
                ccounty=county_df.County_name,

            )
        )
        plot.circle('cx', 'cy', source=source, size=10)
        labels = LabelSet(x='cx', y='cy', text='ccounty', level='glyph',
                          _offset=5, y_offset=5, source=source, render_mode='canvas')
        text_in = """County:{}, Sate:{}, Percentage:{}, Rank:{}"""\
                    .format(county_df.County_name.values[0],
                            county_df.state.values[0],
                            round(county_df.percentage.values[0],2),
                            round(county_df.percentile_rank.values[0],2),

                            )
        citation = Label(x=40, y=70, x_units='screen', y_units='screen',
                     text=text_in, render_mode='canvas',
                     border_line_color='white', border_line_alpha=1.0,
                     background_fill_color='white', background_fill_alpha=1.0)
        plot.add_layout(citation)

        plot.add_layout(labels)



    hover = plot.select_one(HoverTool)
    hover.point_policy = "snap_to_data"
    hover.mode = 'hline'
    hover.names = ['all']
    hover.tooltips = [
        ("County", "@county"),
        ("State", "@state"),
        ("percentage", "@y"),
        ("percentile", "@x"),
        # ("position", "@position")
    ]

    return components(plot)


# Flask views
@app.route('/')
def index():
    return redirect(url_for('kpi_graph', kpi_id=1))


@app.route('/kpi_graph/<kpi_id>', methods=('GET', 'POST'))
def kpi_graph(kpi_id):
    search = SearchForm()
    search.county.choices = [(k.id, k.County_name+" "+k.state) for k in County.query.all()]
    if search.validate_on_submit():
        count_id = search.county.data
        year = search.year.data
        script, div = show_graph(kpi_id, year, count_id)
    else:
        year = sorted(db_session.query(PercentileRank.year.distinct()))[0][0]
        script, div = show_graph(kpi_id, year)

    distinct_kpi = [value[0] for value in db_session.query(PercentileRank.kpi_table_id).distinct()]
    kpis = db_session.query(KpiTable.id, KpiTable.name).filter(KpiTable.id.in_(distinct_kpi))

    return render_template("public_index.html", script=script, div=div,kpis=kpis, form=search, kpi_id=kpi_id)


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

# Admin views
# Create customized index view class that handles login & registration
class MyAdminIndexView(admin.AdminIndexView):

    @expose('/')
    def index(self):
        if not login.current_user.is_authenticated:
            return redirect(url_for('.login_view'))
        return super(MyAdminIndexView, self).index()

    @expose('/login/', methods=('GET', 'POST'))
    def login_view(self):
        # handle user login
        form = LoginForm(request.form)
        if helpers.validate_form_on_submit(form):
            user = form.get_user()
            login.login_user(user)

        if login.current_user.is_authenticated:
            return redirect(url_for('.index'))
        self._template_args['form'] = form
        return super(MyAdminIndexView, self).index()

    @expose('/logout/')
    def logout_view(self):
        login.logout_user()
        return redirect(url_for('.index'))


class UploadView(BaseView):
    @expose('/', methods=('GET', 'POST'))
    def index(self):
        kpi_upload_form = UploadStats()
        kpi_upload_form.kpi_name.choices = [(k.id, k.name) for k in KpiTable.query.all()]
        if kpi_upload_form.validate_on_submit():
            dat = json.loads(jsonify({"result": request.get_dict(field_name='file')}).data.decode('utf8'))
            df_stat = pd.DataFrame(dat['result'])
            df_stat.columns = [x.lower().strip() for x in df_stat.columns]
            df_stat.to_csv('csvout01.csv')
            df_stat = pd.read_csv("csvout01.csv")
            counties = County.query;
            df_counties = pd.read_sql(counties.statement, counties.session.bind)
            df_stat['county_id'] = pd.merge(df_stat, df_counties, left_on=['fips'], right_on=['FIPS'], how='left').id
            df_stat['Year'] = kpi_upload_form.year.data
            df_stat['kpi_table_id'] = kpi_upload_form.kpi_name.data
            df_stat['percentile_rank'] = df_stat.percentage.rank(pct=True)*100
            PercentileRank.query.filter(PercentileRank.year == kpi_upload_form.year.data,
                                        PercentileRank.kpi_table_id == kpi_upload_form.kpi_name.data).delete()
            df_stat[['county_id', 'Year', 'kpi_table_id','percentile_rank','percentage']]\
                .to_sql('percentile_rank', engine.connect(), if_exists='append', index=False)
            flash('Stats Saved!')
            return redirect(url_for('admin.index'))

        return self.render('upload_stats.html', form=kpi_upload_form)

    def is_accessible(self):
        return login.current_user.is_authenticated


init_login()
admin = admin.Admin(app, 'Statsys', index_view=MyAdminIndexView(), base_template='my_master.html')
admin.add_view(UploadView(name='Upload Stats', endpoint='upload_stats'))
admin.add_view(KPIVew(KpiTable, db.session, name='Manage KPI' ))
admin.add_view(PercentileRankView(PercentileRank, db.session))
admin.add_view(MyModelView(User, db.session, name='Manage Users'))


def build_sample_db():
    """
    Populate a small db with some example entries.
    """
    db.drop_all()
    db.create_all()
    test_user = User(login="test", password=generate_password_hash("test"))
    db.session.add(test_user)

    first_names = ['Admin', 'Amelia']
    last_names = ['Admin', 'Smith']

    for i in range(len(first_names)):
        user = User()
        user.first_name = first_names[i]
        user.last_name = last_names[i]
        user.login = user.first_name.lower()
        user.email = user.login + "@example.com"
        user.password = generate_password_hash("admin")
        db.session.add(user)
    return

if __name__ == '__main__':

    app_dir = os.path.realpath(os.path.dirname(__file__))
    database_path = os.path.join(app_dir, "sample_db.sqlite")
    # print(database_path)
    if not os.path.exists(database_path):
        build_sample_db()

    excel.init_excel(app)
    app.run(debug=True)