import numpy as np
import matplotlib.pyplot as plt

S = 144.9                          # Wing area [ft^2]
c_MGC = 3.783                      # Mean geometric chord [ft]
l_HT = 14.06                       # Horizontal tail moment arm [ft]
W = 3400                           # Gross aircraft weight [lbf]

Cm_W = -0.06                       # Wing pitching moment coefficient [-]
CL_max = 1.45                      # Maximum lift coefficient [-]

x_CG_fwd = 0.192 * c_MGC           # Forward CG position [ft]
x_CG_aft = 0.315 * c_MGC           # Aft CG position [ft]
x_n = 0.40 * c_MGC                 # Neutral point position [ft]

x_T = 5.0                          # Longitudinal thrust position [ft]
z_T = 1.0                          # Vertical thrust position [ft]

eta_p = 0.65                       # Propeller efficiency [-]
alpha = np.deg2rad(16)             # Stall angle of attack [rad]

p_0 = 101325                       # Standard sea-level pressure [Pa]
T_0 = 288.15                       # Standard sea-level temperature [K]
rho_0 = 0.002378                   # Standard sea-level density [slug/ft^3]

L = 0.0065                         # ISA temperature lapse rate [K/m]
g = 9.80665                        # Gravitational acceleration [m/s^2]
M = 0.02896968                     # Molar mass of dry air [kg/mol]
R = 8.314462618                    # Universal gas constant [J/(mol*K)]

gamma = 1.4                        # Ratio of specific heats for air [-]
R_specific = 287.05                # Specific gas constant for air [J/(kg*K)]

h = 0                              # Altitude above sea level [m]
x_CG = x_CG_fwd                    # Selected centre of gravity [ft]

P_BHP = 310                        # Engine power [BHP]

V_reference_knots = 70             # Reference stall speed from POH [knots]
V_reference = V_reference_knots * 1.68781   # Reference speed [ft/s]

q_reference = 0.5 * rho_0 * V_reference**2  # Reference dynamic pressure [lbf/ft^2]

M_W = q_reference * S * c_MGC * Cm_W        # Wing pitching moment [ft*lbf]


def atmosphere(h):
    temperature = T_0 - L * h               # Local atmospheric temperature [K]

    p = p_0 * (1 - (L * h) / T_0)**(
        (g * M) / (R * L)
    )                                        # Local atmospheric pressure [Pa]

    rho_SI = (p * M) / (R * temperature)     # Local air density [kg/m^3]

    rho = rho_SI * 0.00194032                # Local air density [slug/ft^3]

    speed_of_sound = np.sqrt(
        gamma * R_specific * temperature
    )                                        # Local speed of sound [m/s]

    return temperature, p, rho_SI, rho, speed_of_sound


def stall_speed(W, CL_max, x_CG, Cm_W, eta_p, h):

    temperature, p, rho_SI, rho, speed_of_sound = atmosphere(h)

    M_W = (
        q_reference * S * c_MGC * Cm_W
    )                                        # Wing pitching moment [ft*lbf]

    thrust = (
        eta_p * 550 * P_BHP / V_reference
    )                                        # Estimated engine thrust [lbf]

    Vs = np.sqrt(
        (2 / (rho * S * CL_max))
        * (1 - (x_CG - x_n) / l_HT)
        * (
            W
            - M_W / (l_HT - x_CG + x_n)
            - (
                (x_T * np.sin(alpha) - z_T * np.cos(alpha))
                / (l_HT - x_CG + x_n)
                + np.sin(alpha)
            ) * thrust
        )
    )                                        # Stall true airspeed [ft/s]

    Vs_TAS_knots = Vs / 1.68781              # Stall true airspeed [knots]

    Vs_CAS_knots = (
        Vs_TAS_knots * np.sqrt(rho / rho_0)
    )                                        # Approx stall calibrated airspeed [knots]

    Vs_TAS_ms = Vs * 0.3048                  # Stall true airspeed [m/s]

    mach = Vs_TAS_ms / speed_of_sound        # Mach number at stall [-]

    return Vs_TAS_knots, Vs_CAS_knots, mach


Vs_base, CAS_base, Mach_base = stall_speed(
    W,
    CL_max,
    x_CG,
    Cm_W,
    eta_p,
    h
)                                            # Baseline model result


# -------------------------------------------------------
# CG PLOT
# -------------------------------------------------------

x_CG_values = np.linspace(
    x_CG_fwd,
    x_CG_aft,
    100
)                                            # CG range [ft]

Vs_TAS_values = []
Vs_CAS_values = []

for cg in x_CG_values:

    tas, cas, mach = stall_speed(
        W,
        CL_max,
        cg,
        Cm_W,
        eta_p,
        h
    )

    Vs_TAS_values.append(tas)
    Vs_CAS_values.append(cas)

Vs_TAS_values = np.array(Vs_TAS_values)      # Stall TAS across CG range [knots]
Vs_CAS_values = np.array(Vs_CAS_values)      # Stall CAS across CG range [knots]

CG_percent = (
    x_CG_values / c_MGC
) * 100                                      # CG position [% chord]

plt.plot(
    CG_percent,
    Vs_TAS_values,
    label="TAS"
)

plt.plot(
    CG_percent,
    Vs_CAS_values,
    label="CAS"
)

plt.xlabel("CG Position (% of chord)")
plt.ylabel("Stall Speed [knots]")
plt.title(f"Stall Speed vs CG Position at {h} m")
plt.grid()
plt.legend()
plt.show()


# -------------------------------------------------------
# SENSITIVITY ANALYSIS
# -------------------------------------------------------

change = 0.10                                # Parameter perturbation = 10%


