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

print(f"logo:{logo}")

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
                        html.Label('Activity of infected person'),
                        ac.exhalation_rate()
                    ], style={ 'width': '50%',
                            'vertical-align': 'top'}
                    ),
                    html.Td([
                        ag.inline_graph()
                    ], style={ 'width': '50%',
                            'vertical-align': 'middle'}
                    )
                ])
            ), style={'width': '100%'}
        )

    ], style={'margin': '10px'}
    ),

    ad.page_footer()
])


if __name__ == '__main__':
    app.run_server(debug=True)