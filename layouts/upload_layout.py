import dash_bootstrap_components as dbc
from dash import Dash, callback, html, dcc, dash_table, Input, Output, State, MATCH, ALL

navbar = dbc.Navbar(
    [
        dbc.Container(
            [
                html.A(
                    dbc.Row(
                        [
                            dbc.Col(html.Img(src="assets/logo_horizontal_dark_blue.svg", height="30px")),
                        ],

                    ),
                    href="/XuLoD", )
            ]
        )
    ],
    color="white",
    sticky='top',
    style={
        'box-shadow': '0 0 7px #719ECE'
    }

)

# navbar2 = dbc.NavbarSimple(
#     children=[
#         # dbc.NavItem(dbc.NavLink("Page 1", href="#")),
#         # dbc.DropdownMenu(
#         #     # children=[
#         #     #     dbc.DropdownMenuItem("More pages", header=True),
#         #     #     dbc.DropdownMenuItem("Page 2", href="#"),
#         #     #     dbc.DropdownMenuItem("Page 3", href="#"),
#         #     # ],
#         #     nav=True,
#         #     in_navbar=True,
#         #     label="More",
#         # ),
#     ],
#     # brand_href="/page-1",
#     color="primary",
#     # dark=True,
#
#     # sticky='top',
#     # fixed='top'
#
# )

upload_attendance = dbc.Container([
    dcc.Upload(
        id="attendance_file",
        children=[
            'Drag and Drop or ',
            html.A('Select Attendance File'),
        ], style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'borderColor': 'rgb(50, 114, 193)',
            'textAlign': 'center'
        },
    )
],
    style={"marginTop": "15px"}
)

upload_shifts = dbc.Container([
    dcc.Upload(
        id="shifts_file",
        children=[
            'Drag and Drop or ',
            html.A('Select Shifts File'),
        ], style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'borderColor': 'rgb(50, 114, 193)',
            'textAlign': 'center'
        }
    )
],
    style={"marginTop": "15px"}
)
upload_salary = dbc.Container([
    dcc.Upload(
        id="salary_file",
        children=[
            'Drag and Drop or ',
            html.A('Select Salary File'),
        ], style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'borderColor': 'rgb(50, 114, 193)',
            'textAlign': 'center'
        }
    )
],
    style={"marginTop": "15px"}
)

attendance_table = dash_table.DataTable(id='attendance_graph',
                                        fixed_rows={'headers': True},
                                        style_cell={'minWidth': 95, 'textAlign': 'center', },
                                        style_table={'maxHeight': 500, 'overflowX': 'auto'},
                                        style_data={
                                            'color': 'black',
                                            'backgroundColor': 'rgb(253, 253, 253)',
                                        },
                                        style_data_conditional=[
                                            {
                                                'if': {'row_index': 'odd'},
                                                'backgroundColor': 'rgb(191, 217, 252)',
                                            }
                                        ],
                                        style_header={
                                            'backgroundColor': 'rgb(50, 114, 193)',
                                            'color': 'white',
                                            'fontWeight': 'bold',
                                            'textAlign': 'center'
                                        }
                                        )

employee_table = dash_table.DataTable(id='employee_graph',
                                      fixed_rows={'headers': True},
                                      style_cell={'minWidth': 95, 'textAlign': 'center', },
                                      style_table={'maxHeight': 500, 'overflowX': 'auto'},
                                      style_cell_conditional=[
                                          {
                                              'if': {'column_id': c},
                                              'textAlign': 'right'
                                          } for c in ['Date', 'Region']
                                      ],
                                      style_data={
                                          'color': 'black',
                                          'backgroundColor': 'rgb(253, 253, 253)',
                                      },
                                      style_data_conditional=[
                                          {
                                              'if': {'row_index': 'odd'},
                                              'backgroundColor': 'rgb(191, 217, 252)',
                                          }
                                      ],
                                      style_header={
                                          # 'backgroundColor': 'rgb(137, 192, 174)',
                                          'backgroundColor': 'rgb(50, 114, 193)',
                                          'color': 'white',
                                          'fontWeight': 'bold',
                                          # 'border': '1px solid rgb(115, 185, 202)',
                                          'textAlign': 'center'
                                      }
                                      )
salary_table = dash_table.DataTable(id='salary_graph',
                                    fixed_rows={'headers': True},
                                    style_cell={'minWidth': 95, 'textAlign': 'center', },
                                    style_table={'maxHeight': 500, 'overflowX': 'auto'},
                                    style_cell_conditional=[
                                        {
                                            'if': {'column_id': c},
                                            'textAlign': 'right'
                                        } for c in ['Date', 'Region']
                                    ],
                                    style_data={
                                        'color': 'black',
                                        'backgroundColor': 'rgb(253, 253, 253)',
                                    },
                                    style_data_conditional=[
                                        {
                                            'if': {'row_index': 'odd'},
                                            'backgroundColor': 'rgb(191, 217, 252)',
                                        }
                                    ],
                                    style_header={
                                        # 'backgroundColor': 'rgb(137, 192, 174)',
                                        'backgroundColor': 'rgb(50, 114, 193)',
                                        'color': 'white',
                                        'fontWeight': 'bold',
                                        # 'border': '1px solid rgb(115, 185, 202)',
                                        'textAlign': 'center'
                                    }
                                    )

upload_page = dbc.Container([
    dbc.Button("Process", id="shift_process", color="primary", outline=True,
               style={"marginTop": "10px",},),
    upload_attendance,
    dbc.Container(
        attendance_table,
        style={"marginTop": "50px", "marginBottom": "50px"},
    ),
    upload_salary,
    dbc.Container(
        salary_table,
        style={"marginTop": "50px", "marginBottom": "50px"},
    ),
    upload_shifts,
    dbc.Container(
        employee_table,
        style={"marginTop": "50px", "marginBottom": "50px"},
    ),

],
    style={
        'text-align': 'right'
    })
