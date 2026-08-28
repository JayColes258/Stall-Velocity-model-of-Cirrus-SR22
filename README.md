This project investigated the factors governing the stall speed of a Cirrus SR22, beginning with the fundamental relationship

\[
V_S = \sqrt{\frac{2W}{\rho S C_{L,\max}}}.
\]

The initial model was extended to account for centre-of-gravity position, wing pitching moment, engine thrust, and propeller efficiency. An ISA atmospheric model was also implemented to calculate temperature, pressure, and air density as functions of altitude, allowing the stall condition to be expressed in terms of true airspeed (TAS), calibrated airspeed (CAS), and Mach number.

At the baseline sea-level condition of \(W = 3400\,\mathrm{lbf}\), \(C_{L,\max} = 1.45\), and the forward CG position, the model predicted a stall speed of \(68.40\,\mathrm{kt}\) TAS and \(68.39\,\mathrm{kt}\) CAS, corresponding to a Mach number of \(0.103\).

A normalised sensitivity analysis was then performed to quantify the influence of individual model parameters. Aircraft weight produced a sensitivity coefficient of

\[
S_W = +0.540,
\]

indicating that a \(10\%\) increase in aircraft weight resulted in approximately a \(5.4\%\) increase in predicted stall speed. Maximum lift coefficient produced a sensitivity coefficient of

\[
S_{C_{L,\max}} = -0.503,
\]

meaning that a \(10\%\) increase in \(C_{L,\max}\) resulted in approximately a \(5.0\%\) decrease in predicted stall speed.

These results are consistent with the theoretical dependence

\[
V_S \propto \sqrt{\frac{W}{C_{L,\max}}},
\]

for which the expected normalised sensitivities are approximately

\[
S_W = +0.5,
\qquad
S_{C_{L,\max}} = -0.5.
\]

The remaining parameters had substantially smaller effects under the assumptions of the model. Propeller efficiency had a normalised sensitivity of approximately

\[
S_{\eta_p} = -0.045,
\]

while the wing pitching-moment coefficient produced a sensitivity of approximately

\[
S_{C_{m,W}} = 0.006.
\]

The effect of centre-of-gravity position was also investigated. Moving the CG from its forward to aft limit reduced the predicted stall speed from

\[
68.40\,\mathrm{kt}
\]

to

\[
67.32\,\mathrm{kt},
\]

corresponding to a reduction of approximately

\[
1.57\%.
\]

The analysis therefore identified aircraft weight and maximum lift coefficient as the dominant parameters governing stall speed within the investigated conditions. Centre-of-gravity position produced a smaller but measurable effect, while pitching-moment coefficient and propeller efficiency produced comparatively small changes within the assumptions of the model.
