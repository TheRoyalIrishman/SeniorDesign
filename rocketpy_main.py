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
    grain_outer_radius= 88 / 2000, # this is just a BS temp value for now - need to actually find it
    grain_initial_inner_radius = 25 / 2000, # this is just a BS temp value for now - need to actually find it
    grain_initial_height = 0.150368,
    nozzle_radius = 46.5 / 2000, # this is just a BS temp value for now - need to actually find it
    throat_radius = 17.4 / 2000, # this is just a BS temp value for now - need to actually find it
    interpolation_method="linear",
    dry_mass = 2.4494, # kg
    dry_inertia = (0.125, 0.125, 0.05),
    grains_center_of_mass_position = 25 / 1000,
    center_of_dry_mass_position = 25 / 1000
)

M2500.info()

m2500Rocket = Rocket(
    radius = 277 / 2000,
    mass = 14.661, # this is mass without motors
    inertia=[6.8449960074, 6.850778567, 0.0556129471, -0.000050334, -0.0156079359, -0.0007228199],
    power_on_drag="drag_burn_on.csv",
    power_off_drag="drag_burn_off.csv",
    center_of_mass_without_motor = 137 / 2000
)

m2500Rocket.add_motor(M2500, position = 0)

m2500Rocket.set_rail_buttons(upper_button_position = -0.62, lower_button_position = -0.96)

# length value and distance to CM is temp - need to fix later
rocketNoseCone = m2500Rocket.add_nose(length=0.533, kind="ogive", position = 0) # position is BS value - needs to be fixed

# these are all temp BS values - will fix later once I've gotten the info from the rocket design team
rocketFins = m2500Rocket.add_trapezoidal_fins(
    n=4,
    root_chord=0.382,
    tip_chord=0.104,
    span=0.202,
    cant_angle=0,
    radius=None,
    airfoil=None,
    position = 0 # position is BS value - needs to be fixed
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
    name = "MainParachute",
    cd_s = 4.078,
    trigger = drogueTrigger,
    sampling_rate = 105,
    lag = 1.5,
    noise = (0, 8.3, 0.5)
)

testFlight = Flight(
    rocket = m2500Rocket,
    environment = rocketEnvironment,
    inclination = 90,
    rail_length = 4.88,
    heading = 0
)

testFlight.all_info()

testFlight.export_kml(
    fileName = "exportRocketTrajectory.kml",
    extrude = True,
    altitude_mode = "relativetoground"
)