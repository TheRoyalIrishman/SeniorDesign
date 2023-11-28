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

# tomorrow = datetime.date.today() 


# temp value for now - this is Cincinnati (39.10 N, 84.51 W, 482 feet above sea level)
rocketEnvironment = Environment(
    latitude = 39.1328,
    longitude = -84.5207,
    elevation = 229 # currently set to 229 meters at Cam's house
)

rocketEnvironment.set_date((tomorrow.year, tomorrow.month, tomorrow.day), "UTC")

rocketEnvironment.set_atmospheric_model(type = "Forecast", file = "GFS")

# rocketEnvironment.info()

rocketRadius = 0.06985 #m
nozzleLength = 0.06499999999999995

M2500 = SolidMotor(
    thrust_source = "AeroTech_M2500T.eng",
    burn_time = 3.9, # will burn for 3.9 seconds
    grain_number = 5, # num grains
    grain_separation = 0.005, # this is just a BS temp value for now - need to actually find it

    # grain_density = 2000.087206, 
    # grain_outer_radius= rocketRadius-0.0145, # this is just a BS temp value for now - need to actually find it
    # grain_initial_inner_radius = 0.0001, # this is just a BS temp value for now - need to actually find it
    
    grain_density = 1625.087206, 
    grain_outer_radius= 0.085471/2, # m
    grain_initial_inner_radius = 0.083058/2, # m
    
    grain_initial_height = 0.1524,
    nozzle_radius = 46.5 / 2000, # this is just a BS temp value for now - need to actually find it
    throat_radius = 17.4 / 2000, # this is just a BS temp value for now - need to actually find it
    interpolation_method="linear",
    dry_mass = 3.353, #mass of motor without propellant # kg
    dry_inertia = (0.125, 0.125, 0.05),
    # grains_center_of_mass_position = 0.3755,
    grains_center_of_mass_position =  0.0762,
    center_of_dry_mass_position = 0.3755
)

M2500.info()

m2500Rocket = Rocket(
    radius = rocketRadius, 
    # mass = 14.661, # this is mass without motors
    mass = 16.301, #mass no motor
    inertia = [6.8449960074, 6.850778567, 0.0556129471, -0.000050334, -0.0156079359, -0.0007228199],
    power_on_drag = "drag_power_on.csv",
    power_off_drag = "drag_power_off.csv",
    center_of_mass_without_motor = 2.09,#m 
    coordinate_system_orientation = "nose_to_tail"
)

#Tip of cone to butt of motor = 3.225 m
m2500Rocket.add_motor(M2500, position = 3.225+nozzleLength)
# m2500Rocket.add_tail(top_radius =  rocketRadius, bottom_radius = 0.0001, length =0.00001, position = 3.225)

m2500Rocket.set_rail_buttons(upper_button_position = 2.451, lower_button_position = 3.213)

rocketNoseCone = m2500Rocket.add_nose(length=0.559, kind="Ogive", position = 0) 


rocketFins = m2500Rocket.add_trapezoidal_fins(
    n = 4,
    root_chord = 0.205,
    tip_chord = 0.0748,
    span = 0.114,
    cant_angle = 0,
    radius = None,
    airfoil = None,
    position =  3.021 # position is BS value - needs to be fixed
)

# m2500Rocket.draw()
# m2500Rocket.all_info()

def drogueTrigger(p, h, y):
    # p = pressure
    # y = [x, y, z, vx, vy, vz, e0, e1, e2, e3, w1, w2, w3]
    # activate drogue when vz < 0 m/s
    
    return True if y[5] < 0 else False
    
def mainTrigger(p, h, y):
    # p = pressure
    # y = [x, y, z, vx, vy, vz, e0, e1, e2, e3, w1, w2, w3]
    # activate main when vz < 0 m/s and z < 800 + 1400 m (+1400 due to surface elevation).
    return True if y[5] < 0 and y[2] < 243.84 else False

mainParachute = m2500Rocket.add_parachute(
    name = "drougeParachute",
    cd_s = 1.340 * 1.32,
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

# testFlight.export_kml(
#     file_name = "exportRocketTrajectory.kml",
#     extrude = True,
#     altitude_mode = "relativetoground"
# )