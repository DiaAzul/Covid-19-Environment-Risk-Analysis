# -*- coding: utf-8 -*-
import dash
# import dash_core_components as dcc
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

# TODO: use isfile to determine whether file exists (extended descriptions)
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

        # Main scrollable contenxt (controls and graph)
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
                ac.control('ventilation-aer'),
                at.text('ventilation'),
                at.heading('distance'),
                ac.control('average-occupancy'),
                at.text('distance'),
                at.heading('inhalation'),
                ac.control('inhalation-rate'),
                ac.control('inhalation-mask'),
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
            'ctrl-ventilation-aer',
            'ctrl-average-occupancy',
            'ctrl-exhalation-mask',
            'ctrl-exhalation-rate',
            'ctrl-inhalation-mask',
            'ctrl-inhalation-rate',
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
    Output(component_id='inline-chart', component_property='children'),
    get_list_of_input_callbacks())
def update_chart(*args):
    kwargs = {}
    for index, id in enumerate(get_list_of_inputs()):
        kwargs[id] = args[index]

    return ag.inline_graph(**kwargs)


if __name__ == '__main__':
    app.run_server(debug=True)
