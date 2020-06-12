""" The apptext file contains descriptive texts use within the app"""

import dash
import dash_core_components as dcc
import dash_html_components as html


class Apptext:
    """This class contains text blocks used within the app to facilitate
    management and editing of text without having to impact the core app code.
    Methods should be defined as staticMethods.
    """   

    @staticmethod
    def introduction_heading():
        return html.H1("Introduction")

    @staticmethod
    def introduction_text():
        return dcc.Markdown("""
    There is a risk of infectious disease transmission within indoor environments. Infectious diseases may be transmitted through multiple mechanisms including touch, bodily fluids, formites, respiritory droplets (spew or aerosol). This risk assessment tool considers transmission within an indoor microenvironment through respiritory droplets, such as may occur in the transmission of Covid-19.

    The factors  affect the number of people who might be infected include:
    * the emission rate of the infected individual
    * the ventilation of the indoor environment
    * the inhilation rate of susceptible individuals
    * the separation distance between infected and susceptible individuals
    * the duration that infectious and susceptible people are in the environment.

    The criteria for assessing the risk are set out below, along with a charting tool to visually represent the risk.    
    """)

