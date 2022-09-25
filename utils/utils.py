import base64
import io
from datetime import datetime
import pandas as pd


def parse_contents(contents, filename):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    if 'csv' in filename:
        # Assume that the user uploaded a CSV file
        return pd.read_csv(
            io.StringIO(decoded.decode('utf-8')))
    elif 'xls' in filename:
        # Assume that the user uploaded an excel file
        return pd.read_excel(io.BytesIO(decoded))


def datetime_from_string(time):
    return datetime.strptime(time, '%H:%M')


def days_hours_minutes(td):
    return round(((td.days*24+td.seconds//3600)*60+(td.seconds//60)%60)/60,2)
