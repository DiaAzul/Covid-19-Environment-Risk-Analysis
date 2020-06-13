""" The Appgraph file contains methods to require a graph for display"""

# import dash
import dash_core_components as dcc
# import dash_html_components as html
import plotly.graph_objects as go
import math


class Appgraph:
    """This class produces graphs for display based upon inputs received.
    Methods should be defined as staticMethods.
    """
    @staticmethod
    def inline_graph(ex_rate):
        return dcc.Graph(
                id='example-graph',
                figure=Appgraph.parameterless_call(ex_rate)
            )

    @staticmethod
    def parameterless_call(ex_rate):
        r = {'Time': math.log2(1 + .5),
             'Exhalation': math.log2(1 + ex_rate/147),
             'Ventilation': math.log2(1 + .5),
             'Distance': math.log2(1 + .5),
             'Inhalation': math.log2(1 + .5)}

        chart = Appgraph.risk_assessment_chart(r, "Environment risk assessment")  # noqa:E501
        return chart

    @staticmethod
    def risk_assessment_chart(r, chart_title):
        categories = [key for key, item in r.items()]
        data = [item for key, item in r.items()]

        fig = go.Figure()

        fig.add_trace(go.Scatterpolar(
            r=data,
            theta=categories,
            fill='toself'
        ))

        fig.update_layout(
            showlegend=False,
            title={
                'text': chart_title,
                'x': 0.5,
                'xanchor': 'center'
            },
            font={
                'size': 18
            },
            polar={
                'radialaxis': {
                    'type': 'linear',
                    'visible': True,
                    'range': [0, 2.2],
                    'angle': 90,
                    'tickangle': 90,
                    'tickfont': {
                        'size': 12
                    },
                    'tickmode': 'array',
                    'tickvals': [0, .1, 1, 2],
                    'ticktext': ['', 'Low', 'Medium', 'High']
                },
                'angularaxis': {
                    'direction': 'clockwise'
                }
            }
        )

        return fig
