import pygame
from ProcessMap import ProcessMap


class Visualiser():

    def __init__(self, map_file="maps/hard/03_ultimate_challenge.txt"):
        self.map = ProcessMap(map_file)
        info = pygame.display.Info()
        self.height = info.current_h
        self.width = info.current_w
        self.hub_width, self.hub_height = self.map.get_width_height()
        self.radius = 50
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        pygame.display.set_caption("Fly-in")
        self.screen.fill((255, 255, 255))

    def calculate_topcorner(self):
        spacing_w = (self.width - 2 * self.radius) / (self.hub_width)
        spacing_h = (self.height - 2 * self.radius) / (self.hub_height)
        self.spacing = min(spacing_w, spacing_h)
        self.y0 = (self.height - self.spacing * (self.hub_height - 1)) / 2
        self.x0 = (self.width - self.spacing * (self.hub_width - 1)) / 2

    def draw_map(self):
        for hub in self.map.hubs:
            x = abs(self.map.min_w - hub.x) * self.spacing + self.x0
            y = abs(self.map.min_h - hub.y) * self.spacing + self.y0
            pygame.draw.circle(self.screen, (0, 0, 255), (x, y), self.radius)

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():#nalinuxie sprawdzic
                if event.type == pygame.QUIT or event.type == 768:
                    running = False

            pygame.display.flip()

        pygame.quit()
