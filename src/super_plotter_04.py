import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
import plotly.graph_objs as go
import numpy as np
import sympy
from dash_extensions.enrich import Output, DashProxy, Input, MultiplexerTransform, html
from dash.dependencies import Input, Output, State

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

toolbox_color = '#383838'

x, y = sympy.symbols('x y')

z = sympy.parse_expr('1/sin(7*x)+1/sin(4*y)')
f = sympy.lambdify((x, y), z, 'numpy')
x_vals = np.linspace(-5, 5, 100)
y_vals = np.linspace(-5, 5, 100)
x_mesh, y_mesh = np.meshgrid(x_vals, y_vals)
z_mesh = f(x_mesh, y_mesh)

first_fig = go.Figure(
    data=[go.Surface(x=x_vals, y=y_vals, z=z_mesh, colorscale='Viridis', showscale=False)])
first_fig.update_layout(margin=dict(l=10, r=10, t=10, b=10), height=800,)
first_fig.update_traces(contours_z=dict(show=True, usecolormap=True,
                                        highlightcolor="limegreen", project_z=True))

# filter out 'nan' values for log etc
mask = np.isnan(z_mesh)
z_mesh = z_mesh[~mask]
z_max = np.max(z_mesh)
z_min = np.min(z_mesh)

# creating plot for prescribed x
x = 3
z_vals = f(x, y_vals)
first_fig_x = go.Figure(
    data=[go.Scatter(x=y_vals, y=z_vals, mode='lines', line=dict(color='#008B8B'))])
first_fig_x.update_layout(xaxis_title="y",
                          margin=dict(l=0, r=10, t=10, b=10), height=400,
                          yaxis=dict(range=[z_min, z_max])
                          )

# creating plot for prescribed y
y = 3
z_vals = f(x_vals, y)
first_fig_y = go.Figure(
    data=[go.Scatter(x=x_vals, y=z_vals, mode='lines', line=dict(color='#008B8B'))])
first_fig_y.update_layout(xaxis_title="x",
                          margin=dict(l=0, r=10, t=20, b=10), height=400,
                          yaxis=dict(range=[z_min, z_max])
                          )

graph = dcc.Graph(id='surface-plot', figure=first_fig,
                  style={'border': '1px solid lightgray'},)

graph_x = dcc.Graph(id='x-plot', figure=first_fig_x,
                    # style={'border': '1px solid lightgray'},
                    )
graph_y = dcc.Graph(id='y-plot', figure=first_fig_y,
                    # style={'border': '1px solid lightgray'},
                    )

card_1 = dbc.Card([
    dbc.CardBody([
        html.P(
            'To get started and to get a feel for the space try the following:'),
        html.P('x+y'),
        html.P('x*y'),
        html.P('x*y**2'),
        html.P('x**2*y**2'),
    ])
], style={'marginTop': '10px'})

card_2 = dbc.Card([
    dbc.CardBody([
        html.P(
            'You can also use sin() and cos(), but also tan() and log(). My favorites are those:'),
        html.P('sin(0.2*x*y)'),
        html.P('sin(0.5*x*y)+cos(x*3)+0.3*y*x'),
        html.P('log(x*y)'),
    ])
], style={'marginTop': '10px'})

card_3 = dbc.Card([
    dbc.CardBody([
        html.P(
            'Finally, you can play around with mathematical concepts. E.g., observe what happens when you divide by x and y or when you only take the absolute:'),
        html.P('1/x+1/y'),
        html.P('1/sin(x)+1/tan(y)+y**3'),
        html.P('log(abs(x*y))'),
        html.P('log(abs(10+x*y))'),
    ])
], style={'marginTop': '10px'})

offcanvas = html.Div(
    [
        dbc.Offcanvas(
            children=[
                html.P(
                    "This app was created to make the invisible visible. It makes it easy to visualize 2d functions that are hard to imagine. Be inspired by the following gallery and have fun exploring the world of math."
                ),
                card_1,
                card_2,
                card_3,
            ],
            id="offcanvas",
            title="Info",
            is_open=False,
        ),
    ]
)


function_card_2 = dbc.Card(
    dbc.CardBody([
        dbc.Input(id='function-input',
                  placeholder='Enter your function here...'),
        dbc.Row([
                dbc.Col([
                    # dbc.Button('Plot Function', id='plot_button'),
                ], style={'align-items': 'right'})
                ], justify='end'),
        dbc.Row([
                dbc.Col([
                    dbc.Button('Info', id='info_button', color='secondary',
                               style={'marginRight': '20px'}),
                ], style={'display': 'flex', 'align-items': 'left'}),
                dbc.Col([
                    dbc.Button('Plot Function', id='plot_button'),
                ], width={'size': 'auto'}, className='text-center')
                ], justify='end', style={'display': 'flex', 'align-items': 'right', 'marginTop': '10px'}),
    ]),
    style={"width": "20rem", "position": "absolute", "top": "6rem",
           "left": "0.5rem", "margin": "1rem", "zIndex": "1", 'backgroundColor': toolbox_color}
)


