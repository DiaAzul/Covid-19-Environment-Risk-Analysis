""" The Appdecoration file contains page decorators for the theme"""

# import dash
import dash_core_components as dcc
import dash_html_components as html


class Appdecoration:
    """This class contains page decorators to theme the app
    Methods should be defined as staticMethods.
    """

    @staticmethod
    def page_header(logo):
        """Provide a banner at the top of the page"""
        return html.Div([
<<<<<<< HEAD
            html.Img(src=logo, width=200, height=60, className='logo'),
            html.H1('Environment risk assessment', className='header-title')
            ],
            className='header'
=======
            html.Img(src=logo, width=200, height=60, style={'float': 'right', 'vertical-align': 'middle'}),  # noqa:E501
            html.H1('Environment risk assessment', style={'position': 'relative', 'margin': '10px'})  # noqa:E501
            ], style={
                'position': 'fixed',
                'width': '100%',
                'top': '0',
                'left': '0',
                # Set z-index above plotly objects which are at 1001-1002
                'z-index': '1005',
                'background-color': 'gainsboro'}
>>>>>>> 9b7f1466b96f73f2d890152c59bb8c2c762512c7
            )

    @staticmethod
    def page_footer():
        """Provide a banner at the top of the page"""
        return html.Div([
<<<<<<< HEAD
            dcc.Markdown("""** Copyright 2020 Tanzo Creative Ltd **""", className='copyright')
            ],
            className='footer'
=======
            dcc.Markdown("""** Copyright 2020 Tanzo Creative Ltd **""", style={'float': 'right', 'position': 'relative', 'margin': '10px'})  # noqa:E501
            ], style={
                'background-color': 'gainsboro',
                'height': '40px'}
>>>>>>> 9b7f1466b96f73f2d890152c59bb8c2c762512c7
            )
