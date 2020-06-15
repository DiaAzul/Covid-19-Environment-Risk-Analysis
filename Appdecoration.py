""" The Appdecoration file contains page decorators for the theme"""

import dash
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
            html.Img(src=logo, width=200, height=60, className='logo'),
            html.H1('Environment risk assessment', className='header-title')
            ],
            className='header'
            )

    @staticmethod
    def page_footer():
        """Provide a banner at the top of the page"""  
        return html.Div([
            dcc.Markdown("""** Copyright 2020 Tanzo Creative Ltd **""", className='copyright')
            ],
            className='footer'
            )



