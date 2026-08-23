import pygame

pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("Fly-in")
screen.fill((255, 255, 255))
info = pygame.display.Info()

running = True
hub_width = 9
hub_height = 3
connection_size = 0
spacing = 0
radius = 50
height = info.current_h
width = info.current_w
spacing_w = (width - 2 * radius - 2 * margin) / (hub_width)
spacing_h = (height - 2 * radius - 2 * margin) / (hub_height)
spacing = min(spacing_w, spacing_h)
y = (height - spacing * (hub_height - 1)) / 2
x = (width - spacing * (hub_width - 1)) / 2
while running:
    screen.fill((255, 255, 255))
    for event in pygame.event.get():#nalinuxie sprawdzic
        if event.type == pygame.QUIT or event.type == 768:
            running = False

    for _ in range(0, hub_height):
        pygame.draw.circle(screen, (0, 0, 255), (x, y), radius)
        for _ in range(0, hub_width - 1):
            pygame.draw.line(screen, (0, 0, 0), (x + radius, y), (x + spacing - radius, y), 5)
            x = x + spacing
            pygame.draw.circle(screen, (0, 0, 255), (x, y), radius)
        y = y + spacing
        x = (width - spacing * (hub_width - 1)) / 2

    pygame.display.flip()

pygame.quit()
