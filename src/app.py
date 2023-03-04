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

graph = dcc.Graph(id='surface-plot', figure=first_fig,
                  style={'border': '1px solid lightgray'},)

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
           "left": "1rem", "margin": "1rem", "zIndex": "1", 'backgroundColor': toolbox_color}
)


button_group = html.Div(
    [
        dbc.RadioItems(
            id="radios",
            className="btn-group",
            inputClassName="btn-check",
            labelClassName="btn btn-outline-primary",
            labelCheckedClassName="active",
            options=[
                {"label": "Light Mode", "value": 1},
                {"label": "Dark Mode", "value": 2},
            ],
            value=1,
        ),
        html.Div(id="output"),
    ],
    className="radio-group",
)


app.layout = html.Div([
    dbc.NavbarSimple(
        children=[
            dbc.Col([
                dbc.Row([
                    html.H4('Super Plotter 4.4', style={'color': 'white'})
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
    graph,
    function_card_2,
    offcanvas
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
    print(function_str)
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


if __name__ == '__main__':
    app.run_server(debug=True)
