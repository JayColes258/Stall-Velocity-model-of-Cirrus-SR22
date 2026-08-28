This project was built around the fundamental stall-speed relationship,

$$
V_S = \sqrt{\frac{2W}{\rho S C_{L,\max}}}
$$

with the aim of investigating which aircraft and aerodynamic parameters have the greatest influence on stall speed.

I developed a Python model of the Cirrus SR22 that extended the basic stall-speed equation to account for centre-of-gravity position, wing pitching moment, engine thrust and propeller efficiency. The model also incorporated an ISA atmospheric model to calculate changes in temperature, pressure and air density with altitude, allowing stall speed to be expressed in terms of TAS, CAS and Mach number.

I then performed a sensitivity analysis by varying key model parameters and measuring their effect on predicted stall speed. The results showed that aircraft weight and maximum lift coefficient, \(C_{L,\max}\), had particularly strong effects on stall speed, while parameters such as propeller efficiency produced comparatively smaller changes within the assumptions of the model.

