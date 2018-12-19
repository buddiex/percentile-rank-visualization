import os
from os.path import join, dirname


os.environ['PYTHONIOENCODING'] = 'UTF-8'
basedir = dirname(__file__)

OUT_FOLDER = join(basedir, 'data')
DATA_FOLDER = join(basedir, 'data')
LOG_FILE = join(basedir, 'app.log')

SECRET_KEY = '123456790'

# Create in-memory database
SQLALCHEMY_ECHO = True

DB_NAME = "StatSys"
SQLALCHEMY_DATABASE_URI = "sqlite:///sample_db.sqlite"

# SQLALCHEMY_DATABASE_URI = """oracle+cx_oracle://system:oracle@(DESCRIPTION = (LOAD_BALANCE=on) (FAILOVER=ON) (ADDRESS = (PROTOCOL = TCP)
#                      (HOST = localhost)(PORT = 1520))(CONNECT_DATA = (SERVER = DEDICATED) (SID=xe)))"""

TWITTER_HANDLE = 'gtbank'

DEFAULT_KPI = 'obessity'