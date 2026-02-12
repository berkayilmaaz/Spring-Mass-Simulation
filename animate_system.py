"""
Animated dashboard for the damped spring-mass system.
6-panel plot grid + live spring visualization.

Berkay Yılmaz — brky.ai
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from spring_mass_system import Spring, Damper, SpringMassSystem


def animate(i, t, x, v, a, pe, ke, energy_loss, lines, mass_circle, spring_line):
    """Frame update for FuncAnimation."""
    lines[0].set_data(t[:i + 1], x[:i + 1])
    lines[1].set_data(x[:i + 1], v[:i + 1])
    lines[2].set_data(t[:i + 1], v[:i + 1])
    lines[3].set_data(t[:i + 1], a[:i + 1])
    lines[4].set_data(t[:i + 1], pe[:i + 1])
    lines[5].set_data(t[:i + 1], ke[:i + 1])
    lines[6].set_data(t[:i + 1], energy_loss[:i + 1])
    lines[7].set_data(t[:i + 1], pe[:i + 1] + ke[:i + 1])

    mass_circle.center = (0, x[i])
    spring_line.set_data([0, 0], [0, x[i]])

    return lines + [mass_circle, spring_line]


def create_animation(t, x, v, a, pe, ke, energy_loss):
    fig = plt.figure(figsize=(14, 12))
    grid = plt.GridSpec(3, 3, fig)
    lines = []

    axs = [fig.add_subplot(grid[i, j]) for i in range(3) for j in range(2)]

    # displacement vs time
    axs[0].set_title('Displacement vs Time')
    axs[0].set_xlabel('Time (s)')
    axs[0].set_ylabel('Displacement (m)')
    axs[0].set_xlim(0, t[-1])
    axs[0].set_ylim(np.min(x), np.max(x))
    ln, = axs[0].plot([], [], 'r-', label='Displacement')
    axs[0].legend()
    lines.append(ln)

    # phase space
    axs[1].set_title('Phase Space')
    axs[1].set_xlabel('Displacement (m)')
    axs[1].set_ylabel('Velocity (m/s)')
    axs[1].set_xlim(np.min(x), np.max(x))
    axs[1].set_ylim(np.min(v), np.max(v))
    ln, = axs[1].plot([], [], 'b-', label='Phase Space')
    axs[1].legend()
    lines.append(ln)

    # velocity + acceleration (twin axes)
    axs[2].set_title('Velocity & Acceleration')
    axs[2].set_xlabel('Time (s)')
    axs[2].set_ylabel('Velocity (m/s)')
    axs[2].set_xlim(0, t[-1])
    axs[2].set_ylim(np.min(v), np.max(v))
    ln_v, = axs[2].plot([], [], 'b-', label='Velocity')
    axs[2].legend(loc='upper left')
    lines.append(ln_v)

    ax_acc = axs[2].twinx()
    ax_acc.set_ylabel('Acceleration (m/s²)', color='g')
    ax_acc.set_ylim(np.min(a), np.max(a))
    ln_a, = ax_acc.plot([], [], 'g-', label='Acceleration')
    ax_acc.legend(loc='upper right')
    lines.append(ln_a)

    # PE + KE
    axs[3].set_title('Potential & Kinetic Energy')
    axs[3].set_xlabel('Time (s)')
    axs[3].set_ylabel('Energy (J)')
    axs[3].set_xlim(0, t[-1])
    axs[3].set_ylim(0, max(np.max(pe), np.max(ke)))
    ln_pe, = axs[3].plot([], [], 'm-', label='PE')
    ln_ke, = axs[3].plot([], [], 'c-', label='KE')
    axs[3].legend()
    lines.extend([ln_pe, ln_ke])

    # energy loss
    axs[4].set_title('Energy Dissipated')
    axs[4].set_xlabel('Time (s)')
    axs[4].set_ylabel('Energy Loss (J)')
    axs[4].set_xlim(0, t[-1])
    axs[4].set_ylim(np.min(energy_loss), np.max(energy_loss))
    ln, = axs[4].plot([], [], 'y-', label='Cumulative Loss')
    axs[4].legend()
    lines.append(ln)

    # total energy
    te = pe + ke
    axs[5].set_title('Total Energy')
    axs[5].set_xlabel('Time (s)')
    axs[5].set_ylabel('Energy (J)')
    axs[5].set_xlim(0, t[-1])
    axs[5].set_ylim(0, np.max(te))
    ln, = axs[5].plot([], [], 'k-', label='Total')
    axs[5].legend()
    lines.append(ln)

    # spring-mass visualization (right column)
    spring_ax = fig.add_subplot(grid[:, 2])
    spring_ax.set_xlim(-0.1, 0.1)
    spring_ax.set_ylim(1.1 * np.min(x), -0.1 * np.max(x))
    spring_ax.get_xaxis().set_visible(False)
    spring_ax.get_yaxis().set_visible(False)
    spring_ax.set_aspect('equal', adjustable='box')

    mass_circle = plt.Circle((0, x[0]), 0.05, color='blue', zorder=5)
    spring_ax.add_patch(mass_circle)
    spring_line, = spring_ax.plot([], [], color='red', lw=2)

    ani = animation.FuncAnimation(
        fig, animate, frames=len(t),
        fargs=(t, x, v, a, pe, ke, energy_loss, lines, mass_circle, spring_line),
        interval=50, blit=True,
    )

    plt.tight_layout()
    plt.show()
    return ani


if __name__ == '__main__':
    system = SpringMassSystem(
        mass=0.65,
        spring=Spring(k=5.5, natural_length=0.3),
        damper=Damper(c=0.8),
    )
    t, x, v, a, pe, ke, te, eloss = system.solve_euler(0.1, -0.2, [0, 10], 0.01)
    ani = create_animation(t, x, v, a, pe, ke, eloss)