Vs_W_high = stall_speed(
    W * (1 + change),
    CL_max,
    x_CG,
    Cm_W,
    eta_p,
    h
)[0]                                        # TAS with weight increased by 10%

Vs_W_low = stall_speed(
    W * (1 - change),
    CL_max,
    x_CG,
    Cm_W,
    eta_p,
    h
)[0]                                        # TAS with weight decreased by 10%


Vs_CL_high = stall_speed(
    W,
    CL_max * (1 + change),
    x_CG,
    Cm_W,
    eta_p,
    h
)[0]                                        # TAS with CL_max increased by 10%

Vs_CL_low = stall_speed(
    W,
    CL_max * (1 - change),
    x_CG,
    Cm_W,
    eta_p,
    h
)[0]                                        # TAS with CL_max decreased by 10%


Vs_Cm_high = stall_speed(
    W,
    CL_max,
    x_CG,
    Cm_W * (1 + change),
    eta_p,
    h
)[0]                                        # TAS with Cm_W changed by +10%

Vs_Cm_low = stall_speed(
    W,
    CL_max,
    x_CG,
    Cm_W * (1 - change),
    eta_p,
    h
)[0]                                        # TAS with Cm_W changed by -10%


Vs_eta_high = stall_speed(
    W,
    CL_max,
    x_CG,
    Cm_W,
    eta_p * (1 + change),
    h
)[0]                                        # TAS with prop efficiency +10%

Vs_eta_low = stall_speed(
    W,
    CL_max,
    x_CG,
    Cm_W,
    eta_p * (1 - change),
    h
)[0]                                        # TAS with prop efficiency -10%


Vs_CG_fwd = stall_speed(
    W,
    CL_max,
    x_CG_fwd,
    Cm_W,
    eta_p,
    h
)[0]                                        # TAS at forward CG limit

Vs_CG_aft = stall_speed(
    W,
    CL_max,
    x_CG_aft,
    Cm_W,
    eta_p,
    h
)[0]                                        # TAS at aft CG limit


weight_sensitivity = (
    (Vs_W_high - Vs_W_low)
    / (2 * Vs_base * change)
)                                            # Normalised sensitivity to weight

CL_sensitivity = (
    (Vs_CL_high - Vs_CL_low)
    / (2 * Vs_base * change)
)                                            # Normalised sensitivity to CL_max

Cm_sensitivity = (
    (Vs_Cm_high - Vs_Cm_low)
    / (2 * Vs_base * change)
)                                            # Normalised sensitivity to Cm_W

eta_sensitivity = (
    (Vs_eta_high - Vs_eta_low)
    / (2 * Vs_base * change)
)                                            # Normalised sensitivity to prop efficiency

CG_effect = (
    (Vs_CG_aft - Vs_CG_fwd) / Vs_CG_fwd
) * 100                                      # Stall-speed change across certified CG range [%]


parameters = [
    "Weight",
    "CL_max",
    "Cm_W",
    "Prop efficiency"
]

sensitivities = [
    weight_sensitivity,
    CL_sensitivity,
    Cm_sensitivity,
    eta_sensitivity
]


plt.bar(
    parameters,
    sensitivities
)

plt.axhline(0)

plt.ylabel("Normalised Sensitivity")
plt.title("Sensitivity of Stall Speed to Model Parameters")

plt.xticks(rotation=20)
plt.grid(axis="y")
plt.show()


temperature, p, rho_SI, rho, speed_of_sound = atmosphere(h)

print("Baseline stall TAS:", Vs_base, "knots")
print("Baseline stall CAS:", CAS_base, "knots")
print("Mach at stall:", Mach_base)

print()
print("Weight sensitivity:", weight_sensitivity)
print("CL_max sensitivity:", CL_sensitivity)
print("Cm_W sensitivity:", Cm_sensitivity)
print("Propeller efficiency sensitivity:", eta_sensitivity)

print()
print("Forward CG stall TAS:", Vs_CG_fwd, "knots")
print("Aft CG stall TAS:", Vs_CG_aft, "knots")
print("CG effect on stall speed:", CG_effect, "%")

print()
print("Local temperature:", temperature, "K")
print("Local pressure:", p, "Pa")
print("Local air density:", rho_SI, "kg/m^3")
print("Local speed of sound:", speed_of_sound, "m/s")

altitude_values = np.linspace(0, 5000, 100)     # Altitude sweep [m]

TAS_altitude = []                               # Stall TAS values [knots]
CAS_altitude = []                               # Stall CAS values [knots]
Mach_altitude = []                              # Stall Mach values [-]

for altitude in altitude_values:

    tas, cas, mach = stall_speed(
        W,
        CL_max,
        x_CG,
        Cm_W,
        eta_p,
        altitude
    )

    TAS_altitude.append(tas)
    CAS_altitude.append(cas)
    Mach_altitude.append(mach)

TAS_altitude = np.array(TAS_altitude)            # Stall TAS across altitude range [knots]
CAS_altitude = np.array(CAS_altitude)            # Stall CAS across altitude range [knots]
Mach_altitude = np.array(Mach_altitude)          # Stall Mach across altitude range [-]

plt.plot(
    altitude_values,
    TAS_altitude,
    label="TAS"
)

plt.plot(
    altitude_values,
    CAS_altitude,
    label="CAS"
)

plt.xlabel("Altitude [m]")
plt.ylabel("Stall Speed [knots]")
plt.title("Effect of Altitude on Stall Speed")

plt.grid()
plt.legend()
plt.show()

plt.plot(
    altitude_values,
    Mach_altitude
)

plt.xlabel("Altitude [m]")
plt.ylabel("Mach Number [-]")
plt.title("Mach Number at Stall vs Altitude")

plt.grid()
plt.show()