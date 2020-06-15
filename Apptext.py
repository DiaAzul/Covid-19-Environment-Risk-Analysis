""" The apptext file contains descriptive texts use within the app"""

# import dash
import dash_core_components as dcc
import dash_html_components as html
import yaml


class Apptext:
    """This class contains text blocks used within the app to facilitate
    management and editing of text without having to impact the core app code.
<<<<<<< HEAD
    Methods should be defined as staticMethods."""
=======
    Methods should be defined as staticMethods.
    """
>>>>>>> 9b7f1466b96f73f2d890152c59bb8c2c762512c7

    def __init__(self, path):
        with open(path) as file:
            self.content = yaml.load(file, Loader=yaml.FullLoader)


    def introduction_heading(self):
        header_text = self.content.get('introduction').get('heading')
        return html.H3(header_text)

<<<<<<< HEAD
=======
    The criteria for assessing the risk are set out below, along with a charting tool to visually represent the risk.
    """)  # noqa:E501
>>>>>>> 9b7f1466b96f73f2d890152c59bb8c2c762512c7

    def introduction_text(self):
        return dcc.Markdown(self.content.get('introduction').get('text'), className='introduction-text')


<<<<<<< HEAD
    def heading(self, section_id):
        return html.H3(self.content.get(section_id).get('heading'))
=======
From microenvironment modelling the attack rate for a supermarket with mechanical ventilation is 0.31%. Note that this is not the probability of becoming infected. To determine that the prbability of infection, the attack rate needs to be multiplied by the probability of an infectious person visiting the same supermarket in the same time frame - a function of background prevalence rate and probability that an infectous person will visit the supermarket.
* Exhalation rate: Standing, no mask
* Ventilation: Length (30m) x width (20m) x heaight (3m), Air Change Per Hour (1.1)
* Distance: 60 customers at any one time
* Inhalation rate: standing, no mask
* Time: 30 minutes
        """, style={'word-wrap': 'break-word'})   # noqa:E501
>>>>>>> 9b7f1466b96f73f2d890152c59bb8c2c762512c7


<<<<<<< HEAD
    def text(self, section_id):
        return dcc.Markdown(self.content.get(section_id).get('text'), className='app-text-body')
    
=======
    @staticmethod
    def exhalation_rate_text():
        return dcc.Markdown("""Respiritory droplets are emitted from an infectuous person as they breath. Empidemiologists use the term quanta to measure the amount of virus transmitted. One quanta is the amount of virus required to infect a person. This measure, whilst abstract, is used to estimate the amount of virus exhaled by an infectuous person, transported through the environment, then inhaled by a susceptible person.

The emission rate, is depdenent upon the amount of virus load present within the persons respiritory system, and the volume of air emitted with each breath. Viral load can vary over the infectuous period. The amount used in the risk assessment assumes an asymptomatic person. An average quanta emission rate is calculated across three activities.

The amount of exhaled virus may be reduced if the infectuous person wears a face mask. A reudction in quanta emitted is selectable, including no mask (baseline), cloth mask (home made), surgical mask and N95 mask.
        """)   # noqa:E501

    @staticmethod
    def ventilation_heading():
        return html.H2("Ventilation")

    @staticmethod
    def ventilation_text():
        return dcc.Markdown("""Within an indoor environment, aerosolised virus particles will accumulate in the air over a period of time until removed. Virus particles may be removed either by falling to the floor due to gravity or air exchange with the outside environment. Virus particles can remain suspended in the air for hours, and it is assumed that the primary mode for removing particles from the environment is ventilation.

Ventilation may be natural or mechanical. Natural ventilation is the natural flow of air between the inside and outside environments resulting from openings in the buildings structure (e.g. doors, windows, ventilation slots). Building regulations aimed at improving thermal efficiency of housing reduces the amount of natural ventilation; this may increase the risk of that infectious particles build up in the environment. Mechanical ventilation uses machinery to exchange air within the buildng. This may be required in environments where there are large numbers of people, heat generating equipment, air-borne pollutants, etc.

The concentration of virus particles will be slower in larger buildings with greater air volume, though these spaces may have larger numbers of susceptible people who could become infected.

