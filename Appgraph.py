""" The Appgraph file contains methods to require a graph for display"""

import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import math


# TODO: Calculate an overall risk score and add to chart
class Appgraph:
    """Class containing methods to generate dynamic output.

    Methods should be defined as staticMethods.
    """
    @staticmethod
    def inline_graph(ac, **kwargs):
        """Given control input parameters produces html code for radar plot

        Args:
            ac (Class instance): Class reference to the Appcontrol class instance

        Returns:
            str: Html code to display the formated radar plot
        """
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
        ventilation_risk = ventilation_rate / base_ventiliaton_rate

        # Distance (base number of people in environment = 60, packing efficiency 75%)
        base_distance = math.sqrt((30 * 20) / 60 * 0.75)
        distance = math.sqrt((kwargs['ctrl-room-length'] * kwargs['ctrl-room-width']) /
                             kwargs['ctrl-average-occupancy'] * 0.75)
        distance_risk = 1 / (distance / base_distance)

        _, ctrl_inhalation_rate = ac.fetch_dropdown_label_value('inhalation-rate',
                                                                'exhalation-rate',
                                                                kwargs['ctrl-exhalation-rate'])  # noqa:E501

        _, ctr_inhalation_mask = ac.fetch_dropdown_label_value('inhalation-mask',
                                                               'exhalation-mask',
                                                               kwargs['ctrl-exhalation-mask'])  # noqa:E501

        # Inhalation rate (bse = Standing, no mask)
        base_inhalation_rate = 0.54 * (1 - 0)
        # inhalation_rate = kwargs['ctrl-inhalation-rate'] * (1 - kwargs['ctrl-inhalation-mask'])
        inhalation_rate = ctrl_inhalation_rate * (1 - ctr_inhalation_mask)
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
    def risk_assessment_chart(r, chart_title):
        """Generate radar chart using Plotly given parameter object

        Args:
            r (dict): Dictionary of parameters for the radar plot
            chart_title (str): Title for the chart

        Returns:
            str: Returns a string containing html code
        """
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

    @staticmethod
    def control_displaybox(id, content):
        """Wraps the same formating as a control around a text box

        Args:
            id (str): An html Id to reference the object in the DOM
            content (str): String to display in the text box

        Returns:
            str: A string of html code to be included in the DOM
        """
        return html.Div(html.P(
                            content,
                            id=id,
                            className='control-display-text-element'
                            ),
                        className='control-display-text'
                        )

    @staticmethod
    def inhalation_rate(ac, **kwargs):
        """Provides a string of html to display inhalation rate based upon exhalation rate activity

        Args:
            ac (Obj): Class instance of the Appcontrol class

        Returns:
            str: String of html code representing inhalation rate assumption formated as a control.
        """
        exhalation_rate = kwargs['ctrl-exhalation-rate']

        label, value = ac.fetch_dropdown_label_value('inhalation-rate',
                                                     'exhalation-rate',
                                                     exhalation_rate)

        text = html.Div([
            dcc.Markdown('This assumption is copied from exhalation and represents the typical activity of people in the environment',  # noqa:E501
                        className='control-description'),
            Appgraph.control_displaybox('crtl-inhalation-test', label)
        ], className='control-wrapper')

        return text

    @staticmethod
    def inhalation_mask(ac, **kwargs):
        """Provides a string of html to display inhalation mask based upon exhalation mask assumption

        Args:
            ac (Obj): Class instance of the Appcontrol class

        Returns:
            str: String of html code representing inhalation mask assumption formated as a control.
        """
        exhalation_mask = kwargs['ctrl-exhalation-mask']

        label, value = ac.fetch_dropdown_label_value('inhalation-mask',
                                                     'exhalation-mask',
                                                     exhalation_mask)

        text = html.Div([
            dcc.Markdown('This assumption is copied from exhalation and states what face covering most people are using',  # noqa:E501
                        className='control-description'),
            Appgraph.control_displaybox('crtl-inhalation-mask', label)
        ], className='control-wrapper')

        return text
