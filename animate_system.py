"""
Berkay Yılmaz @2024
github.com/berkayilmaaz
linkedin.com/berkayilmaaz
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from spring_mass_system import Spring, Mass, Damping, SpringMassSystem


plt.rcParams['animation.ffmpeg_path'] = '/opt/homebrew/bin/ffmpeg'   

    # Animation update function
def animate(i, t, y, v, a, pe, ke, energy_loss, lines, mass_circle, spring_line):
    # Update the data in plots
    lines[0].set_data(t[:i+1], y[:i+1])
    lines[1].set_data(y[:i+1], v[:i+1])
    lines[2].set_data(t[:i+1], v[:i+1])  
    lines[3].set_data(t[:i+1], a[:i+1])  
    lines[4].set_data(t[:i+1], pe[:i+1])
    lines[5].set_data(t[:i+1], ke[:i+1])
    lines[6].set_data(t[:i+1], energy_loss[:i+1])
    lines[7].set_data(t[:i+1], pe[:i+1] + ke[:i+1])
    
    # Update the position of the mass
    mass_circle.center = (0, y[i])
  
    # Update the position and length of the spring
    spring_line.set_data([0, 0], [0, y[i]])
  
    # Flatten the list of artists for return
    flattened_lines = [item for sublist in lines for item in (sublist if isinstance(sublist, tuple) else [sublist])]
    return flattened_lines + [mass_circle, spring_line]



def create_animation(t, y, v, a, pe, ke, energy_loss):
    fig = plt.figure(figsize=(14, 12))
    grid = plt.GridSpec(3, 3, fig)  # Creating a 3x3 grid
    lines = []  # List to hold all the line objects for updating during animation

    # Create subplots for the left and middle columns
    axs = [fig.add_subplot(grid[i, j]) for i in range(3) for j in range(2)]

    # Displacement vs Time
    axs[0].set_title('Displacement vs Time')
    axs[0].set_xlabel('Time (s)')
    axs[0].set_ylabel('Displacement (m)')
    axs[0].set_xlim(0, t[-1])
    axs[0].set_ylim(np.min(y), np.max(y))
    line1, = axs[0].plot([], [], 'r-', label='Displacement')
    axs[0].legend()
    lines.append(line1)

    # Phase Space Plot
    axs[1].set_title('Phase Space Plot')
    axs[1].set_xlabel('Displacement (m)')
    axs[1].set_ylabel('Velocity (m/s)')
    axs[1].set_xlim(np.min(y), np.max(y))
    axs[1].set_ylim(np.min(v), np.max(v))
    line2, = axs[1].plot([], [], 'b-', label='Phase Space')
    axs[1].legend()
    lines.append(line2)

    # Velocity and Acceleration vs Time
    axs[2].set_title('Velocity and Acceleration vs Time')
    axs[2].set_xlabel('Time (s)')
    axs[2].set_ylabel('Velocity (m/s)')
    axs[2].set_xlim(0, t[-1])
    axs[2].set_ylim(np.min(v), np.max(v))
    line3, = axs[2].plot([], [], 'b-', label='Velocity')
    axs[2].legend(loc='upper left')
    lines.append(line3)

    ax2 = axs[2].twinx()
    ax2.set_ylabel('Acceleration (m/s²)', color='g')
    ax2.set_ylim(np.min(a), np.max(a))
    line4, = ax2.plot([], [], 'g-', label='Acceleration')
    ax2.legend(loc='upper right')
    lines.append(line4)

    # Potential and Kinetic Energy vs Time
    axs[3].set_title('Potential and Kinetic Energy vs Time')
    axs[3].set_xlabel('Time (s)')
    axs[3].set_ylabel('Energy (J)')
    axs[3].set_xlim(0, t[-1])
    axs[3].set_ylim(0, max(np.max(pe), np.max(ke)))
    line5, = axs[3].plot([], [], 'm-', label='Potential Energy')
    line6, = axs[3].plot([], [], 'c-', label='Kinetic Energy')
    axs[3].legend()
    lines.append(line5)  
    lines.append(line6)  


    # Energy Loss vs Time
    axs[4].set_title('Energy Loss vs Time')
    axs[4].set_xlabel('Time (s)')
    axs[4].set_ylabel('Energy Loss (J)')
    axs[4].set_xlim(0, t[-1])
    axs[4].set_ylim(np.min(energy_loss), np.max(energy_loss))
    line7, = axs[4].plot([], [], 'y-', label='Energy Loss')
    axs[4].legend()
    lines.append(line7)

    # Total Energy vs Time
    axs[5].set_title('Total Energy vs Time')
    axs[5].set_xlabel('Time (s)')
    axs[5].set_ylabel('Energy (J)')
    axs[5].set_xlim(0, t[-1])
    axs[5].set_ylim(0, np.max(pe + ke))
    line8, = axs[5].plot([], [], 'k-', label='Total Energy')
    axs[5].legend()
    lines.append(line8)

    # Create the spring-mass animation subplot spanning the entire right column
    spring_mass_ax = fig.add_subplot(grid[:, 2])
    spring_mass_ax.set_xlim(-0.1, 0.1)
    spring_mass_ax.set_ylim(1.1 * np.min(y), -0.1 * np.max(y))
    spring_mass_ax.get_xaxis().set_visible(False)
    spring_mass_ax.get_yaxis().set_visible(False)
    spring_mass_ax.set_aspect('equal', adjustable='box')

    # Create a circle to represent the mass
    mass_circle = plt.Circle((0, y[0]), 0.05, color='blue', zorder=5)
    spring_mass_ax.add_patch(mass_circle)

    # Create a line to represent the spring
    spring_line, = spring_mass_ax.plot([], [], color='red', lw=2)

    # Create the animation using FuncAnimation
    ani = animation.FuncAnimation(
        fig, animate, frames=len(t),
        fargs=(t, y, v, a, pe, ke, energy_loss, lines, mass_circle, spring_line),
        interval=50, blit=True
    )

    plt.tight_layout()
    plt.show()
    return ani


    fig = plt.figure(figsize=(14, 12))
    grid = plt.GridSpec(3, 3, fig)
    lines = []

    # Create subplots for the left and middle columns
    axs = [fig.add_subplot(grid[i, j]) for i in range(3) for j in range(2)]

    # Configure each subplot
    # Displacement vs Time
    axs[0].set_title('Displacement vs Time')
    axs[0].set_xlabel('Time (s)')
    axs[0].set_ylabel('Displacement (m)')
    axs[0].set_xlim(0, t[-1])
    axs[0].set_ylim(np.min(y), np.max(y))
    line1, = axs[0].plot([], [], 'r-', label='Displacement')
    axs[0].legend()
    lines.append(line1)
    
    # Phase Space Plot
    axs[1].set_title('Phase Space Plot')
    axs[1].set_xlabel('Displacement (m)')
    axs[1].set_ylabel('Velocity (m/s)')
    axs[1].set_xlim(np.min(y), np.max(y))
    axs[1].set_ylim(np.min(v), np.max(v))
    line2, = axs[1].plot([], [], 'b-', label='Phase Space')
    axs[1].legend()
    lines.append(line2) 

    # Velocity and Acceleration vs Time
    axs[2].set_title('Velocity and Acceleration vs Time')
    axs[2].set_xlabel('Time (s)')
    axs[2].set_ylabel('Velocity (m/s)')
    axs[2].set_xlim(0, t[-1])
    axs[2].set_ylim(np.min(v), np.max(v))
    line3, = axs[2].plot([], [], 'b-', label='Velocity') 
    ax2 = axs[2].twinx()
    ax2.set_ylabel('Acceleration (m/s²)', color='g')
    ax2.set_ylim(np.min(a), np.max(a))
    line4, = ax2.plot([], [], 'g-', label='Acceleration')  
    axs[2].legend(loc='upper left')  
    ax2.legend(loc='upper right')  

    # Potential and Kinetic Energy vs Time
    axs[3].set_title('Potential and Kinetic Energy vs Time')
    axs[3].set_xlabel('Time (s)')
    axs[3].set_ylabel('Energy (J)')
    axs[3].set_xlim(0, t[-1])
    axs[3].set_ylim(0, max(np.max(pe), np.max(ke)))
    line5, = axs[3].plot([], [], 'm-', label='Potential Energy') 
    line6, = axs[3].plot([], [], 'c-', label='Kinetic Energy') 
    axs[3].legend()  

    # Energy Loss vs Time
    axs[4].set_title('Energy Loss vs Time')
    axs[4].set_xlabel('Time (s)')
    axs[4].set_ylabel('Energy Loss (J)')
    axs[4].set_xlim(0, t[-1])
    axs[4].set_ylim(np.min(energy_loss), np.max(energy_loss))
    line7, = axs[4].plot([], [], 'y-', label='Energy Loss') 
    axs[4].legend()  

    # Total Energy vs Time
    axs[5].set_title('Total Energy vs Time')
    axs[5].set_xlabel('Time (s)')
    axs[5].set_ylabel('Energy (J)')
    axs[5].set_xlim(0, t[-1])
    axs[5].set_ylim(0, np.max(pe + ke))
    line8, = axs[5].plot([], [], 'k-', label='Total Energy') 
    axs[5].legend()  


    # Create the spring-mass animation subplot spanning the entire right column
    spring_mass_ax = fig.add_subplot(grid[:, 2])
    # Set a small xlim range to avoid the singular transformation warning
    spring_mass_ax.set_xlim(-0.1, 0.1)  # -0.1 ve 0.1 arasında küçük bir aralık belirleyin
    spring_mass_ax.set_ylim(1.1 * np.min(y), -0.1 * np.max(y))
    spring_mass_ax.get_xaxis().set_visible(False)
    spring_mass_ax.get_yaxis().set_visible(False)
    spring_mass_ax.set_aspect('equal', adjustable='box')  # Ensure equal aspect ratio


    # Create a circle to represent the mass
    mass_circle = plt.Circle((0, y[0]), 0.05, color='blue', zorder=5)  # The zorder parameter makes sure the circle is drawn on top of the line
    spring_mass_ax.add_patch(mass_circle)
    
    # Create a line to represent the spring
    spring_line, = spring_mass_ax.plot([], [], color='red', lw=2)

    # Create the animation
    ani = animation.FuncAnimation(
        fig, animate, frames=len(t),
        fargs=(t, y, v, a, pe, ke, energy_loss, lines, mass_circle, spring_line),
        interval=50, blit=True
    )

    plt.tight_layout()
    plt.show()
    return ani


# System-features
mass = Mass(0.65)
spring = Spring(5.5, 0.3)
damping = Damping(0.8)
system = SpringMassSystem(mass, spring, damping)
t, y, v, a, pe, ke, energy_loss = system.solve_euler(0.1, -0.2, [0, 10], 0.01)

# save 
ani = create_animation(t, y, v, a, pe, ke, energy_loss)
ani.save('animation_Mass(0.65)_k(5.5)_damping(0.8).mp4', writer='ffmpeg', fps=30)