import pygame
import time
import random
pygame.font.init()

WIDTH, HEIGHT = 1000, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Cats")

PLAYER_WIDTH = 125
PLAYER_HEIGHT = 100

PLAYER_VEL = 7
STAR_WIDTH = 100
STAR_HEIGHT = 100
STAR_VEL = 3

FONT = pygame.font.SysFont("Press Start 2P", 50)

BG = pygame.transform.scale(pygame.image.load("bg.jpg"), (WIDTH, HEIGHT))
PLAYER = pygame.transform.scale(pygame.image.load("catship.png"), (PLAYER_WIDTH, PLAYER_HEIGHT))
STAR_IMG = pygame.transform.scale(pygame.image.load("dogship.png"), (STAR_WIDTH, STAR_HEIGHT))

def draw(player_pos, elapsed_time, stars):
    WIN.blit(BG, (0, 0))
    WIN.blit(PLAYER, player_pos)

    time_text = FONT.render(f"Time: {round(elapsed_time)}s", 1, "white")
    WIN.blit(time_text, (10,10))

    for star_rect, star_img in stars:
        WIN.blit(star_img, (star_rect.x, star_rect.y))

    pygame.display.update()

def main():
    run = True

    # player = pygame.image.load("catship.png")
    player_x = 200
    player_y = HEIGHT - PLAYER_HEIGHT

    clock = pygame.time.Clock()
    start_time = time.time()
    elapsed_time = 0

    star_add_increment = 2000
    star_count = 0

    stars = []
    hit = False

    while run:
        star_count += clock.tick(60)
        elapsed_time = time.time() - start_time

        if star_count > star_add_increment:
            for _ in range(3):
                star_x = random.randint(0, WIDTH - STAR_WIDTH)
                star_rect = pygame.Rect(star_x, -STAR_HEIGHT, STAR_WIDTH, STAR_HEIGHT)
                stars.append((star_rect, STAR_IMG))

            star_add_increment = max(200, star_add_increment - 50)
            star_count = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x - PLAYER_VEL >= 0:
            player_x -= PLAYER_VEL
        if keys[pygame.K_RIGHT] and player_x + PLAYER_VEL + PLAYER_WIDTH <= WIDTH:
            player_x += PLAYER_VEL

        player_rect = pygame.Rect(player_x, player_y, PLAYER_WIDTH, PLAYER_HEIGHT)

        for star in stars[:]:
            star_rect, star_img = star
            star_rect.y += STAR_VEL

            if star_rect.y > HEIGHT:
                stars.remove(star)
            elif star_rect.colliderect(player_rect):
                stars.remove(star)
                hit = True
                break

        if hit:
            lost_text = FONT.render("You were hit!", 1, "white")
            WIN.blit(lost_text, (WIDTH/2 - lost_text.get_width()/2, HEIGHT/2 - lost_text.get_height()/2))
            pygame.display.update()
            pygame.time.delay(4000)
            break

        draw((player_x, player_y), elapsed_time, stars)

    pygame.quit()

if __name__ == '__main__':
    main()