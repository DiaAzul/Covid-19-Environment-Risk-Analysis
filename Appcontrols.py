""" The Appcontrols file contains user input controls to modify the chart"""

import dash
import dash_core_components as dcc
import dash_html_components as html


class Appcontrols:
    """This class contains controls used within the app to adjust
    calculations and information shown on the chart.
    Methods should be defined as staticMethods.
    """

    @staticmethod
    def exhalation_rate():
        return dcc.Dropdown(
                    options=[
                            {'label':'resting', 'value':98.1},
                            {'label':'standing', 'value':147},
                            {'label':'light exercise', 'value':317}
                    ],
                    id='dd_exhalation_rate',
                    value=98.1,
                    style = ({'width':'200px'})
                )