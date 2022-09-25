from datetime import timedelta
import dash_bootstrap_components as dbc
import pandas as pd
from dash import html, dash_table, callback, Output, Input, no_update, State, callback_context
from models.date_preprocess import attend_calc
from models.global_vars import GlobalVar as g
from utils.utils import days_hours_minutes

preprocess_table = dash_table.DataTable(id='preprocess_graph',
                                        # fixed_rows={'headers': True,},
                                        style_header_conditional=[{
                                            'if': {
                                                'column_id': ['Check-in2', 'Check-out2', 'index', ]},
                                            'display': 'None'
                                        }],
                                        style_cell={'minWidth': 95, 'textAlign': 'center', },
                                        style_table={'height': 500, 'overflowX': 'auto', 'overflowY': 'auto'},
                                        style_data={
                                            'color': 'black',
                                            'backgroundColor': 'rgb(253, 253, 253)',
                                            'textAlign': 'center'

                                        },
                                        style_data_conditional=[
                                            {
                                                'if': {'row_index': 'odd'},
                                                'backgroundColor': 'rgb(191, 217, 252)',
                                                'textAlign': 'center'
                                            },
                                            {
                                                'if': {
                                                    'filter_query': '{Check-in2} > {Check-out2}',
                                                    'column_id': ['Check-in', 'Check-out']
                                                },
                                                'backgroundColor': 'rgb(203, 68, 74)',
                                                'color': 'black'
                                            },
                                            {
                                                'if': {
                                                    'filter_query': '{early extra} > ""',
                                                    'column_id': 'Check_early_extra'
                                                },
                                                'backgroundColor': 'rgb(246, 195, 68)',
                                                'color': 'black'
                                            },
                                            {
                                                'if': {
                                                    'filter_query': '{late extra} > ""',
                                                    'column_id': 'Check_late_extra'
                                                },
                                                'backgroundColor': 'rgb(246, 195, 68)',
                                                'color': 'black'
                                            },
                                            {
                                                'if': {
                                                    'column_id': ['Check-in2', 'Check-out2', 'index', ]},
                                                'display': 'None'
                                            }

                                        ],
                                        style_header={
                                            # 'backgroundColor': 'rgb(137, 192, 174)',
                                            'backgroundColor': 'rgb(50, 114, 193)',
                                            'color': 'white',
                                            'fontWeight': 'bold',
                                            # 'border': '1px solid rgb(115, 185, 202)',
                                            'textAlign': 'center',
                                        },
                                        style_filter_conditional=[{
                                            'if': {
                                                'column_id': ['Check-in2', 'Check-out2', 'index', ]},
                                            'display': 'None'
                                        }],
                                        filter_action='native',
                                        editable=False
                                        )
process_page = html.Div([
    html.H2(id="header_text", children=[], style={"marginTop": "25px", "marginBottom": "25px"}),
    preprocess_table,
    # dbc.ButtonGroup([
    dbc.Button("Back", id="back", style={"display": "none"}),
    dbc.Button("Next", id="next"),
    # ], size="md", style={"marginTop": "50px", "marginBottom": "50px"}, ),
    html.Var(id="btn_var", children=0, style={"display": "none"}),
    dbc.Button("Finish", id="finish"),
    html.Div(id="hidden-d", children=[], style={"display": 'none'}),

], style={"marginLeft": "10px", "marginRight": "10px"})


