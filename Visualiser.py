import pygame
from ProcessMap import ProcessMap


class Visualiser():

    def __init__(self, proccess_map: ProcessMap):
        pygame.init()
        self.map = proccess_map
        self.hub_width, self.hub_height = self.map.get_width_height()
        self.radius = 100
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        pygame.display.set_caption("Fly-in")
        info = pygame.display.Info()
        self.height = info.current_h
        self.width = info.current_w
        self.screen.fill((255, 255, 255))
        self.calculate_topcorner()
        self.draw_map()
        
        self.calculate_topcorner()
        self.draw_map()
        
    def calculate_topcorner(self):
        spacing_w = (self.width) / (self.hub_width)
        spacing_h = (self.height) / (self.hub_height)
        spacing_w = (self.width) / (self.hub_width)
        spacing_h = (self.height) / (self.hub_height)
        self.spacing = min(spacing_w, spacing_h)
        self.y0 = (self.height - self.spacing * (self.hub_height - 1)) / 2
        self.x0 = (self.width - self.spacing * (self.hub_width - 1)) / 2

    def draw_map(self):
        self.words_font = pygame.font.Font(None, int(self.spacing * 0.15))
        self.radius = self.spacing * 0.4
        for connection in self.map.connections:
                    x1, y1 = (
                        abs(self.map.hubs[connection.huba.name].x - self.map.min_w) * self.spacing + self.x0,
                        abs(self.map.hubs[connection.huba.name].y - self.map.min_h) * self.spacing + self.y0)
                    x2, y2 = (
                        abs(self.map.hubs[connection.hubb.name].x - self.map.min_w) * self.spacing + self.x0,
                        abs(self.map.hubs[connection.hubb.name].y - self.map.min_h) * self.spacing + self.y0)
                    pygame.draw.line(
                        self.screen, (0, 0, 0), (x1, y1),
                        (x2, y2), 4)
        for hub in self.map.hubs.values():
            color = (100, 100, 100)
            x = abs(self.map.min_w - hub.x) * self.spacing + self.x0
            y = abs(self.map.min_h - hub.y) * self.spacing + self.y0

            try:
                color = pygame.Color(hub.metadata.color)
            except (ValueError, AttributeError):
                color = (100, 100, 100)

            if hub.start or hub.end:
                pygame.draw.circle(self.screen, color, (x, y), self.radius + 15)
            else:
                pygame.draw.circle(self.screen, color, (x, y), self.radius)

            name = self.words_font.render(hub.name, True, (0, 0, 0))
            name_rect = name.get_rect(center=(x, y))
            self.screen.blit(name, name_rect)
            self.number = self.words_font.render(str(hub.drones), True, (0, 0, 0))
            self.number_rect = self.number.get_rect(center=(x, y + 30))
            self.screen.blit(self.number, self.number_rect)

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():#nalinuxie sprawdzic
                if event.type == pygame.QUIT or event.type == 768:
                    running = False

            pygame.display.flip()

        pygame.quit()
