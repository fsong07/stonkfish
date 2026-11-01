import pygame

pygame.init()

screen = pygame.display.set_mode((600, 600))
pygame.display.set_caption("Pygame Display Test")

running = True

while running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

    screen.fill((40, 40, 40))

    pygame.draw.circle(
        screen,
        (255, 255, 255),
        (300, 300),
        100
    )

    pygame.display.flip()

pygame.quit()