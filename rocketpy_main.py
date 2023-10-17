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
rocketEnvironment = Environment(
    latitude = 39.1328,
    longitude = -84.5207,
    elevation = 229 # currently set to 229 meters at Cam's house
)

rocketEnvironment.set_date((tomorrow.year, tomorrow.month, tomorrow.day), "UTC")

rocketEnvironment.set_atmospheric_model(type="Forecast", file="GFS")

rocketEnvironment.info()

M2500 = SolidMotor(
    thrust_source = "AeroTech_M2500T.eng",
    burn_time = 3.9, # will burn for 3.9 seconds
    grain_number = 5, # num grains
    grain_separation = 0.005, # this is just a BS temp value for now - need to actually find it
    grain_density = 2400, # this is just a BS temp value for now - need to actually find it
    grain_outer_radius=88 / 2000, # this is just a BS temp value for now - need to actually find it
    grain_initial_inner_radius=25/ 2000, # this is just a BS temp value for now - need to actually find it
    grain_initial_height=198 / 1000, # this is just a BS temp value for now - need to actually find it
    nozzle_radius=46.5 / 2000, # this is just a BS temp value for now - need to actually find it
    throat_radius=17.4 / 2000, # this is just a BS temp value for now - need to actually find it
    interpolation_method="linear"
)

M2500.info()

m2500Rocket = Rocket(
    motor = M2500,
    radius = 277 / 2000,
    mass=8.964, # this is just a BS temp value for now - need to actually find it
    inertiaI=5.95, # this is just a BS temp value for now - need to actually find it
    inertiaZ=0.022, # this is just a BS temp value for now - need to actually find it
    distanceRocketNozzle=-0.97, # this is just a BS temp value for now - need to actually find it
    distanceRocketPropellant=-0.372, # this is just a BS temp value for now - need to actually find it
    # put Drag On and Drag Off CSV files here - need to remember how to get ORK file to grab this info
)

m2500Rocket.set_rail_buttons([-0.62, -0.96])

# length value and distance to CM is temp - need to fix later
rocketNoseCone = m2500Rocket.add_nose(length=0.533, kind="ogive", distanceToCM=1.85)

# these are all temp BS values - will fix later once I've gotten the info from the rocket design team
rocketFins = m2500Rocket.add_trapezoidal_fins(
    n=4,
    rootChord=0.382,
    tipChord=0.104,
    span=0.202,
    distanceToCM=-0.57,
    cantAngle=0,
    radius=None,
    airfoil=None
)

m2500Rocket.all_info()

def drogueTrigger(p, y):
    # p = pressure
    # y = [x, y, z, vx, vy, vz, e0, e1, e2, e3, w1, w2, w3]
    # activate drogue when vz < 0 m/s.
    return True if y[5] < 0 else False

def mainTrigger(p, y):
    # p = pressure
    # y = [x, y, z, vx, vy, vz, e0, e1, e2, e3, w1, w2, w3]
    # activate main when vz < 0 m/s and z < 800 + 1400 m (+1400 due to surface elevation).
    return True if y[5] < 0 and y[2] < 152 + 289.4 else False

mainParachute = m2500Rocket.add_parachute(
    "MainParachute",
    # the constants are current temp values - will fix later
    CdS=0.879,
    trigger=drogueTrigger,
    samplingRate=105, # still need to ask about this
    lag=1.5, # still need to ask about this
    noise=(0, 8.3, 0.5) # still need to ask about this
)

testFlight = Flight(
    rocket = m2500Rocket,
    environment = rocketEnvironment,
    inclination = 85,
    heading = 0
)

testFlight.all_info()

testFlight.export_kml(
    fileName = "exportRocketTrajectory.kml",
    extrude = True,
    altitude_mode = "relativetoground"
)