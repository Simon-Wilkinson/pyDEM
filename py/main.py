import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

from pyDEM import DEMSimulation

from data_model import Particle, Step
from analysis import calculate_degree_of_mixing


def get_steps() -> list[Step]:
    steps = []
    with open('data/out/particle_positions.txt', 'r') as f:
        all_text = f.read()
        stepsText = all_text.split('-----------------------------------')
        for step in stepsText:
            lines = step.split('\n')
            lines = [line for line in lines if line != '']
            if lines == []:
                continue
            line = lines[0].split(' ')
            step_number = int(line[1])
            time = float(line[3])
            boundary_angle = float(line[6])
            particles = []
            for line in lines[1:]:
                id, type, radius, x, y = line.split(',')
                particle = Particle(int(id), int(type), float(radius), float(x), float(y))
                particles.append(particle)
            step = Step(step_number, time, boundary_angle, particles)
            steps.append(step)
    return steps

def get_time_to_mixed(steps: list[Step]) -> float:
    time = []
    doms = []
    flag = True
    time_to_mixed = None
    for step in steps:
        dom = calculate_degree_of_mixing(step, 10)
        time.append(step.time)
        doms.append(dom)
        if dom > 0.95 and flag:
            time_to_mixed = step.time
            flag = False   
    
    plt.plot(time, doms)
    #set labels
    plt.xlabel("Time")
    plt.ylabel("Degree of Mixing %")
    
    return time_to_mixed

def animate(steps: list[Step], boundary_radius: float):
    # Initialize plot
    fig, ax = plt.subplots()
    ax.set_xlim(-boundary_radius, boundary_radius)
    ax.set_ylim(-boundary_radius, boundary_radius)

    # Initialize scatter and circle patches
    rotation_marker, = ax.plot([], [], 'ro')
    ax.add_patch(plt.Circle((0, 0), boundary_radius, color='k', fill=False))
    ax.set_aspect('equal', adjustable = 'box')
    circles = []
    # Function to update the animation
    def update(frame):
        step = steps[frame]
        angle = step.boundary_angle
        if angle > 0:
            pass

        rotation_marker.set_data([boundary_radius * np.cos(angle)], [boundary_radius * np.sin(angle)])        
        for i, particle in enumerate(step.particles):
            if i >= len(circles):
                circles.append(plt.Circle((particle.x, particle.y), particle.radius, color='b' if particle.type == 1 else 'g'))
                ax.add_patch(circles[i])
            else:
                circles[i].center = (particle.x, particle.y)
                circles[i].radius = particle.radius
                circles[i].set_color('b' if particle.type == 1 else 'g')
        
        return rotation_marker, *circles

    #Create animation
    ani = animation.FuncAnimation(fig, update, frames=len(steps), interval=5, blit=True, repeat=False)
    plt.show()
   
    # Show plot
    


def main():
    boundary_radius = 120
    particle_radius = 2
    number_of_particles_type1 = 100
    number_of_particles_type2 = 100
    mixing_time = 20
    restitution_coefficient = 0.1
    boundary_friction_coefficient = 0.2
    timestep = 0.0001

    show_animations = True
    # Test three different mixingAngularVelocities
    params = [0.5,1,1.5]
    times_to_mixed = []
    for mixing_angular_velocity in params:
        sim = DEMSimulation(boundary_radius, mixing_angular_velocity, particle_radius, number_of_particles_type1, number_of_particles_type2, mixing_time, restitution_coefficient, boundary_friction_coefficient, timestep)
        sim.run()
        steps = get_steps()
        time_to_mixed = get_time_to_mixed(steps)
        if show_animations: animate(steps, boundary_radius)
        if times_to_mixed != None: times_to_mixed.append(time_to_mixed)

    plt.show()
    plt.plot(params, times_to_mixed)
    plt.xlabel("Angular velocity")
    plt.ylabel('Time to 95% Mixed')
    plt.show()

if __name__ == '__main__':
    main()
    