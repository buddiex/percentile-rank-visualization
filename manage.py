from functools import wraps
from app import create_app
import click
import pandas as pd
from sqlalchemy import create_engine # database connection

app = create_app()
cnx = create_engine(app.config['SQLALCHEMY_DATABASE_URI']).connect()


@click.group()
def main():
    """Flask Simple Login Example App"""

@main.command()
# @click.option('--reloader/--no-reloader', default=None)
def create_db():
    print('populating Counties Table')
    df_count = pd.read_excel("counties.xlsx")
    df_count['FIPS_County'] = df_count['FIPS_County'].apply(lambda x: '{0:0>3}'.format(x))
    df_count['FIPS'] = df_count['FIPS_State'].map(str)+df_count['FIPS_County'].map(str)
    print(app.config['SQLALCHEMY_DATABASE_URI'])
    df_count.to_sql('county', cnx, if_exists='append', index=False)

@main.command()
@click.option('--reloader/--no-reloader', default=None)
@click.option('--debug/--no-debug', default=None)
@click.option('--host', default=None)
@click.option('--port', default=None)
def runserver(app=app, reloader=None, debug=None, host=None, port=None):
    """Run the Flask development server i.e. app.run()"""
    debug = debug or app.config.get('DEBUG', False)
    reloader = reloader or app.config.get('RELOADER', False)
    host = host or app.config.get('HOST', '127.0.0.1')
    port = port or app.config.get('PORT', 5000)
    app.run(
        use_reloader=reloader,
        debug=debug,
        host=host,
        port=port
    )


if __name__ == "__main__":
    main()
