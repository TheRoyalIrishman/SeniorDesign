from rocketpy import Environment, SolidMotor, Rocket, Flight
import datetime

import matplotlib.pyplot as plt
plt.close("all")

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

# temp value for now - this is launch site
rocketEnvironment = Environment(
    latitude = 39.853611,
    longitude = -83.655556,
    elevation = 392.42
)

rocketEnvironment.set_date((tomorrow.year, tomorrow.month, tomorrow.day), "UTC")
rocketEnvironment.set_atmospheric_model(type = "Forecast", file = "GFS")


rocketEnvironment.info()

rocketRadius = 0.140335/2 #m
#nozzleLength = 0.1048766

M2500 = SolidMotor(
    thrust_source = "AeroTech_M2500T.eng",
    burn_time = 3.9, # will burn for 3.9 seconds
    grain_number = 4, # num grains
    grain_separation = 0.005, # this is just a BS temp value for now - need to actually find it

    # grain_density = 2000.087206, 
    # grain_outer_radius= rocketRadius-0.0145, # this is just a BS temp value for now - need to actually find it
    # grain_initial_inner_radius = 0.0001, # this is just a BS temp value for now - need to actually find it
    
    grain_density = 1600,
    grain_outer_radius= 0.085471/2, # m
    grain_initial_inner_radius = 0.028575/2, # m
    grain_initial_height = 0.1524,
    nozzle_radius = 0 / 2000, # this is just a BS temp value for now - need to actually find it
    throat_radius = 0 / 2000, # this is just a BS temp value for now - need to actually find it
    interpolation_method="linear",
    dry_mass = 3.354, #mass of motor without propellant # kg THIS IS THE CASING MASS
    dry_inertia = (0.1642, 0.1642, 0.02969),
    # grains_center_of_mass_position = 0.3755,
    grains_center_of_mass_position = 0.3755,
    center_of_dry_mass_position = 0.3755
)

M2500.info()

m2500Rocket = Rocket(
    radius = rocketRadius,
    mass = 15.9891, #mass no propellant or casing
    inertia = [6.8449960074, 6.850778567, 0.0556129471, -0.000050334, -0.0156079359, -0.0007228199],
    power_on_drag = "drag_power_on.csv",
    power_off_drag = "drag_power_off.csv",
    center_of_mass_without_motor = 1.867,#m - with casing
    coordinate_system_orientation = "nose_to_tail"
)

#Tip of cone to butt of motor = 3.225 m
m2500Rocket.add_motor(M2500, position = 3.4544)
# m2500Rocket.add_tail(top_radius =  rocketRadius, bottom_radius = 0.0001, length =0.00001, position = 3.225)

m2500Rocket.set_rail_buttons(upper_button_position = 2.667, lower_button_position = 3.4544)

rocketNoseCone = m2500Rocket.add_nose(length=0.76835, kind="von karman", position = 0)


rocketFins = m2500Rocket.add_trapezoidal_fins(
    n = 4,
    root_chord = 0.2049526,
    tip_chord = 0.0748,
    span = 0.11,
    cant_angle = 0,
    sweep_length=.0762,
    radius = None,
    airfoil = None,
    position = 3.2494474
)

m2500Rocket.draw()
m2500Rocket.all_info()

def drogueTrigger(p, h, y):
    # p = pressure
    # y = [x, y, z, vx, vy, vz, e0, e1, e2, e3, w1, w2, w3]
    # activate drogue when vz < 0 m/s

    return True if y[5] < 0 else False

def mainTrigger(p, h, y):
    # p = pressure
    # y = [x, y, z, vx, vy, vz, e0, e1, e2, e3, w1, w2, w3]
    # activate main when vz < 0 m/s and z < 800 + 1400 m (+1400 due to surface elevation).
    return True if y[5] < 0 and y[2] < 213.36 else False

drogueParachute = m2500Rocket.add_parachute(
    name = "drougeParachute",
    cd_s = 0.8 * 1.32,
    trigger = drogueTrigger,
    sampling_rate = 105,
    lag = 3.0,
    noise = (0, 8.3, 0.5)
)

mainParachute = m2500Rocket.add_parachute(
    name = "mainParachute",
    cd_s = 1.260 * 5.29547,
    trigger = mainTrigger,
    sampling_rate = 105,
    lag = 1.0,
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
     file_name = "exportRocketTrajectory.kml",
     extrude = True,
     altitude_mode = "relativetoground"
 )