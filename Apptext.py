""" The apptext file contains descriptive texts use within the app"""

# import dash
import dash_core_components as dcc
import dash_html_components as html
import yaml


class Apptext:
    """This class contains text blocks used within the app to facilitate
    management and editing of text without having to impact the core app code.
    Methods should be defined as staticMethods."""

    def __init__(self, path):
        with open(path) as file:
            self.content = yaml.load(file, Loader=yaml.FullLoader)


    def introduction_heading(self):
        header_text = self.content.get('introduction').get('heading')
        return html.H3(header_text)


    def introduction_text(self):
        return dcc.Markdown(self.content.get('introduction').get('text'), className='introduction-text')


    def heading(self, section_id):
        return html.H3(self.content.get(section_id).get('heading'))


    def text(self, section_id):
        return dcc.Markdown(self.content.get(section_id).get('text'), className='app-text-body')
    
