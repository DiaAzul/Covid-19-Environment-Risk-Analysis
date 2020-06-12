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
            html.Img(src=logo, width=200, height=60, style={'float':'right', 'vertical-align':'middle'}),
            html.H1('Environment risk assessment', style={'position':'relative', 'margin':'10px'})
            ], style={
                'position':'fixed',
                'width': '100%',
                'top': '0',
                'left': '0',
                # Set z-index above plotly objects which are at 1001-1002
                'z-index': '1005',
                'background-color': 'gainsboro'}
            )

    @staticmethod
    def page_footer():
        """Provide a banner at the top of the page"""  
        return html.Div([
            dcc.Markdown("""** Copyright 2020 Tanzo Creative Ltd **""", style={'float':'right', 'position':'relative', 'margin':'10px'})
            ], style={
                'background-color': 'gainsboro',
                #'vertical-align': 'middle',
                #'text-align':'right',
                'height':'40px'}
            )



