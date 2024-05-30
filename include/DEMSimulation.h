#ifndef DEMSIMULATION_H
#define DEMSIMULATION_H

#include <vector>
#include "Particle.h"
#include <string>
#include <fstream>

class DEMSimulation {
public:
    DEMSimulation(double boundaryRadius, double targetAngularVelocity, double particleRadius,
        double nParticlesType1, double nParticlesType2, double mixingTime,
        double resitiution, double boundaryFrictionFactor, double timestep);
    void run();

    // design variables
    const double boundaryRadius;
    const double targetAngularVelocity;
    const double particleRadius;
    const double nParticlesType1;
    const double nParticlesType2;
    const double mixingTime;

    // contact model
    const double resitiution;
    const double boundaryFrictionFactor;

    // simulation settings
    const double timestep;
    std::ofstream stateFile;

    // state variables 
    double angularVelocity;
    double boundaryAngularPosition;
    double timeElapsed;
    int iteration;

private:
    std::vector<Particle> particles;
    double randomDouble(double min, double max);
    void printState();
    void addParticle(int type);
    void wait(double time);
    void update();
};

#endif
