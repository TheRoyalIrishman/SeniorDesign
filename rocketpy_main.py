from rocketpy import Environment, SolidMotor, Rocket, Flight
import datetime

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

tomorrow = datetime.date.today() + datetime.timedelta(days=1)

# temp value for now - this is Cincinnati (39.10 N, 84.51 W, 482 feet above sea level)
rocketEnvironment = Environment(latitude=39.10, longitude=84.51, elevation=482)

rocketEnvironment.set_date((tomorrow.year, tomorrow.month, tomorrow.day), timezone="EST")

rocketEnvironment.set_atmospheric_model(type="Forecast", file="GFS")

# rocketEnvironment.info()