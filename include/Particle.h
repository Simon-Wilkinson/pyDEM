#ifndef PARTICLE_H
#define PARTICLE_H

struct Particle {
    double x, y;       // Position
    double vx, vy;     // Velocity
    double radius;     // Radius
    int type;          // type of particle
    int id;
};

#endif
