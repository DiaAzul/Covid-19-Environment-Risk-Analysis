# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import logging

from Apptext import Apptext as at
from Appcontrols import Appcontrols as ac
from Appgraph import Appgraph as ag
from Appdecoration import Appdecoration as ad

app = dash.Dash(__name__)
logo = app.get_asset_url('logo.png')

app.layout = html.Div([
    # Outer block for header & footer

    ad.page_header(logo),
    #Inset Div spacer so that top of scrollnig text not hidden behind title bar
    html.Div(style={'height':'60px'}),

    html.Div([

        at.introduction_heading(),


        html.Div(
            at.introduction_text(),
            style={'columns' : '400px 3',
                    'column-rule-color': 'lightblue'}
        ),

        html.Hr(),

        html.Table(
            html.Tbody(
                html.Tr([
                    html.Td([
                        at.base_case_assumptions_heading(),
                        at.base_case_assumptions_text(),
                        at.exhalation_rate_heading(),
                        ac.exhalation_rate(),
                        at.exhalation_rate_text(),
                        at.ventilation_heading(),
                        at.ventilation_text(),
                        at.distance_heading(),
                        at.distance_text(),
                        at.inhalation_rate_heading(),
                        at.inhalation_rate_text(),
                        at.time_heading(),
                        at.time_text()
                    ], style={'width':'50%',
                            'word-wrap':'break-word',
                            'vertical-align':'top'}
                    ),
                    html.Td([
                        ag.inline_graph()
                    ], style={ 'width': '50%',
                            'vertical-align': 'top'}
                    )
                ])
            ),
        style={'table-layout':'fixed','width': '100%'}
        )

    ], style={'margin': '10px'}
    ),

    ad.page_footer()
])


if __name__ == '__main__':
    app.run_server(debug=True)