import pygame
import math

pygame.init()

screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

try:
    background_image = pygame.image.load("Assets/wall.png")
except FileNotFoundError:
    print("Error: Could not find background image 'Assets/wall.png'")
    quit()

class Player(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()
        self.x = 300
        self.y = 500
        self.speed = 5
        self.move_left = False
        self.move_right = False
        self.rect = pygame.Rect(self.x, self.y, 100, 20)

    def draw_self(self):
        pygame.draw.rect(screen, (255, 255, 255), self.rect)

    def update(self):
        if self.move_left and self.rect.x > 0:
            self.rect.x -= self.speed
        if self.move_right and self.rect.x < screen_width - 100:
            self.rect.x += self.speed

class Brick(pygame.sprite.Sprite):
    def __init__(self, x, y) -> None:
        super().__init__()
        self.rect = pygame.Rect(x, y, 25, 10)

    def draw_self(self):
        pygame.draw.rect(screen, (255, 255, 255), self.rect)

class Unbreakable(Brick):
    def __init__(self, x, y) -> None:
        super().__init__(x, y)
        self.rect = pygame.Rect(x, y, 25, 10)
    
    def draw_self(self):
        pygame.draw.rect(screen, (100, 100, 100), self.rect)

class Ball(pygame.sprite.Sprite):
    def __init__(self, x, y) -> None:
        super().__init__()
        self.image = pygame.Surface((20, 20), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (255, 255, 255), (10, 10), 10)
        self.rect = self.image.get_rect(center=(x, y))
        self.angle = 45
        self.speed = 3
        self.moving = False

    def collision(self, paddle, bricks, all_sprites):
        if self.moving:
            angle_radians = math.radians(self.angle)
            angle_x = self.speed * math.cos(angle_radians)
            angle_y = -self.speed * math.sin(angle_radians)

            new_rect = self.rect.move(angle_x, angle_y)

            if new_rect.left <= 0 or new_rect.right >= screen_width:
                self.angle = 180 - self.angle
            if new_rect.top <= 0:
                self.angle = -self.angle

            if new_rect.colliderect(paddle.rect):
                self.angle = -self.angle

            for brick in bricks:
                if new_rect.colliderect(brick.rect):
                    if isinstance(brick, Unbreakable):
                        if angle_x > 0:
                            self.rect.right = brick.rect.left
                        elif angle_x < 0:
                            self.rect.left = brick.rect.right
                        if angle_y > 0:
                            self.rect.bottom = brick.rect.top
                        elif angle_y < 0:
                            self.rect.top = brick.rect.bottom

                        self.angle = -self.angle
                    elif isinstance(brick, Brick):
                        self.angle = -self.angle
                        if brick in bricks: 
                            bricks.remove(brick)
                            all_sprites.remove(brick)
                        break

            self.rect = self.rect.move(angle_x, angle_y)

            if self.rect.bottom >= screen_height:
                self.moving = False
                self.rect.center = (paddle.rect.centerx, paddle.rect.top - 10)


    def draw_self(self):
        screen.blit(self.image, self.rect.topleft)


def generate_bricks_from_map(brick_map):
    bricks = pygame.sprite.Group()
    for row_index, row in enumerate(brick_map):
        for col_index, brick_type in enumerate(row):
            if brick_type == 1:
                brick = Brick(10 + col_index * 30 + 5, 10 + row_index * 15)
                bricks.add(brick)
            elif brick_type == 2:
                brick = Unbreakable(10 + col_index * 30 + 5, 10 + row_index * 15)
                bricks.add(brick)
    return bricks

def main():
    all_sprites_list = pygame.sprite.Group()

    player = Player()
    all_sprites_list.add(player)

    brick_map = [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1],
        [1, 1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1, 1, 1, 1],
        [1, 1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1, 1, 1, 1],
        [1, 1, 2, 0, 0, 2, 2, 2, 2, 2, 1, 1, 1, 2, 2, 2, 2, 2, 0, 0, 2, 1, 1, 1, 1],
        [1, 1, 2, 0, 0, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 0, 0, 2, 1, 1, 1, 1],
        [1, 1, 2, 0, 0, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 0, 0, 2, 1, 1, 1, 1],
        [1, 1, 2, 0, 0, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 0, 0, 2, 1, 1, 1, 1],
        [1, 1, 2, 0, 0, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 0, 0, 2, 1, 1, 1, 1],
        [1, 1, 2, 0, 0, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 0, 0, 2, 1, 1, 1, 1],
        [1, 1, 2, 0, 0, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 0, 0, 2, 1, 1, 1, 1],
        [2, 2, 2, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 2, 2, 2, 2, 2]
    ]

    bricks = generate_bricks_from_map(brick_map)
    all_sprites_list.add(bricks)

    ball = Ball(player.rect.centerx, player.rect.top - 10)
    all_sprites_list.add(ball)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.move_left = True
                elif event.key == pygame.K_RIGHT:
                    player.move_right = True
                elif event.key == pygame.K_SPACE:
                    ball.moving = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    player.move_left = False
                elif event.key == pygame.K_RIGHT:
                    player.move_right = False

        player.update()
        ball.collision(player, bricks, all_sprites_list)
        screen.fill((0, 0, 0))
        screen.blit(background_image, (0, 0))

        for sprite in all_sprites_list:
            sprite.draw_self()

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