Ideally, all spaces should be large and well ventilated to minimise the build up of aerosolised particles.

Note: Outdoor spaces may be considered indoor spaces when there are temperature inversions (e.g. above crowds) which trap aerosols at or near ground level, and when there is little background air movement to disperse any aerosol.

Air exchange rates (Air Changes Per Hour - ACH) can vary significantly depending upon the age of the property, property design, maintenance and presence of mechanical ventilation. Guidline air exchange rates for the risk assessment see (https://www.vent-axia.com/sites/default/files/Ventilation%20Design%20Guidelines%202.pdf) for a more extensive list). Note that these are guidelines for effective ventilation many properties will diverge from these values and will have worse or better ventilation which will have a significant impact on infection rates.
* Natural ventilation (no windows, doors open): 0.3 (Building regulation recommend 0.3 l/s/m^2 which is 0.3 ACH but can be higher if doors and windows open, increasing to 0.5 or more depending on external wind blowing air through)
* Natural ventilation (windows/door, one side): 0.67
* Natural ventilation (windows/doors two side): 1.0
* Offices: 8 (range 6-10)
* Restaurants: 10 (range 8-12)
* Cafes and coffee bars: 11 (range 10-12)
* Gymnasium: 6 (minimum)
* Pubs: 12 (minimum)
* Schoolrooms: 6 (range 5-7)
* Shops and supermarkets: 11 (range 8-15)
* Conference rooms: 10 (range 8-12)
        """)  # noqa:E501

    @staticmethod
    def distance_heading():
        return html.H2("Distance")

    @staticmethod
    def distance_text():
        return dcc.Markdown("""The risk of infectious disease transmission increases the closer a susceptible peron is to an infected person. The calculation of this risk for all situations in a specific situation as it depends on the airflow between the infected and susceptible person. For instance the susceptible person's body heat might be sufficient to generate an updraft which pushes infectious particles above their head; an infectious person talking loudly, without a mask, might generate a plume of spew which travels several meters in still air; and, someone wearing a mask might cause particles to be emitted sideways rather than straight ahead. Even within a building, the arrangement of ventilation, heating, obstacles and natural airflow may case particles to move in unpredictable directions and over significant distances.

The model assumes that people are equally distributed over the surface area of the microenvironment, and that the air is well enough mixed that the risk of inhalation of an infectious particle is equal for all people at all times. Therefore, the number of potential people infected is related to the density of people within the microenvironment at any one time (other paramters in the risk assessment showing the impact of other factors on the risk of people being infected)
    """)   # noqa:E501

    @staticmethod
    def inhalation_rate_heading():
        return html.H2("Inhalation")

    @staticmethod
    def inhalation_rate_text():
        return dcc.Markdown("""Inhalation by susceptible people is the reverse of exhalation by infected people. The risk of infection is driven by the inhalation rate (m3 h-1) as modified by any face coverings. With the exception of clinical personal protective equipment the impact of face coverings is considered low. Note, the model excludes risk associated with infection resulting from deposition of infectious droplets on non respiritory mucosal surfaces (e.g. eye).

|    Activity      | Inhalation rate  (m3 h-1)     |
|:--------------:  |:-------------------------:    |
|     Resting      |            0.36               |
|    Standing      |            0.54               |
| Light Exercise   |            1.16               |
        """, style={'word-wrap': 'break-word'})  # noqa:E501

    @staticmethod
    def time_heading():
        return html.H2("Time")

    @staticmethod
    def time_text():
        return dcc.Markdown("""The final component of the risk assessment is time, both the amount of time that infectious and susceptible people spend in the environment. The longer the infecious person is in the environment, the greater the concentration build up of infectious material. The longer the susceptible person is in the environment the more chance they have of becoming infected. If the susceptible person arrives some time after the infectious person has left then quanta concentrations will have reduced due to the diluting effect of ventilation.

The baseline time assumes that infectious and susceptible people are in the microenvironment at the same time and for an amount of time that would create an X% risk of the susceptible person becoming infected.
    """)  # noqa:E501
>>>>>>> 9b7f1466b96f73f2d890152c59bb8c2c762512c7
