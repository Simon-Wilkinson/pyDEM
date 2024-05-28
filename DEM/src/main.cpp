#include "DEMSimulation.h"

int main() {
    DEMSimulation simulation(100,0.5*3.14159,2,100,100,20,0.1,0.1,0.0001);
    simulation.run();  // Run simulation for 100 steps
    return 0;
}