app.layout = html.Div([
    dbc.NavbarSimple(
        children=[
            dbc.Col([
                dbc.Row([
                    html.H4('Super Plotter 4.4', style={
                            'color': 'white'}, id='app_title')
                ], style={'marginBottom': '0px', 'marginTop': '0px'}),
                dbc.Row([
                    html.P('created by Simon Wichmann',
                           style={'color': 'gray'})
                ], style={'marginBottom': '0px', 'marginTop': '0px'})
            ], style={'marginBottom': '0px', 'marginTop': '0px'}),
        ],
        color=toolbox_color,
        dark=True
    ),
    dbc.Row([
        html.Div([
            graph,
            function_card_2,
        ], style={'width': '70%', 'display': 'inline-block'}),
        html.Div([
            dbc.Row([
                graph_x
            ]),
            dbc.Row([
                graph_y
            ])
        ], style={'width': '30%', 'display': 'inline-block', 'border': '1px solid lightgray'}),
    ]),
    offcanvas,
])

# Define the callback


@ app.callback(
    Output(component_id='surface-plot', component_property='figure'),
    [
        Input(component_id='plot_button',
              component_property='n_clicks'),
        State(component_id='function-input', component_property='value'),
        State(component_id='surface-plot', component_property='figure')
    ],
    prevent_initial_callback=True
)
def update_figure(n_clicks, function_str, figure):
    # print(function_str)
    if function_str == None or function_str == '':
        return first_fig

    x, y = sympy.symbols('x y')

    try:
        z = sympy.parse_expr(function_str)
        f = sympy.lambdify((x, y), z, 'numpy')
    except:
        print('excepted...')
        return figure

    x_vals = np.linspace(-5, 5, 100)
    y_vals = np.linspace(-5, 5, 100)
    x_mesh, y_mesh = np.meshgrid(x_vals, y_vals)
    z_mesh = f(x_mesh, y_mesh)

    fig_2 = go.Figure(
        data=[go.Surface(x=x_vals, y=y_vals, z=z_mesh, colorscale='Viridis', showscale=False)])
    fig_2.update_layout(margin=dict(l=10, r=10, t=10, b=10))
    fig_2.update_traces(contours_z=dict(show=True, usecolormap=True,
                                        highlightcolor="limegreen", project_z=True))

    return fig_2


@app.callback(
    Output("offcanvas", "is_open"),
    Input("info_button", "n_clicks"),
    [State("offcanvas", "is_open")],
)
def toggle_offcanvas(n1, is_open):
    if n1:
        return not is_open
    return is_open


# clickData to add the 2d plots
@app.callback(
    Output(component_id='x-plot', component_property='figure'),
    Output(component_id='y-plot', component_property='figure'),
    [Input("surface-plot", "hoverData"),
     State(component_id='function-input', component_property='value'), ],
    prevent_initial_callback=True
)
def create_slice_plots(clickData, function_str):
    print(clickData)
    if clickData == None or clickData == '':
        return first_fig_x, first_fig_y
    if function_str == None or function_str == '':
        function_str = '1/sin(7*x)+1/sin(4*y)'
    point = clickData['points'][0]

    # create variables and extract functions
    x, y = sympy.symbols('x y')
    z = sympy.parse_expr(function_str)
    f = sympy.lambdify((x, y), z, 'numpy')

    # this is only needed to recieve the upper and lower z-bounds
    x_vals = np.linspace(-5, 5, 100)
    y_vals = np.linspace(-5, 5, 100)
    x_mesh, y_mesh = np.meshgrid(x_vals, y_vals)
    z_mesh = f(x_mesh, y_mesh)

    # filter out 'nan' values for log etc
    mask = np.isnan(z_mesh)
    z_mesh = z_mesh[~mask]
    z_max = np.max(z_mesh)
    z_min = np.min(z_mesh)

    # creating plot for prescribed x
    x = np.round(point['x'], 4)
    z_vals = f(x, y_vals)
    fig_x = go.Figure(
        data=[go.Scatter(x=y_vals, y=z_vals, mode='lines', line=dict(color='#008B8B'))])
    fig_x.update_layout(xaxis_title="y",
                        margin=dict(l=0, r=10, t=10, b=10), height=400,
                        yaxis=dict(range=[z_min, z_max])
                        )

    # creating plot for prescribed y
    y = np.round(point['y'], 4)
    z_vals = f(x_vals, y)
    fig_y = go.Figure(
        data=[go.Scatter(x=x_vals, y=z_vals, mode='lines', line=dict(color='#008B8B'))])
    fig_y.update_layout(xaxis_title="x",
                        margin=dict(l=0, r=10, t=20, b=10), height=400,
                        yaxis=dict(range=[z_min, z_max])
                        )

    return fig_x, fig_y


if __name__ == '__main__':
    app.run_server(debug=True)
