import pygame
import random


class Particle:
    def __init__(self, color=(255, 255, 255), x=0, y=0, start_radius=5, direction='left'):
        self.color = color
        self.x = x
        self.y = y
        self.pos = (self.x, self.y)
        self.radius = start_radius
        self.direction = direction

    def update(self):
        if self.direction == 'left':
            self.x -= 2
            self.y -= random.randint(0,1)
        elif self.direction == 'right':
            self.x += 2
            self.y -= random.randint(0,1)
        elif self.direction == 'up':
            self.y -= 2
            self.x += random.randint(-1,1)
        elif self.direction == 'down':
            self.y += 2
            self.x += random.randint(-1,1)
        self.radius -= 0.1  # Decrease radius with each update to simulate shrinking effect

    def draw(self, display):
        pygame.draw.circle(display, self.color, (self.x, self.y), self.radius)

    def is_alive(self):
        return self.radius > 0



class ParticleSystem:
    def __init__(self, max_particles=100):
        self.particles = []
        self.max_particles = max_particles

    def create_particle(self, x, y, color=(255,255,255), direction='left'):
        if len(self.particles) < self.max_particles:
            particle = Particle(color, x, y, 3, direction)
            self.particles.append(particle)

    def update(self):
        for particle in self.particles:
            particle.update()
        self.particles = [p for p in self.particles if p.is_alive()]  # Remove dead particles

    def draw(self, display):
        for particle in self.particles:
            particle.draw(display)