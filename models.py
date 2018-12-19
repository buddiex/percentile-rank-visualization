# coding: utf-8
from sqlalchemy import BigInteger, Column, ForeignKey, Integer, String, Table, Text
from sqlalchemy.orm import relationship
from database import Base

metadata = Base.metadata


class County(Base):
    __tablename__ = 'county'

    id = Column(Integer, primary_key=True)
    state = Column(String)
    County_name = Column(String)
    FIPS_County = Column(String)
    FIPS = Column(String)
    FIPS_State = Column(String)


class File(Base):
    __tablename__ = 'file'

    id = Column(Integer, primary_key=True)
    name = Column(String(64))
    path = Column(String(128))


class KpiTable(Base):
    __tablename__ = 'kpi_table'

    id = Column(Integer, primary_key=True)
    name = Column(String(64))
    description =Column(String(200))


class PercentileRank(Base):
    __tablename__ = 'percentile_rank'

    id = Column(Integer, primary_key=True)
    kpi_table_id = Column(ForeignKey('kpi_table.id'), index=True)
    county_id = Column(ForeignKey('county.id'), index=True)
    percentage = Column(Integer)
    percentile_rank = Column(Integer)
    year = Column(Integer)

    county = relationship('County')
    kpi_table = relationship('KpiTable')

class State(Base):
    __tablename__ = 'state'

    id = Column(Integer, primary_key=True)
    name = Column(String)


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    first_name = Column(String(100))
    last_name = Column(String(100))
    login = Column(String(80), unique=True)
    email = Column(String(120))
    password = Column(String(64))
