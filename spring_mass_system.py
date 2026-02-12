"""
Spring-Mass System with Viscous Damping
Euler integration + static plots for underdamped, critical, and overdamped regimes.

Berkay Yılmaz — brky.ai
"""
import numpy as np
import matplotlib.pyplot as plt
from dataclasses import dataclass


@dataclass
class Spring:
    k: float              # spring constant [N/m]
    natural_length: float  # rest length [m]

    def force(self, displacement: float) -> float:
        """Restoring force relative to equilibrium (gravity already factored out)."""
        return -self.k * displacement


@dataclass
class Damper:
    c: float  # damping coefficient [N·s/m]

    def force(self, velocity: float) -> float:
        return -self.c * velocity


@dataclass
class SpringMassSystem:
    mass: float
    spring: Spring
    damper: Damper

    @property
    def omega0(self) -> float:
        return np.sqrt(self.spring.k / self.mass)

    @property
    def zeta(self) -> float:
        return self.damper.c / (2 * np.sqrt(self.spring.k * self.mass))

    def acceleration(self, x: float, v: float) -> float:
        net_force = self.spring.force(x) + self.damper.force(v)
        return net_force / self.mass

    def solve_euler(self, x0: float, v0: float, t_span: tuple, dt: float):
        """Forward Euler integration for damped harmonic oscillator (relative to equilibrium)."""
        num_steps = int((t_span[1] - t_span[0]) / dt)
        t = np.linspace(t_span[0], t_span[1], num_steps)
        x = np.zeros(num_steps)
        v = np.zeros(num_steps)
        a = np.zeros(num_steps)

        x[0], v[0] = x0, v0

        for i in range(1, num_steps):
            a[i - 1] = self.acceleration(x[i - 1], v[i - 1])
            v[i] = v[i - 1] + a[i - 1] * dt
            x[i] = x[i - 1] + v[i - 1] * dt

        # last acceleration value (original code left this as zero)
        a[-1] = self.acceleration(x[-1], v[-1])

        pe = 0.5 * self.spring.k * x ** 2
        ke = 0.5 * self.mass * v ** 2
        te = pe + ke

        # cumulative energy dissipated by damper
        power_loss = self.damper.c * v ** 2
        energy_loss = np.cumsum(power_loss) * dt

        return t, x, v, a, pe, ke, te, energy_loss


def plot_motion(t, x, v, a, pe, ke, te, energy_loss):
    fig, axs = plt.subplots(3, 2, figsize=(14, 12))

    axs[0, 0].plot(t, x, 'r-')
    axs[0, 0].set_xlabel('Time (s)')
    axs[0, 0].set_ylabel('Displacement (m)')
    axs[0, 0].set_title('Displacement vs Time')

    axs[0, 1].plot(x, v, 'b-')
    axs[0, 1].set_xlabel('Displacement (m)')
    axs[0, 1].set_ylabel('Velocity (m/s)')
    axs[0, 1].set_title('Phase Space')

    axs[1, 0].plot(t, v, 'b-', label='Velocity')
    ax2 = axs[1, 0].twinx()
    ax2.plot(t, a, 'g-', label='Acceleration')
    axs[1, 0].set_xlabel('Time (s)')
    axs[1, 0].set_ylabel('Velocity (m/s)')
    ax2.set_ylabel('Acceleration (m/s²)')
    axs[1, 0].set_title('Velocity & Acceleration')
    axs[1, 0].legend(loc='upper left')
    ax2.legend(loc='upper right')

    axs[1, 1].plot(t, pe, 'm-', label='PE (elastic)')
    axs[1, 1].plot(t, ke, 'c-', label='KE')
    axs[1, 1].set_xlabel('Time (s)')
    axs[1, 1].set_ylabel('Energy (J)')
    axs[1, 1].set_title('Potential & Kinetic Energy')
    axs[1, 1].legend()

    axs[2, 0].plot(t, energy_loss, 'y-')
    axs[2, 0].set_xlabel('Time (s)')
    axs[2, 0].set_ylabel('Cumulative Loss (J)')
    axs[2, 0].set_title('Energy Dissipated by Damper')

    axs[2, 1].plot(t, te, 'k-', label='Total Mechanical')
    axs[2, 1].set_xlabel('Time (s)')
    axs[2, 1].set_ylabel('Energy (J)')
    axs[2, 1].set_title('Total Energy vs Time')
    axs[2, 1].legend()

    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    system = SpringMassSystem(
        mass=0.65,
        spring=Spring(k=5.5, natural_length=0.3),
        damper=Damper(c=1.0),
    )
    t, x, v, a, pe, ke, te, eloss = system.solve_euler(0.0, 0.0, [0, 10], 0.01)
    plot_motion(t, x, v, a, pe, ke, te, eloss)
