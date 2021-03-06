# -*- coding: utf-8 -*-
import dash
import dash_html_components as html
from dash.dependencies import Input, Output
import os


from Apptext import Apptext
from Appcontrols import Appcontrols
from Appgraph import Appgraph as ag
from Appdecoration import Appdecoration as ad

app = dash.Dash(__name__)
logo = app.get_asset_url('logo.png')

# Import content for text fields
cwd = os.path.dirname(os.path.abspath(__file__))

# Option to include a file with extended content which overrides standard content
if os.path.isfile(f"{cwd}/config/content-extended.yml"):
    at = Apptext(f"{cwd}/config/content-extended.yml")
else:
    at = Apptext(f"{cwd}/config/content.yml")
# Import the configuration of the controls
ac = Appcontrols(f"{cwd}/config/controls.yml")

app.layout = html.Div([

    ad.page_header(logo),

    html.Div([

        # Introduction text
        html.Div([
            at.introduction_heading(),
            at.introduction_text(),
            html.Hr(className='introduction-break-after'),
            ], className='introduction-wrapper'),

        # Main scrollable content (controls and graph)
        html.Div([
            html.Div(id='inline-chart', className='graph-container'),
            html.Div([
                at.heading('base_case_assumptions'),
                ac.control('room-length'),
                ac.control('room-width'),
                ac.control('room-height'),
                at.text('base_case_assumptions'),
                at.heading('exhalation'),
                ac.control('exhalation-rate'),
                ac.control('exhalation-mask'),
                at.text('exhalation'),
                at.heading('ventilation'),
                ac.control('ventilation-type'),
                ac.control('ventilation-building'),
                ac.control('ventilation-aer'),
                at.text('ventilation'),
                at.heading('distance'),
                ac.control('average-occupancy'),
                at.text('distance'),
                at.heading('inhalation'),
                # Inhalation should match exhalation options, the original controls
                # were replaced with display boxes so that inhalation always matches
                # exhalation options. The original code is retained in case the option
                # to have different settings is required. Additional changes are required
                # in the callback function below, and Appgraph where the inhalation rate
                # options are copied from the exhalation settings.
                # ac.control('inhalation-rate'),
                # ac.control('inhalation-mask'),
                html.Div(id='inhalation-rateT', className='display-value-container'),
                html.Div(id='inhalation-maskT', className='display-value-container'),
                at.text('inhalation'),
                at.heading('time'),
                ac.control('time-in-environment'),
                at.text('time')
            ],
                className='text-container',
            )
        ],
            className='flexbox-wrapper',
        )
    ]),

    ad.page_footer()
])


# To manage a long list of inputs, define the inputs as a list
def get_list_of_inputs():
    return ['ctrl-room-length',
            'ctrl-room-width',
            'ctrl-room-height',
            'ctrl-ventilation-type',
            'ctrl-ventilation-building',
            'ctrl-ventilation-aer',
            'ctrl-average-occupancy',
            'ctrl-exhalation-mask',
            'ctrl-exhalation-rate',
            # 'ctrl-inhalation-mask',
            # 'ctrl-inhalation-rate',
            'ctrl-time-in-environment'
            ]


# Create a list of callbacks to use in the wrapper based on that list
def get_list_of_input_callbacks():
    ids = get_list_of_inputs()
    callback_list = []
    for id in ids:
        callback_list.append(Input(component_id=id, component_property='value'))
    return callback_list


# Define the callback function then pack returned values from list into a dictionary
@app.callback(
    [Output(component_id='inline-chart', component_property='children'),
     Output(component_id='inhalation-rateT', component_property='children'),
     Output(component_id='inhalation-maskT', component_property='children')],
    get_list_of_input_callbacks())
# The callback only provides a list of values with no id information, this is risky
# as any changes in the code could shift values in the array which require multiple
# code changes to keep things synchronised. Therefore, take the list of values and
# transform into a dictionary with id:value pairs.
def update_chart(*args):
    kwargs = {}
    # Iterate over the list of inputs and create a dictionary to pass to the function
    # which will perform processing and return an object to display.
    for index, id in enumerate(get_list_of_inputs()):
        kwargs[id] = args[index]

    return (ag.inline_graph(ac, **kwargs),
            ag.inline_value(ac, 'exhalation-rate', 'inhalation-rate', **kwargs),
            ag.inline_value(ac, 'exhalation-mask', 'inhalation-mask', **kwargs))


if __name__ == '__main__':
    app.run_server(debug=True)
