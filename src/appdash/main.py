# load the resuired modules
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_daq as daq
import numpy as np

from appdash.predictions import mtcars, preds, fit, cyl_enc


# create an instance of a dash app
app = dash.Dash(__name__)
app.title = 'Predicting MPG'

# dash apps are unstyled by default
# this css I'm using was created by the author of Dash
# and is the most commonly used style sheet
app.css.append_css({
    "external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"
})

# I compute these up front to avoid having to
# calculate thes twice
unq_cyl = mtcars['cyl'].unique()
unq_cyl.sort() # so it's in a nice order
opts_cyl = [{'label': i, 'value': i} for i in unq_cyl]


app.layout = html.Div([

        html.H5('Displacement (in cubic inches):'),
        html.Br(), html.Br(),
        daq.Slider(
            id='input-disp',
            min=np.floor(mtcars['disp'].min()),
            max=np.ceil(mtcars['disp'].max()),
            step=.5,
            dots=False,
            handleLabel={"showCurrentValue": True,"label": "Value"},
            value=np.floor(mtcars['disp'].mean())),

        html.H5('Quarter mile time:'),
        html.Br(),
        daq.Slider(
            id='input-qsec',
            min=np.floor(mtcars['qsec'].min()),
            max=np.ceil(mtcars['qsec'].max()),
            dots=False,
            handleLabel={"showCurrentValue": True,"label": "Value"},
            step=.25,
            value=np.floor(mtcars['disp'].mean())),

        html.H5('Number of cylinders:'),
        dcc.RadioItems(
            id='input-cyl',
            options=opts_cyl,
            value=opts_cyl[0].get('value'),
            labelStyle={'display': 'inline-block'}),

        daq.ToggleSwitch(
            id='input-am',
            label='Has manual transmission',
            value=False),

        html.H2(id='output-prediction')
])


# callback will watch for changes in inputs and re-execute when any
# changes are detected.
@app.callback(
    dash.dependencies.Output('output-prediction', 'children'),
    [
        dash.dependencies.Input('input-disp', 'value'),
        dash.dependencies.Input('input-qsec', 'value'),
        dash.dependencies.Input('input-cyl', 'value'),
        dash.dependencies.Input('input-am', 'value')])
def callback_pred(disp, qsec, cyl, am):
    # pass values from the function on to our prediction function
    # defined in setup
    pred = preds(fit=fit,
                 cyl_enc=cyl_enc,
                 disp=disp,
                 qsec=qsec,
                 am=np.float64(am),
                 cyl=cyl)
    # return a string that will be rendered in the UI
    return "Predicted MPG: {}".format(pred)


# for running the app
if __name__ == '__main__':
    app.run_server(debug=True)

def run():
    return True
