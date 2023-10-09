from rocketpy import Environment, SolidMotor, Rocket, Flight
from datetime import datetime
from pytz import timezone

"""

DOCUMENTATION RESOURCES:

Generic page
https://docs.rocketpy.org/en/latest/notebooks/getting_started.html

On how to use the Enviornment class
https://docs.rocketpy.org/en/latest/notebooks/environment/environment_class_usage.html

On how to use the SolidMotor class
https://docs.rocketpy.org/en/latest/user/motors/solidmotor.html

On how to use the Rocket class
https://docs.rocketpy.org/en/latest/user/rocket.html

Notes on position & coordinate systems
https://docs.rocketpy.org/en/latest/user/positions.html

On how to define a parachute
https://docs.rocketpy.org/en/latest/user/rocket.html#adding-parachutes


"""
easternTimeZone = timezone('EST')

datetime.now(easternTimeZone)