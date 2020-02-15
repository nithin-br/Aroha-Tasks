import os
import pymysql
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Numeric, CHAR, VARCHAR

host = os.environ.get('db_local_host')
user = os.environ.get('db_local_user')
password = os.environ.get('db_local_pwd')
database = 'test0'

engine = create_engine("mysql+pymysql://{user}:{pw}@{host}/{db}"
                       .format(host=host, user=user, pw=password, db=database))

Base = declarative_base()


class Date_Dim(Base):

    __tablename__ = 'DATE_DIM'
    DATEKEY = Column(Integer, primary_key=True)
    THEDATE = Column(DateTime)
    YEAR = Column(Numeric)
    MONTH = Column(Numeric)
    YEARMONTH = Column(CHAR(7))
    MONTHNAME = Column(VARCHAR(9))
    MONTHABBR = Column(VARCHAR(3))
    DAY = Column(Numeric)
    DAYOFWEEK = Column(Numeric)
    DAYOFWEEKNAME = Column(VARCHAR(9))
    DAYOFWEEKABBR = Column(VARCHAR(3))
    QUARTER = Column(Numeric)
    SEASON = Column(VARCHAR(6))
    HOLIDAY = Column(VARCHAR(30))
    CURRENTYEAR = Column(CHAR(1))
    PRIORYEAR = Column(CHAR(1))
    CURRENTMONTH = Column(CHAR(1))
    PRIORMONTH = Column(CHAR(1))
    FIRSTOFMONTH = Column(CHAR(1))
    BUSINESSDAY = Column(CHAR(1))
    FISCALMONTH = Column(VARCHAR(20))
    ELIGILITYDATE = Column(DateTime)


# creating table
Date_Dim.__table__.create(engine)
