## Cirrus SR22 Stall Speed Model

This project investigates the factors governing the stall speed of a Cirrus SR22, beginning with the fundamental stall-speed relationship:

$$
V_S = \sqrt{\frac{2W}{\rho S C_{L,\max}}}
$$

where:

- $V_S$ = stall speed
- $W$ = aircraft weight
- $\rho$ = air density
- $S$ = wing area
- $C_{L,\max}$ = maximum lift coefficient

The model extends this basic relationship to account for **centre-of-gravity position, wing pitching moment, engine thrust, and propeller efficiency**.

An ISA atmospheric model is also implemented to calculate temperature, pressure, air density, and local speed of sound as functions of altitude. This allows stall conditions to be evaluated in terms of **TAS, CAS, and Mach number**.

### Baseline Conditions

| Parameter | Value |
|---|---:|
| Aircraft | Cirrus SR22 |
| Weight | 3400 lbf |
| Wing area | 144.9 ft² |
| Maximum lift coefficient | 1.45 |
| Wing pitching coefficient | -0.06 |
| Propeller efficiency | 0.65 |
| Engine power | 310 bhp |
| CG position | 19.2% chord |
| Stall angle of attack | 16° |
| Altitude | 0 m |
| Air density | 1.225 kg/m³ |

The baseline model predicted:

| Output | Result |
|---|---:|
| Stall TAS | 68.40 kt |
| Stall CAS | 68.39 kt |
| Stall Mach | 0.103 |

## Sensitivity Analysis

A normalised sensitivity analysis was performed to determine which parameters have the greatest influence on predicted stall speed.

The analysis produced:

| Parameter | Normalised Sensitivity |
|---|---:|
| Weight | +0.540 |
| $C_{L,\max}$ | -0.503 |
| $C_{m,W}$ | +0.006 |
| Propeller efficiency | -0.045 |

A weight sensitivity of **+0.540** means that a 10% increase in aircraft weight produces approximately a **5.4% increase in stall speed**.

Similarly, a $C_{L,\max}$ sensitivity of **-0.503** means that a 10% increase in maximum lift coefficient produces approximately a **5.0% reduction in stall speed**.

These results closely agree with the theoretical relationship:

$$
V_S \propto \sqrt{\frac{W}{C_{L,\max}}}
$$

which predicts approximate normalised sensitivities of:

$$
S_W = +0.5
\qquad
S_{C_{L,\max}} = -0.5
$$

The model therefore reproduces the expected theoretical dependence while also accounting for additional aerodynamic and propulsion effects.

### Centre-of-Gravity Effect

The model was also evaluated across the permitted CG range.

- **Forward CG:** 68.40 kt
- **Aft CG:** 67.32 kt
- **Change:** -1.57%

Moving the CG from its forward to aft limit therefore reduced predicted stall speed by approximately **1.08 kt**.

## Key Findings

The sensitivity analysis identified **aircraft weight and maximum lift coefficient as the dominant parameters** governing stall speed.

Weight had a positive sensitivity, meaning heavier aircraft stall at higher speeds, while increasing $C_{L,\max}$ reduced the required stall speed. These numerical sensitivities closely matched the theoretical square-root dependence predicted by the fundamental stall-speed equation.

CG position produced a smaller but measurable effect, while wing pitching moment and propeller efficiency produced comparatively small changes under the assumptions of the model.

The altitude model additionally demonstrates the distinction between **true airspeed and calibrated airspeed**: as altitude increases and air density decreases, stall TAS increases while stall CAS remains approximately constant.

<img width="1759" height="927" alt="image" src="https://github.com/user-attachments/assets/2e4ade77-c153-4a6e-bba7-ff5df61114ba" />

