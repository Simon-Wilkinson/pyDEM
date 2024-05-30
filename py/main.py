import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

from pyDEM import DEMSimulation

from data_model import Particle, Step
from analysis import calculate_degree_of_mixing


def main():
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
    return time_to_mixed

   # Initialize plot
    fig, ax = plt.subplots()
    ax.set_xlim(-boundaryRadius, boundaryRadius)
    ax.set_ylim(-boundaryRadius, boundaryRadius)

    # Initialize scatter and circle patches
    rotation_marker, = ax.plot([], [], 'ro')
    ax.add_patch(plt.Circle((0, 0), boundaryRadius, color='k', fill=False))
    circles = []
    # Function to update the animation
    def update(frame):
        step = steps[frame]
        angle = step.boundary_angle
        if angle > 0:
            pass

        rotation_marker.set_data([boundaryRadius * np.cos(angle)], [boundaryRadius * np.sin(angle)])
        
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

    # Show plot
    plt.show()

if __name__ == '__main__':
    boundaryRadius = 120
    mixingAngularVelocity = 0.5*np.pi
    particleRadius = 2
    numberOfParticlesType1 = 100
    numberOfParticlesType2 = 100
    mixingTime = 1
    restitutionCoefficient = 0.1
    boundaryFrictionCoefficient = 0.2
    timestep = 0.0001


    params = [0.5,1,1.5]
    times_to_mixed = []
    for mixingAngularVelocity in params:
        sim = DEMSimulation(boundaryRadius, mixingAngularVelocity, particleRadius, numberOfParticlesType1, numberOfParticlesType2, mixingTime, restitutionCoefficient, boundaryFrictionCoefficient, timestep)
        sim.run()
        times_to_mixed = main()
        if times_to_mixed != None:
            times_to_mixed.append(times_to_mixed)

    plt.show()

    plt.plot(params, times_to_mixed)
    plt.ylabel('Time to 95% Mixed')

    plt.show()
    