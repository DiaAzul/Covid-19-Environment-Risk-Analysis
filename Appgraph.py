""" The Appgraph file contains methods to require a graph for display"""

import dash
import dash_core_components as dcc
import dash_html_components as html

class Appgraph:
    """This class produces graphs for display based upon inputs received.
    Methods should be defined as staticMethods.
    """   

    @staticmethod
    def inline_graph():
        return dcc.Graph(
                id='example-graph',
                figure={
                    'data': [
                        {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                        {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
                    ],
                    'layout': {
                        'title': 'Dash Data Visualization'
                    }
                }
            )
