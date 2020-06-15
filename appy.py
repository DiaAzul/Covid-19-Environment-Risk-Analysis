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


# Define callbacks
@app.callback(
    Output(component_id='inline-chart', component_property='children'),
    [Input(component_id='ctrl-exhalation-rate', component_property='value')]
)
def update_chart(input_value):
    return ag.inline_graph(input_value)


if __name__ == '__main__':
    app.run_server(debug=True)
