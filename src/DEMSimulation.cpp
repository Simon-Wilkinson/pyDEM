#include <iostream>
#include <cstdlib>
#include <ctime>
#include <cmath>

#include "DEMSimulation.h"

DEMSimulation::DEMSimulation(double boundaryRadius, double targetAngularVelocity, double particleRadius,
    double nParticlesType1, double nParticlesType2, double mixingTime,
    double resitiution, double boundaryFrictionFactor, double timestep)
    :
    boundaryRadius(boundaryRadius),
    targetAngularVelocity(targetAngularVelocity),
    particleRadius(particleRadius),
    nParticlesType1(nParticlesType1),
    nParticlesType2(nParticlesType2),
    mixingTime(mixingTime),
    resitiution(resitiution),
    boundaryFrictionFactor(boundaryFrictionFactor),
    timestep(timestep),
    angularVelocity(0.0),
    boundaryAngularPosition(0.0),
    timeElapsed(0.0),
    iteration(0)
{
    // Open the state file for writing
    stateFile.open("data/out/particle_positions.txt");
    if (!stateFile.is_open()) {
        std::cerr << "Error: Could not open particle_positions.txt for writing." << std::endl;
    }
}

void DEMSimulation::addParticle(int type) {
    // adds particle at top middle of box
    Particle newParticle;
    newParticle.x = randomDouble(-particleRadius * 5, particleRadius * 5);
    newParticle.y = 0 - boundaryRadius/2;
    newParticle.vx = 0;
    newParticle.vy = 0;
    newParticle.radius = particleRadius;
    newParticle.type = type;
    newParticle.id = particles.size();
    particles.push_back(newParticle);
}


void DEMSimulation::update() {
    // Update the boundary angle
    boundaryAngularPosition += angularVelocity * timestep;
    timeElapsed += timestep;
    iteration ++;
    for (size_t i = 0; i < particles.size(); ++i) {
        Particle& particle = particles[i];

        // apply gravity
        double ay = -981;
        particle.vy = particle.vy + ay * timestep;

        // Update positions
        particle.x += particle.vx * timestep;
        particle.y += particle.vy * timestep;

        // Calculate distance from center to particle
        double dx = particle.x;
        double dy = particle.y;
        double distance = std::sqrt(dx * dx + dy * dy);
        

        // Check for collisions with the circular boundary
        if (distance + particle.radius > boundaryRadius) {
            double overlap = (distance + particle.radius) - boundaryRadius;
            double normalX = dx / distance;
            double normalY = dy / distance;

            // Reflect the velocity component normal to the boundary and reduce it by the restitution factor
            double relativeVelocity = particle.vx * normalX + particle.vy * normalY;
            particle.vx -= 2 * relativeVelocity * normalX * resitiution;
            particle.vy -= 2 * relativeVelocity * normalY * resitiution;

            // Move the particle back within the boundary
            particle.x -= overlap*randomDouble(1, 1.1) * normalX;
            particle.y -= overlap*randomDouble(1, 1.1) * normalY;

            // Calculate the tangential velocity of the boundary at the contact point
            double boundaryTangentialVelocityX = -angularVelocity * boundaryRadius * normalY;
            double boundaryTangentialVelocityY = angularVelocity * boundaryRadius * normalX;

            // Calculate the relative tangential velocity between the particle and the boundary
            double relativeTangentialVelocityX = particle.vx - boundaryTangentialVelocityX;
            double relativeTangentialVelocityY = particle.vy - boundaryTangentialVelocityY;

            // Apply the tangential velocity correction
            particle.vx -= relativeTangentialVelocityX * boundaryFrictionFactor; 
            particle.vy -= relativeTangentialVelocityY * boundaryFrictionFactor;
        }

        // Check for collisions with other particles
        for (size_t j = i + 1; j < particles.size(); ++j) {
            Particle& other = particles[j];
            double dx = particle.x - other.x;
            double dy = particle.y - other.y;
            double distance = std::sqrt(dx * dx + dy * dy);

            if (distance < particle.radius + other.radius) {
                // Collision detected
                double overlap = (particle.radius + other.radius) - distance;
                double normalX = dx / distance;
                double normalY = dy / distance;        

                // Move particles apart based on their mass (assuming equal mass here)
                particle.x += normalX * overlap * 0.5;
                particle.y += normalY * overlap * 0.5;
                other.x -= normalX * overlap * 0.5;
                other.y -= normalY * overlap * 0.5;

                // Reflect velocities (simple elastic collision with energy absorption)
                double relativeVelocityX = other.vx - particle.vx;
                double relativeVelocityY = other.vy - particle.vy;
                double relativeVelocity = relativeVelocityX * normalX + relativeVelocityY * normalY;

                particle.vx += relativeVelocity * normalX * resitiution;
                particle.vy += relativeVelocity * normalY * resitiution;
                other.vx -= relativeVelocity * normalX * resitiution;
                other.vy -= relativeVelocity * normalY * resitiution;
            }
        }
    }
    if (iteration % 500 == 0) {
        printState();
    }
}

void DEMSimulation::wait(double time) {
    int steps = int(time / timestep);
    for (int i = 0; i < steps; ++i) {
        update();
    }
}

void DEMSimulation::run() {
    for (int i = 0; i < nParticlesType1; ++i) {
        addParticle(1);
        wait(0.01);
    }
    wait(1);
    for (int i = 0; i < nParticlesType2; ++i) {
        addParticle(2);
        wait(0.01);
    }
    wait(1);
    angularVelocity = targetAngularVelocity;
    wait(mixingTime);
    stateFile.close();
}

double DEMSimulation::randomDouble(double min, double max) {
    return min + static_cast<double>(rand()) / RAND_MAX * (max - min);
}

void DEMSimulation::printState() {
    if (stateFile.is_open()) {
        stateFile << "Step: " << iteration << " Time: " << timeElapsed << " Boundary Angle: " << boundaryAngularPosition << "\n";
        for (const auto& particle : particles) {
            stateFile << particle.id << "," << particle.type << "," << particle.radius << "," << particle.x << "," << particle.y << "\n";
        }
        stateFile << "-----------------------------------\n";
    }
}
