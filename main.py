import pygame
import random
import math

pygame.init()
pygame.mixer.music.load('./assets/song1.mp3')
pygame.mixer.music.set_volume(0.7)


WIDTH, HEIGHT = 800, 600
window = pygame.display.set_mode((WIDTH, HEIGHT))

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

pygame.display.set_caption("Space Invaders")

class Player:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT - 50
        self.speed = 5
        self.width = 40
        self.height = 20
    
    def move(self, keys):
        if keys[pygame.K_LEFT] and self.x > 0:
            self.x -= self.speed

        if keys[pygame.K_RIGHT] and self.x < WIDTH - self.width:
            self.x += self.speed
        
    def draw(self):
        pygame.draw.rect(
            window, BLUE, (self.x, self.y, self.width, self.height)
        )
    

class Bullet:
    def __init__(self):
        self.x = 0
        self.y = HEIGHT - 50
        self.speed = 10
        self.state = "ready"

    def fire(self, player_x):
        if self.state == "ready":
            self.x = player_x + 18
            self.y = HEIGHT - 50
            self.state = "fire"
    
    def move(self):
        if self.state == "fire":
            pygame.draw.rect(
                window, GREEN,
                (self.x, self.y, 5, 10)
            )
            self.y -= self.speed
            if self.y < 0:
                self.state = "ready"


class Enemy:
    def __init__(self):
        self.x = random.randint(0, WIDTH - 50)
        self.y = random.randint(50, 150)
        self.width = 40
        self.height = 40
        self.speed = 3

    def move(self):
        self.x += self.speed
        if self.x >= WIDTH - self.width or self.x <= 0:
            self.speed *= -1
            self.y += 40

    def draw(self):
        pygame.draw.rect(
            window, RED,
            (self.x, self.y, self.width, self.height)
        )


class Game:
    def __init__(self):
        self.player = Player()
        self.bullet = Bullet()
        self.enemies = [Enemy() for _ in range(9)]
        self.score = 0
        self.clock = pygame.time.Clock()

    def is_collision(self, enemy):
        distance = math.sqrt(
            (math.pow(enemy.x - self.bullet.x, 2)) +
            (math.pow(enemy.y - self.bullet.y, 2))
        )
        return distance < 27

    def draw_text(self, text, size, x, y):
        font = pygame.font.Font(None, size)
        render = font.render(text, True, WHITE)
        rect = render.get_rect(center=(x, y))
        window.blit(render, rect)

    def run(self):
        running = True
        pygame.mixer.music.play(-1)
        while running:
            window.fill(BLACK)
            keys = pygame.key.get_pressed()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and self.bullet.state == "ready":
                        self.bullet.fire(self.player.x)

            self.player.move(keys)
            self.player.draw()
            self.bullet.move()

            for enemy in self.enemies:
                enemy.move()
                enemy.draw()

                if self.is_collision(enemy):
                    self.bullet.state = "ready"
                    self.score += 1
                    self.enemies.remove(enemy)

                if enemy.y > self.player.y - enemy.height:
                    self.game_over()
                    running = False

                if len(self.enemies) == 0:
                    self.game_win()

            self.draw_text(f"Puntuación: {self.score}", 24, 60, 20)

            pygame.display.update()
            self.clock.tick(60)

    def game_over(self):
        window.fill(BLACK)
        self.draw_text("Fin del juego", 64, WIDTH // 2, HEIGHT // 2)
        pygame.display.update()
        pygame.time.wait(2000)
        main_menu()

    def game_win(self):
        window.fill(BLACK)
        self.draw_text("Has ganado", 64, WIDTH // 2, HEIGHT // 2)
        pygame.display.update()
        pygame.time.wait(2000)
        main_menu()

def main_menu():

    run = True
    while run:
        window.fill(BLACK)
        game = Game()
        game.draw_text("SPACE INVADERS", 64, WIDTH // 2, HEIGHT // 3)
        game.draw_text("Presiona ENTER para empezar", 32, WIDTH // 2, HEIGHT // 2)
        game.draw_text("Usa flecha e izquierda para moverte", 24, WIDTH // 2, HEIGHT // 1.5)
        game.draw_text("Usa la barra de espacio para disparar ", 24, WIDTH // 2, HEIGHT // 1.4)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    game.run()

if __name__ == "__main__":
    main_menu()
    pygame.quit()
