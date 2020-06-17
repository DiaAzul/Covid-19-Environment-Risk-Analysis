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
    def inline_graph(**kwargs):

        # Exhalation rate (base = Standing, no mask)
        base_exhalation_rate = 147 * (1 - 0)
        exhalation_rate = kwargs['ctrl-exhalation-rate'] * (1 - kwargs['ctrl-exhalation-mask'])
        exhalation_risk = exhalation_rate / base_exhalation_rate

        # Determination of the AER rate is spread over two controls
        # The first determines whether the building is naturally or mechanically ventilated
        aer_natural = kwargs['ctrl-ventilation-type']

        aer = kwargs['ctrl-ventilation-building'] if aer_natural == 'mechanical' else aer_natural

        aer = kwargs['ctrl-ventilation-aer'] if aer_natural == 'entered-value' else aer

        # Ventilation (base = 30m x 20m x 3m with AER:1.1)
        base_ventiliaton_rate = 1 / (30 * 20 * 3 * 1.1)
        ventilation_rate = 1 / (kwargs['ctrl-room-length'] *
                                kwargs['ctrl-room-width'] *
                                kwargs['ctrl-room-height'] *
                                aer)
                                #kwargs['ctrl-ventilation-aer'])
        ventilation_risk = ventilation_rate / base_ventiliaton_rate

        # Distance (base number of people in environment = 60, packing efficiency 75%)
        base_distance = math.sqrt((30 * 20) / 60 * 0.75)
        distance = math.sqrt((kwargs['ctrl-room-length'] * kwargs['ctrl-room-width']) /
                             kwargs['ctrl-average-occupancy'] * 0.75)
        distance_risk = 1 / (distance / base_distance)

        # Inhalation rate (bse = Standing, no mask)
        base_inhalation_rate = 0.54 * (1 - 0)
        inhalation_rate = kwargs['ctrl-inhalation-rate'] * (1 - kwargs['ctrl-inhalation-mask'])
        inhalation_risk = inhalation_rate / base_inhalation_rate

        # Time (base time = 30 minutes)
        base_exposure_time = 30
        exposure_time = kwargs['ctrl-time-in-environment']
        exposure_time_risk = exposure_time / base_exposure_time

        r = {'Time': math.log2(1 + exposure_time_risk),
             'Exhalation': math.log2(1 + exhalation_risk),
             'Ventilation': math.log2(1 + ventilation_risk),
             'Distance': math.log2(1 + distance_risk),
             'Inhalation': math.log2(1 + inhalation_risk)}

        fig = Appgraph.risk_assessment_chart(r, "Environment risk assessment")

        return dcc.Graph(
                id='environment-risk-assessment-graph',
                figure=fig
            )

    @staticmethod
    def parameterless_call(ex_rate):
        r = {'Time': math.log2(1 + .5),
             'Exhalation': math.log2(1 + ex_rate/147),
             'Ventilation': math.log2(1 + .5),
             'Distance': math.log2(1 + .5),
             'Inhalation': math.log2(1 + .5)}

        chart = Appgraph.risk_assessment_chart(r, "Environment risk assessment")
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
            paper_bgcolor='#FFF8DC',  # Cornsilk
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
