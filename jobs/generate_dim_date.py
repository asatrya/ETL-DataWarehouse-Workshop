import pandas as pd
import sqlalchemy as db
import configparser
import logging
from logging.config import fileConfig


# Configs
config = configparser.ConfigParser()
config.read('conf/.env')

fileConfig('conf/logging_config.ini')
logger = logging.getLogger()

# Database connection URI
db_engine = db.create_engine(
    "mysql+pymysql://{}:{}@{}:{}/{}".format(config['database']['user'],
                                            config['database']['password'],
                                            config['database']['host'],
                                            config['database']['port'],
                                            config['database']['db']))

# Data warehouse connection URI
dw_engine = db.create_engine(
    "mysql+pymysql://{}:{}@{}:{}/{}".format(config['data-warehouse']['user'],
                                            config['data-warehouse']['password'],
                                            config['data-warehouse']['host'],
                                            config['data-warehouse']['port'],
                                            config['data-warehouse']['db']))


def extract_latest_date(db_engine, table, field):
    """Get the latest date from a table"""

    query = "SELECT MAX({}) AS max_date FROM {}".format(field, table)
    result_df = pd.read_sql(query, db_engine)
    return result_df.loc[0, 'max_date']


def label_weekend(row):
    """Add label `1` for weekend or `0` for weekday"""

    if row['dayofweek'] == 5 or row['dayofweek'] == 6:
        return 1
    else:
        return 0


def create_date_table(start, end):
    """Generate date records for a range of date"""

    df = pd.DataFrame({"date": pd.date_range(start, end)})
    df["dayofweek"] = df.date.dt.dayofweek
    df["day"] = df.date.dt.day
    df["week"] = df.date.dt.weekofyear
    df["month"] = df.date.dt.month
    df["quarter"] = df.date.dt.quarter
    df["year"] = df.date.dt.year
    df["is_weekend"] = df.apply(lambda row: label_weekend(row), axis=1)
    df["is_holiday"] = df.apply(lambda row: label_weekend(row), axis=1)
    df["date_key"] = df.date.dt.strftime('%Y%m%d')
    return df[['date_key', 'day', 'date', 'year', 'quarter', 'month', 'week', 'is_weekend', 'is_holiday']]


# extract latest value from date dimension
dateDim_latest = extract_latest_date(dw_engine, 'dimDate', 'date')


# determine start range of generated date
if dateDim_latest == None:
    start_date_range = pd.datetime(2005, 1, 1).date()
else:
    start_date_range = dateDim_latest + pd.Timedelta(1, unit='D')
logger.debug('start_date_range={}'.format(start_date_range))

# determine end range of generated date
end_date_range = pd.datetime(2026, 1, 1).date()
logger.debug('end_date_range={}'.format(end_date_range))

# Check if date range is valid
if end_date_range >= start_date_range:
    # Generate date range
    date_range_df = create_date_table(start_date_range, end_date_range)
    logger.debug('date_range_df={}'.format(date_range_df))

    # Load to dimension table
    date_range_df.to_sql('dimDate', dw_engine, if_exists='append', index=False)
