"""
Berkay Yılmaz @2024
github.com/berkayilmaaz
linkedin.com/berkayilmaaz
"""
import numpy as np
import matplotlib.pyplot as plt


class Spring:
    def __init__(self, spring_constant, natural_length):
        self.k = spring_constant       # Spring constant (N/m)
        self.L = natural_length        # Natural length of the spring (m)
 
    def force(self, extension):
        return -self.k * (extension - self.L)  # Spring force (N)

    def extension(self, displacement):
        # Calculate the extension of the spring from its natural length
        return displacement + self.L

class Mass:
    def __init__(self, mass):
        self.m = mass                 # Mass of the object (kg)

class Damping:
    def __init__(self, damping_coefficient):
        self.c = damping_coefficient  # Damping coefficient (s/m)

    def force(self, velocity):
        return -self.c * velocity     # Damping force (N)

class SpringMassSystem:  
    def __init__(self, mass, spring, damping, gravity=9.81):
        self.mass = mass
        self.spring = spring
        self.damping = damping
        self.gravity = gravity        # Acceleration due to gravity (m/s^2)

    def equation(self, x, v):
        spring_force = self.spring.force(x)
        damping_force = self.damping.force(v)
        net_force = spring_force + damping_force - self.mass.m * self.gravity
        return net_force / self.mass.m # Acceleration (m/s^2)

    def solve_euler(self, initial_displacement, initial_velocity, t_span, dt):
        num_steps = int((t_span[1] - t_span[0]) / dt)
        t = np.linspace(t_span[0], t_span[1], num_steps)
        y = np.zeros(num_steps)
        v = np.zeros(num_steps)
        a = np.zeros(num_steps)
        pe = np.zeros(num_steps)
        ke = np.zeros(num_steps)
        energy_loss = np.zeros(num_steps)

        y[0], v[0] = initial_displacement, initial_velocity
        pe[0] = 0.5 * self.spring.k * (y[0] - self.spring.L)**2
        ke[0] = 0.5 * self.mass.m * v[0]**2

        for i in range(1, num_steps):
            a[i-1] = self.equation(y[i-1], v[i-1])
            y[i] = y[i-1] + v[i-1] * dt
            v[i] = v[i-1] + a[i-1] * dt
            pe[i] = 0.5 * self.spring.k * (y[i] - self.spring.L)**2    #1/2kx^2
            ke[i] = 0.5 * self.mass.m * v[i]**2                        #1/2mv^2
            energy_loss[i] = energy_loss[i-1] + self.damping.force(v[i-1]) * v[i-1] * dt

        return t, y, v, a, pe, ke, energy_loss
    
    
def plot_motion(t, y, v, a, pe, ke, energy_loss):
    fig, axs = plt.subplots(3, 2, figsize=(14, 12))

    # Displacement vs Time
    axs[0, 0].plot(t, y, 'r-')
    axs[0, 0].set_xlabel('Time (s)')
    axs[0, 0].set_ylabel('Displacement (m)')
    axs[0, 0].set_title('Displacement vs Time')

    # Phase Space Plot
    axs[0, 1].plot(y, v, 'b-')
    axs[0, 1].set_xlabel('Displacement (m)')
    axs[0, 1].set_ylabel('Velocity (m/s)')
    axs[0, 1].set_title('Phase Space Plot')

    # Velocity and Acceleration vs Time
    ax2 = axs[1, 0].twinx()
    axs[1, 0].plot(t, v, 'b-', label='Velocity')
    ax2.plot(t, a, 'g-', label='Acceleration')
    axs[1, 0].set_xlabel('Time (s)')
    axs[1, 0].set_ylabel('Velocity (m/s)')
    ax2.set_ylabel('Acceleration (m/s²)')
    axs[1, 0].set_title('Velocity and Acceleration vs Time')
    axs[1, 0].legend(loc='upper left')
    ax2.legend(loc='upper right')

    # Potential and Kinetic Energy vs Time
    axs[1, 1].plot(t, pe, 'm-', label='Potential Energy')
    axs[1, 1].plot(t, ke, 'c-', label='Kinetic Energy')
    axs[1, 1].set_xlabel('Time (s)')
    axs[1, 1].set_ylabel('Energy (J)')
    axs[1, 1].set_title('Potential and Kinetic Energy vs Time')
    axs[1, 1].legend()

    # Energy Loss vs Time
    axs[2, 0].plot(t, energy_loss, 'y-')
    axs[2, 0].set_xlabel('Time (s)')
    axs[2, 0].set_ylabel('Energy Loss (J)')
    axs[2, 0].set_title('Energy Loss vs Time')

    # Total Energy (Potential + Kinetic) vs Time
    total_energy = pe + ke  
    axs[2, 1].plot(t, total_energy, 'k-', label='Total Energy')
    axs[2, 1].set_xlabel('Time (s)')
    axs[2, 1].set_ylabel('Energy (J)')
    axs[2, 1].set_title('Total Energy vs Time')
    axs[2, 1].legend()
    


    plt.tight_layout()
    plt.show()
    


mass = Mass(0.65)
spring = Spring(5.5, 0.3)
damping = Damping(1)
system = SpringMassSystem(mass, spring, damping)
t, y, v, a, pe, ke, energy_loss = system.solve_euler(0.0, 0, [0, 10], 0.01)

plot_motion(t, y, v, a, pe, ke, energy_loss)