@callback(
    Output("preprocess_graph", "data"),
    Output("preprocess_graph", "columns"),
    Output("btn_var", "children"),
    Output("header_text", "children"),
    Output("finish", "style"),
    Output("back", "style"),
    Output("next", "style"),
    Input('url', 'pathname'),
    Input('next', 'n_clicks'),
    Input('back', 'n_clicks'),
    Input('btn_var', 'children'),

)
def attendance(page, next, back, btn_var):
    if page == "/Im93F":
        if len(g.attendance_df) != 0:
            changed_id = [p['prop_id'] for p in callback_context.triggered][0]
            btn_var = btn_var - 1 if 'back' in changed_id else (btn_var + 1 if 'next' in changed_id else btn_var)
            attend_check_df = g.attendance_df
            attend_check_df['Check-in2'] = pd.to_datetime(attend_check_df['Check-in'], format='%H:%M')
            attend_check_df['Check-out2'] = pd.to_datetime(attend_check_df['Check-out'], format='%H:%M')
            attend_check_df['Attended hours'] = attend_check_df["Attended-hours"].apply(lambda x: x.time())
            attend_check_df = attend_check_df.loc[attend_check_df['Check-in2'] > attend_check_df['Check-out2']]
            attend_check_df['Lateness type'] = 'Unjustified'
            attend_check_df['Early Check-out Type'] = 'Unjustified'
            attend_check_df = attend_check_df[
                ["Name", "Date", "Day", "Shift Name", "Check-in", "Check-out", "Attended hours", "index", "Check-in2",
                 "Check-out2", "Lateness type", "Early Check-out Type"]]
            if len(attend_check_df) > 0 and btn_var == 0:  # ('back' in changed_id or btn_var[0]):
                return attend_check_df.to_dict('records'), [{"name": i, "id": i, 'editable': True} for i in
                                                            attend_check_df.columns], btn_var, "Correct Check Times", {
                           "display": 'none'}, {"display": 'none'}, {"display": 'inline-block'}
            else:
                if btn_var == 0:
                    btn_var += 1
                check_justifying_df = g.attendance_df.loc[
                    ~((g.attendance_df['lateness'].isin(['0'])) & (g.attendance_df['Early Check-out'].isin(['0'])))]
                check_justifying_df['Attended hours'] = check_justifying_df["Attended-hours"].apply(lambda x: x.time())

                check_justifying_df = check_justifying_df[
                    ["Name", "Date", "Day", "Shift Name", "Check-in", "Check-out", "Attended hours", 'lateness',
                     'Lateness type', 'Early Check-out', 'Early Check-out Type',
                     "index"]]
                if len(check_justifying_df) > 0 and btn_var == 1:  # (('next' in changed_id or btn_var[1]):
                    return check_justifying_df.to_dict('records'), [{"name": i, "id": i, 'editable': True} for i in
                                                                    check_justifying_df.columns], \
                           btn_var, "Justifying Times", {"display": 'none'}, {"display": 'inline-block'}, {
                               "display": 'inline-block'}
                elif btn_var == 2:  # (:
                    post_process_df = g.attendance_df
                    post_process_df['Check-in2'] = pd.to_datetime(post_process_df['Check-in'], format='%H:%M')
                    post_process_df['Check-out2'] = pd.to_datetime(post_process_df['Check-out'], format='%H:%M')
                    post_process_df = attend_calc(post_process_df)
                    post_process_df['late extra'] = post_process_df['late_extra'].astype('string')
                    post_process_df[['late extra']] = post_process_df[['late extra']].fillna('')
                    post_process_df['early extra'] = post_process_df['early_extra'].astype('string')
                    post_process_df[['early extra']] = post_process_df[['early extra']].fillna('')
                    post_process_df['work hours'] = post_process_df['work_hours'].astype('string')
                    post_process_df['deduct hours'] = post_process_df['deduct_hours'].astype('string')
                    post_process_df['Attended hours'] = post_process_df["Attended-hours"].apply(lambda x: x.time())

                    post_process_df = post_process_df[
                        ["Name", "Date", "Day", "Attendance", "Shift Name", "Check-in", "Check-in2", "Check-out",
                         "Attended hours", 'work hours',
                         'deduct_hours', 'Check_early_extra', 'early extra', 'Check_late_extra', 'late extra', 'index']]
                    return post_process_df.to_dict('records'), [{"name": i, "id": i, 'editable': True} for i in
                                                                post_process_df.columns], btn_var, "Extra Times", {
                               "display": 'none'}, {"display": 'inline-block'}, {"display": 'inline-block'}
                elif btn_var == 3:
                    g.final_df = g.attendance_df.copy()
                    g.final_df['Attended-hours'] = g.final_df['Attended-hours'].dt.time
                    g.final_df['Shift-Check-in'] = g.final_df["Shift-Check-in"].dt.time
                    g.final_df['Shift-Check-out'] = g.final_df["Shift-Check-out"].dt.time
                    return g.final_df.to_dict('records'), [{"name": i, "id": i} for i in
                                                           g.final_df.columns], btn_var, "Attendance Table", {
                               "display": 'inline-block'}, {"display": 'inline-block'}, {"display": 'none'}
                else:
                    return no_update, no_update, no_update, no_update, {"display": 'inline-block'}, {
                        "display": 'inline-block'}, {"display": 'none'}
        return no_update
    else:
        return no_update


