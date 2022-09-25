from models.global_vars import GlobalVar as g
from dash import Dash, callback, html, dcc, dash_table, Input, Output, State, MATCH, ALL, no_update

salary_page = dash_table.DataTable(id="final_graph",
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

                                       }

                                   ],
                                   style_header={
                                       'backgroundColor': 'rgb(50, 114, 193)',
                                       'color': 'white',
                                       'fontWeight': 'bold',
                                       'textAlign': 'center',
                                   },
                                   editable=False,
                                   filter_action='native',
                                   export_format='xlsx',
                                   export_headers='display',
                                   merge_duplicate_headers=True
                                   )

salary_page = html.Div([
    salary_page,

], style={"marginLeft": "10px", "marginRight": "10px"})


@callback(
    Output("final_graph", "data"),
    Output("final_graph", "columns"),
    Input('url2', 'pathname'),
)
def salary_show(pathname, ):
    if pathname == '/CoP3?':
        return g.final_df.to_dict('records'), [{"name": i, "id": i} for i in
                                               g.final_df.columns]
    return no_update, no_update
