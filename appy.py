# -*- coding: utf-8 -*-
import dash
# import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output


from Apptext import Apptext
from Appcontrols import Appcontrols
from Appgraph import Appgraph as ag
from Appdecoration import Appdecoration as ad

app = dash.Dash(__name__)
logo = app.get_asset_url('logo.png')

at = Apptext('./config/content.yml')
ac = Appcontrols('./config/controls.yml')

app.layout = html.Div([
    # Outer block for header & footer

    ad.page_header(logo),
    # Inset Div spacer so that top of scrollnig text not hidden behind
    # title bar
    html.Div(style={'height': '60px'}),

    # Everything between header and footer
    html.Div([
        
        # Introduction text
        html.Div([
        at.introduction_heading(),
        at.introduction_text(),
        html.Hr(className='introduction-break-after'),
        ], className='introduction-wrapper'),

        # Main scollable contenxt (controls and graph)
        html.Div([
            html.Div(id='inline-chart', className='graph-container'),
            html.Div([
                at.heading('base_case_assumptions'),
                at.text('base_case_assumptions'),
                at.heading('exhalation'),
                ac.control('exhalation-rate'),
                at.text('exhalation'),
                at.heading('ventilation'),
                at.text('ventilation'),
                at.heading('distance'),
                at.text('distance'),
                at.heading('inhalation'),
                at.text('inhalation'),
                at.heading('time'),
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
