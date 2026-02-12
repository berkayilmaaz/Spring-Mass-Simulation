# Damped Spring-Mass Simulation

<p align="center">
<img src="assets/brky-logo.png" height="120">
</p>

<p align="center">
🚀 <b>For a more detailed analysis and interactive visualizations, visit the project website:</b>
<a href="https://springmass.brky.ai"><b>springmass.brky.ai</b></a>
</p>

![Python](https://img.shields.io/badge/Python-3.10%2B-3776ab?logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Stable-brightgreen)

---

A numerical and analytical study of the damped harmonic oscillator, comparing forward Euler integration with exact solutions across three damping regimes: underdamped, critically damped, and overdamped.

## Physics

The system follows the equation of motion:

```
m·ẍ + c·ẋ + k·x = 0
```

where `x` is displacement from equilibrium, `m` is mass, `c` is the damping coefficient, and `k` is the spring constant. Displacement is measured relative to the static equilibrium position, which eliminates gravity from both the EOM and energy expressions.

The damping ratio `ζ = c / (2√(km))` determines the qualitative behavior:

| Regime | Condition | Behavior |
|--------|-----------|----------|
| Underdamped | ζ < 1 | Oscillatory decay with envelope e^(−ζω₀t) |
| Critically damped | ζ = 1 | Fastest aperiodic return to equilibrium |
| Overdamped | ζ > 1 | Sluggish exponential settling |

## Numerical Method

Forward Euler integration with first-order explicit scheme:

```
v[n+1] = v[n] + (−k·x[n] − c·v[n]) / m · Δt
x[n+1] = x[n] + v[n] · Δt
```

Stability condition: `Δt < 2 / (ζω₀)`.

## Default Parameters

| Symbol | Value | Description |
|--------|-------|-------------|
| m | 0.65 kg | Mass |
| k | 5.5 N/m | Spring constant |
| c | 0.8 N·s/m | Damping coefficient |
| x₀ | 0.15 m | Initial displacement |
| ẋ₀ | 0.0 m/s | Initial velocity |
| Δt | 0.01 s | Time step |

Computed: ω₀ ≈ 2.91 rad/s, ζ ≈ 0.212 (underdamped).

## Project Structure

```
.
├── spring_mass_system.py   # physics engine + static plots
├── animate_system.py       # matplotlib animation (spring visualization)
├── requirements.txt        # numpy, matplotlib, scipy
├── README.md
├── assets/
│   └── brky-logo.png
├── animation_1.gif
└── animation_2.gif
```

## Usage

```bash
git clone https://github.com/berkayilmaaz/Spring-Mass-Simulation.git
cd Spring-Mass-Simulation
pip install -r requirements.txt
python spring_mass_system.py
python animate_system.py
```


## Author

**Berkay Yılmaz** — Physics, Marmara University  
[brky.ai](https://brky.ai) · [contact@brky.ai](mailto:contact@brky.ai)
