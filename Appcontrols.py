""" The Appcontrols file contains user input controls to modify the chart"""

# import dash
import dash_core_components as dcc
import dash_html_components as html
import yaml


class Appcontrols:
    """Controls within the app are defined within a configuration file.
    This file is loaded into this class at startup, which is then called by
    the layout to return html code for each control object. The styling for
    the control objects is defined within the app_specific css file.
    """
    def __init__(self, path):
        """Given the path to the config file load config into a directory

        Args:
            path (string): URI of the configuration file
        """
        with open(path) as file:
            self.controls = yaml.load(file, Loader=yaml.FullLoader)

        # Python equivalent of case statement is implemented using dictionary
        # of functions. This calls control function by type of control.
        self.control_selector = {
            'dropdown': self.control_dropdown,
            'number': self.control_number
        }

    def control(self, control_id):
        """Returns html for a control with description

        Args:
            control_id (str): ID of the control within the YAML file.

        Returns:
            str: Html code for the control
        """
        control = self.controls.get(control_id, None)

        type = control.get('type')
        get_control_html = self.control_selector.get(type)

        return html.Div([
            dcc.Markdown(control.get('description', 'Select an option'),
                        className='control-description'),
            get_control_html(control)
        ], className='control-wrapper')

    def control_dropdown(self, control):
        """Returns html code for a control

        Args:
            control (dict): Control object for a dropdown list

        Returns:
            str: Html code for configured dropdown
        """
        options = control.get('options')
        dropdown_list = []
        for _, value in options.items():
            dropdown_list.append(value)

        default_option = control.get('default')
        default_value = options.get(default_option).get('value')

        return html.Div(dcc.Dropdown(
                        options=dropdown_list,
                        id=control.get('id'),
                        value=default_value,
                        clearable=False
                        ),
                        className='control-dropdown'
                        )

    def control_number(self, control):

        options = control.get('options')
        minimum = options.get('minimum')
        maximum = options.get('maximum')

        default_value = control.get('default')

        return html.Div(dcc.Input(
                        id=control.get('id'),
                        type='number',
                        inputMode='numeric',
                        min=minimum,
                        max=maximum,
                        placeholder=default_value,
                        value=default_value,
                        debounce=True
                        ),
                        className='control-number'
                        )

    def fetch_dropdown_label_value(self, id, id_match, match_value):
        control = self.controls.get(id, None)
        match_control = self.controls.get(id_match, None)
        label = None
        value = None

        for _, match_option in match_control.get('options').items():
            if match_option.get('value') == match_value:
                label = match_option.get('label')
                for _, option in control.get('options').items():
                    if option.get('label') == label:
                        value = option.get('value')
                        break

        return label, value