@callback(
    Output('hidden-d', 'children'),
    Input('next', 'n_clicks'),
    Input('preprocess_graph', 'data_timestamp'),
    State('preprocess_graph', 'data'))
def update_columns(n, timestamp, rows):
    if rows is None:
        return []
    test2 = pd.DataFrame.from_records(rows)
    col = 'index'
    try:
        cols_to_replace = ['Check-in', 'Check-out', 'Lateness type', 'Early Check-out Type']
        g.attendance_df.loc[g.attendance_df[col].isin(test2[col]), cols_to_replace] = \
            test2.loc[test2[col].isin(g.attendance_df[col]), cols_to_replace].values

    except:
        try:
            cols_to_replace = ['Lateness type', 'Early Check-out Type']
            g.attendance_df.loc[g.attendance_df[col].isin(test2[col]), cols_to_replace] = \
                test2.loc[test2[col].isin(g.attendance_df[col]), cols_to_replace].values
        except:
            cols_to_replace = ['Check_early_extra', 'Check_late_extra']
            g.attendance_df.loc[g.attendance_df[col].isin(test2[col]), cols_to_replace] = \
                test2.loc[test2[col].isin(g.attendance_df[col]), cols_to_replace].values

    return []


@callback(
    Output('url2', 'pathname'),
    Input('finish', 'n_clicks')
)
def processing(n):
    if n:
        for idx, item in g.attendance_df.iterrows():
            if not isinstance(item["early_extra"], int):
                if not item["Check_early_extra"]:
                    g.attendance_df.loc[idx, "early_extra"] = timedelta(hours=0)
                if not item["Check_late_extra"]:
                    g.attendance_df.loc[idx, "late_extra"] = timedelta(hours=0)

        final_df = g.attendance_df.groupby(['Number', 'Name', 'Per Hour'])[
            'work_hours', 'deduct_hours', 'early_extra', 'late_extra'].sum().reset_index()
        for idx, item in final_df.iterrows():
            if not isinstance(item["early_extra"], int):
                final_df.loc[idx, "early_extra"] = days_hours_minutes(final_df['early_extra'][idx])
            if not isinstance(item["late_extra"], int):
                final_df.loc[idx, "late_extra"] = days_hours_minutes(final_df['late_extra'][idx])
            final_df.loc[idx, "work_hours"] = days_hours_minutes(final_df['work_hours'][idx])
            final_df.loc[idx, "deduct_hours"] = days_hours_minutes(final_df['deduct_hours'][idx])
            final_df.loc[idx, "salary"] = round((240 - final_df['deduct_hours'][idx]) * final_df['Per Hour'][idx], 2)
            final_df.loc[idx, "extra salary"] = round((final_df['early_extra'][idx] + final_df['late_extra'][idx]) * \
                                                      final_df['Per Hour'][idx], 2)
            final_df.loc[idx, "final salary"] = final_df.loc[idx, "salary"] + final_df.loc[idx, "extra salary"]
        # print(final_df)
        g.final_df = final_df
        return "/CoP3?"
    return no_update
