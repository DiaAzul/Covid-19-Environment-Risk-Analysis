""" The Appcontrols file contains user input controls to modify the chart"""

# import dash
import dash_core_components as dcc
<<<<<<< HEAD
import dash_html_components as html
import yaml
import itertools
=======
# import dash_html_components as html

>>>>>>> 9b7f1466b96f73f2d890152c59bb8c2c762512c7

class Appcontrols:
    """This class contains controls used within the app to adjust
    calculations and information shown on the chart.
    Methods should be defined as staticMethods.
    """
    def __init__(self, path):
        """Given the path to the config file load config into a directory

        Args:
            path (string): URI of the configuration file
        """
        with open(path) as file:
            self.controls = yaml.load(file, Loader=yaml.FullLoader)


    def control(self, control_id):
        control = self.controls.get(control_id, None)
        # Create a DIV with className option box and type flex -> Row
        # Add Markdown as flexbox 1 with introductory text
        # Add control as flexbox 2 with control (call as function returned)

        return html.Div([
            dcc.Markdown(control.get('description', 'Select an option'), className='control-description'),
            self.dropdown_box(control)
        ], className='control-wrapper')


    def dropdown_box(self, control):
        options = control.get('options', None)
        dropdown_list = []
        for _, value in options.items():
            dropdown_list.append(value)

<<<<<<< HEAD
        return html.Div(dcc.Dropdown(
                        options=dropdown_list,
                        # options=[
                        #         {'label':'resting', 'value':98.1},
                        #         {'label':'standing', 'value':147},
                        #         {'label':'light exercise', 'value':317}
                        # ],
                        id=control.get('id'),
                        value=98.1,
                    ),
                    className='control-dropdown'
        )
    
=======
    @staticmethod
    def exhalation_rate():
        return dcc.Dropdown(
                    options=[
                            {'label': 'resting', 'value': 98.1},
                            {'label': 'standing', 'value': 147},
                            {'label': 'light exercise', 'value': 317}
                    ],
                    id='dd_exhalation_rate',
                    value=98.1,
                    style=({'width': '200px'})
                )
>>>>>>> 9b7f1466b96f73f2d890152c59bb8c2c762512c7
