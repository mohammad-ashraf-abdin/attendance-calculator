# from DBs.utils import datetime_server2local, execute_query
from layouts.salary_page_layout import salary_page
from models.global_vars import GlobalVar

from layouts.upload_layout import *
from pages.process_page import process_page
from pages.upload_page import upload_page

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True
)

app.title = "Attendance"
server = app.server

app.layout = html.Div(
    [
        navbar,
        dbc.Container(
            [

                dcc.Location(id='url', refresh=False),
                dcc.Location(id='url2', refresh=False),
                html.Div(id='page-content'),
            ]
        )
    ]
    ,
)

index_page = dbc.Container([
    html.Br(),
    dbc.Button("start",id="url",href="/XuLoD"),
],    className="d-grid gap-2 col-6 mx-auto",
)


# Update the index
@callback(Output('page-content', 'children'),
          [Input('url', 'pathname'), Input('url2', 'pathname')])
def display_page(pathname, pathname2):
    # print(pathname)
    if pathname == '/XuLoD' or pathname == '/':
        return upload_page
    elif pathname2 == '/CoP3?':
        return salary_page
    elif pathname == '/Im93F' and GlobalVar.attendance_df is not None:
        # print("WORK ON IT")
        return process_page
    else:
        return index_page
    # You could also return a 404 "URL not found" page here


if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=5002, debug=True)
