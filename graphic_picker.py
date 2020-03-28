import pygame

pygame.init()

terrain_file = pygame.image.load('graphics/terrain.png')

resolution = 32
height, width = 32, 32

screen = pygame.display.set_mode((height * resolution, width * resolution))
terrain_file = terrain_file.convert()
selector = pygame.image.load('graphics/selector.png')
x, y = 0, 0
clock = pygame.time.Clock()

running = True
vx, vy = 0, 0
while running:
    previous_x, previous_y = x, y
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                vx, vy = (0, 32)
            elif event.key == pygame.K_UP:
                vx, vy = (0, -32)
            elif event.key == pygame.K_LEFT:
                vx, vy = (-32, 0)
            elif event.key == pygame.K_RIGHT:
                vx, vy = (32, 0)
            if event.key == pygame.K_RETURN:
                print(y + x // 32)
        if event.type == pygame.KEYUP:
            vx, vy = 0, 0
            x, y = previous_x, previous_y
    x += vx
    y += vy
    screen.blit(terrain_file, (0, 0))
    screen.blit(selector, (x, y))
    pygame.display.update()
    clock.tick(20)
