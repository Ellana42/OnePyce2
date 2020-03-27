import pygame

pygame.init()

terrain_file = pygame.image.load('graphics/terrain2.png')

resolution = 32
height, width = 32, 32

screen = pygame.display.set_mode((height * resolution, width * resolution))
terrain_file = terrain_file.convert()
selector = pygame.image.load('graphics/selector.png')
x, y = 0, 0
clock = pygame.time.Clock()

running = True

while running:
    previous_x, previous_y = x, y
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                y += 32
            elif event.key == pygame.K_UP:
                y -= 32
            elif event.key == pygame.K_LEFT:
                x -= 32
            elif event.key == pygame.K_RIGHT:
                x += 32
            if event.key == pygame.K_RETURN:
                print(y + x // 32)
        if event.type == pygame.KEYUP:
            x, y = previous_x, previous_y

    screen.blit(terrain_file, (0, 0))
    screen.blit(selector, (x, y))
    pygame.display.update()
    clock.tick(20)
