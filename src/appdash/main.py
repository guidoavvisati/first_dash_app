# load the resuired modules
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_daq as daq
import numpy as np
import os
import flask

from src.appdash.predictions import mtcars, preds, fit, cyl_enc


"""
# Setup the app
# the template is configured to execute 'server' on 'src/main.py'

dash apps are unstyled by default
external CSS stylesheets
https://dash.plotly.com/external-resources
"""

server = flask.Flask(__name__)
server.secret_key = os.environ.get("secret_key", str(np.random.randint(0, 1000000)))

external_stylesheets = [
    "https://codepen.io/chriddyp/pen/bWLwgP.css",
]

# create an instance of a dash app
app = dash.Dash(
    __name__,
    external_scripts=None,
    external_stylesheets=external_stylesheets,
    server=server,
)
app.title = "Predicting MPG"

# I compute these up front to avoid having to
# calculate thes twice
unq_cyl = np.sort(mtcars["cyl"].unique().astype(int)).astype(str)
opts_cyl = [{"label": i, "value": str(i)} for i in unq_cyl]


app.layout = html.Div(
    [
        html.H5("Displacement (in cubic inches):"),
        html.Br(),
        html.Br(),
        daq.Slider(
            id="input-disp",
            min=np.floor(mtcars["disp"].min()),
            max=np.ceil(mtcars["disp"].max()),
            step=0.5,
            dots=False,
            handleLabel={"showCurrentValue": True, "label": "Value"},
            value=np.floor(mtcars["disp"].mean()),
        ),
        html.H5("Quarter mile time:"),
        html.Br(),
        daq.Slider(
            id="input-qsec",
            min=np.floor(mtcars["qsec"].min()),
            max=np.ceil(mtcars["qsec"].max()),
            dots=False,
            handleLabel={"showCurrentValue": True, "label": "Value"},
            step=0.25,
            value=np.floor(mtcars["qsec"].mean()),
        ),
        html.H5("Number of cylinders:"),
        html.Br(),
        dcc.RadioItems(
            id="input-cyl",
            options=opts_cyl,
            value=opts_cyl[0].get("value"),
            labelStyle={"display": "inline-block"},
        ),
        html.Br(),
        daq.ToggleSwitch(
            id="input-am",
            label="Has manual transmission",
            value=False,
            style={"display": "inline-block"},
        ),
        html.H2(id="output-prediction"),
        html.Br(),
        dcc.Dropdown(
            id="my-dropdown",
            options=[
                {"label": "Linear", "value": "LINEAR"},
                {"label": "Log", "value": "LOG"},
            ],
            value="LINEAR",
            style={
                "background-color": "lightblue",
                "display": "inline-block",
                "width": "200px",
                "border": "2px solid blue",
                # "padding": "10px"
            },
        ),
        html.Br(),
        dcc.Graph(
            id="my-graph", style={"display": "inline-block", "width": "1000px",},
        ),
    ]
)


# callback will watch for changes in inputs and re-execute when any
# changes are detected.
@app.callback(
    dash.dependencies.Output("output-prediction", "children"),
    [
        dash.dependencies.Input("input-disp", "value"),
        dash.dependencies.Input("input-qsec", "value"),
        dash.dependencies.Input("input-cyl", "value"),
        dash.dependencies.Input("input-am", "value"),
    ],
)
def callback_pred(disp: float, qsec: float, cyl: str, am: bool) -> str:
    """Pass values from the UI on to our prediction function defined in
    predictions.py.

    Parameters
    ----------
    disp
    qsec
    cyl
    am

    Returns
    -------
    None
    """

    pred = preds(
        fit=fit, cyl_enc=cyl_enc, disp=disp, qsec=qsec, am=np.float64(am), cyl=cyl
    )
    # return a string that will be rendered in the UI
    return "Predicted MPG: {}".format(pred)


@app.callback(
    dash.dependencies.Output("my-graph", "figure"),
    [dash.dependencies.Input("my-dropdown", "value")],
)
def update_graph(selected_dropdown_value):
    if selected_dropdown_value == "LINEAR":
        return {
            "data": [{"x": mtcars.index, "y": mtcars.disp}],
            "layout": {"margin": {"l": 200, "r": 200, "t": 20, "b": 30}},
        }
    else:
        return {
            "data": [{"x": mtcars.index, "y": np.log(mtcars.disp)}],
            "layout": {"margin": {"l": 200, "r": 200, "t": 20, "b": 30}},
        }


# for running the app
if __name__ == "__main__":
    app.server.run(debug=True, threaded=True)
