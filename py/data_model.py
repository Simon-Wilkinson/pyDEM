class Particle:
    def __init__(self, id, type, radius, x, y):
        self.id = id
        self.type = type
        self.radius = radius
        self.x = x
        self.y = y

class Step:
    def __init__(self, step, time, boundary_angle, particles):
        self.step = step
        self.time = time
        self.boundary_angle = boundary_angle
        self.particles = particles