""" The Appgraph file contains methods to require a graph for display"""

import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import math


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

        # Assumptions for the risk assessment base case
        # The following assumption represent a small supermarket
        base = {}
        base['ctrl-exhalation-rate'] = 147
        base['ctrl-exhalation-mask'] = 0
        base['ctrl-room-length'] = 30
        base['ctrl-room-width'] = 20
        base['ctrl-room-height'] = 3
        base['ctrl-ventilation-aer'] = 1.1
        base['ctrl-average-occupancy'] = 60
        packing_efficiency = 0.75
        base['ctrl-inhalation-rate'] = 0.54
        base['ctrl-inhalation-mask'] = 0
        base['ctrl-time-in-environment'] = 30

        # Exhalation rate (base = Standing, no mask)
        base_exhalation_rate = base['ctrl-exhalation-rate'] * (1 - base['ctrl-exhalation-mask'])
        exhalation_rate = kwargs['ctrl-exhalation-rate'] * (1 - kwargs['ctrl-exhalation-mask'])
        exhalation_risk = exhalation_rate / base_exhalation_rate

        # Ventilation

        # Determination of the AER rate is spread over two controls
        # The first determines whether the building is naturally or mechanically ventilated
        aer_natural = kwargs['ctrl-ventilation-type']
        aer = kwargs['ctrl-ventilation-building'] if aer_natural == 'mechanical' else aer_natural
        aer = kwargs['ctrl-ventilation-aer'] if aer_natural == 'entered-value' else aer

        # Ventilation base case
        base_volume = base['ctrl-room-length'] * base['ctrl-room-width'] * base['ctrl-room-height']
        base_v_scalar = (base['ctrl-average-occupancy'] / base_volume /
                         base['ctrl-ventilation-aer'])  # *
                         # base['ctrl-time-in-environment'] / 60)
        base_ventilation = base_v_scalar * (math.exp(-base['ctrl-ventilation-aer'] *
                                            base['ctrl-time-in-environment'] / 60))

        # Ventilation scenario
        volume = kwargs['ctrl-room-length'] * kwargs['ctrl-room-width'] * kwargs['ctrl-room-height']
        v_scalar = (kwargs['ctrl-average-occupancy'] / volume / aer)  # *
                    # kwargs['ctrl-time-in-environment'] / 60)
        ventilation = v_scalar * (math.exp(-aer * kwargs['ctrl-time-in-environment'] / 60))

        ventilation_risk = ventilation / base_ventilation

        # Distance (base number of people in environment = 60, packing efficiency 75%)
        average_occupancy = kwargs['ctrl-average-occupancy']
        base_distance = math.sqrt((base['ctrl-room-length'] *
                                   base['ctrl-room-width']) /
                                  base['ctrl-average-occupancy'] * packing_efficiency)

        distance = math.sqrt((kwargs['ctrl-room-length'] *
                              kwargs['ctrl-room-width']) /
                             average_occupancy * packing_efficiency)

        distance_risk = 1 / (distance / base_distance)

        # Inhalation rates and mask assumptions are derived from settings from exhalation rate
        # This function looks up the exhalation assumption and then applies the assumption to the
        # inhalation control in order to get the assumption value
        _, ctrl_inhalation_rate = ac.fetch_dropdown_label_value('inhalation-rate',
                                                                'exhalation-rate',
                                                                kwargs['ctrl-exhalation-rate'])  # noqa:E501

        _, ctr_inhalation_mask = ac.fetch_dropdown_label_value('inhalation-mask',
                                                               'exhalation-mask',
                                                               kwargs['ctrl-exhalation-mask'])  # noqa:E501

        # Inhalation rate (bse = Standing, no mask)
        base_inhalation_rate = base['ctrl-inhalation-rate'] * (1 - base['ctrl-inhalation-mask'])

        # The inhalation controls are fixed to copy settings from exhalation assumptions
        # the following line is included should separate settings be required.
        # inhalation_rate = kwargs['ctrl-inhalation-rate'] * (1 - kwargs['ctrl-inhalation-mask'])
        inhalation_rate = ctrl_inhalation_rate * (1 - ctr_inhalation_mask)
        inhalation_risk = inhalation_rate / base_inhalation_rate

        # Time (base time = 30 minutes)
        base_exposure_time = base['ctrl-time-in-environment']
        exposure_time = kwargs['ctrl-time-in-environment']
        exposure_time_risk = exposure_time / base_exposure_time

        # Calculate overall risk
        quanta_concentration = Appgraph.average_concentration(exposure_time,
                                                              exhalation_rate,
                                                              volume,
                                                              aer)

        quanta_inhaled_per_person = 1 - math.exp(-quanta_concentration * inhalation_rate / 60)
        quanta_risk = quanta_inhaled_per_person * average_occupancy

        fig_gauge = Appgraph.inline_gauge_chart(quanta_risk, 'Risk Score')

        # Risk components chart

        r = {'Time': math.log2(1 + exposure_time_risk),
             'Exhalation': math.log2(1 + exhalation_risk),
             'Ventilation': math.log2(1 + ventilation_risk),
             'Distance': math.log2(1 + distance_risk),
             'Inhalation': math.log2(1 + inhalation_risk)}

        fig_radar = Appgraph.risk_assessment_chart(r, "Risk components")

        results_block = html.Div([
            dcc.Graph(id='environment-risk-assessment-gauge',
                      figure=fig_gauge,
                      className='gauge-chart'),
            dcc.Graph(id='environment-risk-assessment-graph',
                      figure=fig_radar)
        ])

        return results_block

    @staticmethod
    def average_concentration(t, Er, v, AER):
        Exp_AER = math.exp(-AER / 60)
        concentration_total = (Er / 60 * (1 + t * AER / 60 - Exp_AER ** t) /
                               ((1 - Exp_AER) * v * AER / 60))

        return concentration_total / 2

    @staticmethod
    def inline_gauge_chart(reading, chart_title):

        # define gauge segment levels
        zero = 0.0
        low_to_medium = 0.5
        medium_to_high = 1.5
        top = 5

        # constrain pointer to limits
        reading = min(max(reading, zero), top)

        labels = ['Low', 'Medium', 'High', ' ']
        colors = ['lightblue', 'moccasin', 'mistyrose', '#FFFFFF00']

        values = [low_to_medium - zero,
                  medium_to_high - low_to_medium,
                  top - medium_to_high,
                  top]

        values = [0.5, 1.0, 3.5, 5]

        base_chart = {
            'labels': labels,
            'values': values,
            'textinfo': 'label',
            'insidetextorientation': 'horizontal',
            'rotation': -90,
            'textfont_size': 12,
            'hole': .55,
            'direction': 'clockwise',
            'sort': False,
            'marker': {
                'colors': colors,
                'line': {
                    'color': '#FFFFFF',
                    'width': 2
                }
            }
        }

        layout = {
            'showlegend': False,
            'paper_bgcolor': '#FBFBFF',
            'height': 450,
            'width': 600,
            'title': {
                'text': chart_title,
                'x': 0.5,
                'xanchor': 'center'
            },
            'font': {
                'family': 'Proza Libre',
                'size': 18
            },
            'shapes': [{
                'type': 'path',
                'path': Appgraph.pointer_coordinates(reading, zero, top),
                'fillcolor': 'gainsboro',
                'line': {
                    'color': 'gainsboro',
                    'width': 0.5
                },
                'xref': 'paper',
                'yref': 'paper'
            }]
        }

        fig = go.Figure()
        fig.add_trace(go.Pie(base_chart))
        fig.update_layout(layout)

        return fig
    

    @staticmethod
    def pointer_coordinates(reading, min, max):

        # Angle of pointer (in radians)
        angle = math.pi * (reading - min) / (max - min)

        # Center point
        c_x = 0.5
        c_y = 0.5
        # Needle point
        np_x, np_y = Appgraph.polar_to_rectangular(0.3, angle)
        # Left, right need base points
        l_x, l_y = Appgraph.polar_to_rectangular(0.02, angle + Appgraph.degree_to_radians(180 - 60))
        r_x, r_y = Appgraph.polar_to_rectangular(0.02, angle + Appgraph.degree_to_radians(180 + 60))

        svg_path = f'M {c_x} {c_y} L {l_x} {l_y} L {np_x} {np_y} L {r_x} {r_y} Z'

        return svg_path  # 'M 0.515 0.5 L 0.5 0.8 L 0.485 0.5 Z'

    @staticmethod
    def polar_to_rectangular(r, t):
        # Assumes that co-ordinate (0, 0) is the centre of the chart which is plotly (0.5, 0.5)
        # Angular zero degrees points directly left from centre point (backwards from usual)
        # TODO: Find a better way to correct for aspect ratio
        x = 0.5 - r * math.cos(t) * 450 / 600
        y = 0.5 + r * math.sin(t)

        return x, y

    def degree_to_radians(t):
        return t / 180 * math.pi

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
            paper_bgcolor='#FBFBFF',
            title={
                'text': chart_title,
                'x': 0.5,
                'xanchor': 'center'
            },
            font={
                'family': 'Proza Libre',
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
    def inline_value(ac, source_control, value_control,  **kwargs):
        """Provides a string of html to display inhalation mask based upon exhalation mask assumption

        Args:
            ac {obj}: Class instance of the Appcontrol class
            source_control {str}: Root key for the control which determines value shown
            value_control {str}: Root key for the control which defines  to display

        Returns:
            str: String of html code representing inhalation mask assumption formated as a control.
        """
        source_dictionary = ac.controls.get(source_control)
        source_crtl_id = source_dictionary.get('id')
        source_value = kwargs[source_crtl_id]

        label, value = ac.fetch_dropdown_label_value(value_control,
                                                     source_control,
                                                     source_value)

        value_dictionary = ac.controls.get(value_control)
        value_ctrl_id = value_dictionary.get('id')
        value_description = value_dictionary.get('description')

        text = html.Div([
            dcc.Markdown(value_description,
                        className='control-description'),
            Appgraph.control_displaybox(value_ctrl_id, label)
        ], className='control-wrapper')

        return text
