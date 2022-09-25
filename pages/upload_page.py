from layouts.upload_layout import *
from models.global_vars import GlobalVar
from models.date_preprocess import prepare_df
from utils.utils import parse_contents
import pandas as pd


@callback(
    Output("attendance_graph", "data"),
    Output("attendance_graph", "columns"),
    [Input("attendance_file", "filename"), Input("attendance_file", "contents")]
)
def attendance(filename, contents):
    if contents is None:
        return [{}], []
    GlobalVar.attendance_df = parse_contents(contents, filename)
    return GlobalVar.attendance_df.to_dict('records'), [{"name": i, "id": i} for i in GlobalVar.attendance_df.columns]


@callback(
    Output("employee_graph", "data"),
    Output("employee_graph", "columns"),
    [Input("shifts_file", "filename"), Input("shifts_file", "contents")]
)
def employee(filename, contents):
    if contents is None:
        return [{}], []
    GlobalVar.shifts_df = parse_contents(contents, filename)
    return GlobalVar.shifts_df.to_dict('records'), [{"name": i, "id": i} for i in GlobalVar.shifts_df.columns]


@callback(
    Output("salary_graph", "data"),
    Output("salary_graph", "columns"),
    [Input("salary_file", "filename"), Input("salary_file", "contents")]
)
def salary(filename, contents):
    if contents is None:
        return [{}], []
    GlobalVar.salary_df = parse_contents(contents, filename)
    return GlobalVar.salary_df.to_dict('records'), [{"name": i, "id": i} for i in GlobalVar.salary_df.columns]


@callback(
    Output('url', 'pathname'),
    Input("shift_process", "n_clicks")
)
def start_processing(n, ):
    if n is not None and len(GlobalVar.attendance_df) != 0:
        GlobalVar.attendance_df = prepare_df(GlobalVar.attendance_df, GlobalVar.salary_df,
                                             GlobalVar.shifts_df)
        return "/Im93F"

    return "/XuLoD"
