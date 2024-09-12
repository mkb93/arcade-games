import pygame

# Base class for game objects
class CircleShape(pygame.sprite.Sprite):
    def __init__(self, x, y, radius):
        # we will be using this later
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()

        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.radius = radius

    def draw(self, screen):
        # sub-classes must override
        pass

    def update(self, dt):
        # sub-classes must override
        pass
    def collision(self, CircleShape):
        distance_between_Circles = self.position.distance_to(CircleShape.position)
        collision_distance = self.radius + CircleShape.radius
        if distance_between_Circles <= collision_distance:
            return True
        else:
            return False
    
