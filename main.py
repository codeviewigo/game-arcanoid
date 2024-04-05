# Импорт необходимых библиотек
import pygame
import sys

# Инициализация Pygame
pygame.init()

# Основные настройки экрана
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
BG_COLOR = (0, 0, 0)  # Цвет фона

# Настройки ракетки
PADDLE_WIDTH, PADDLE_HEIGHT = 100, 20
PADDLE_COLOR = (250, 155, 240)
PADDLE_SPEED = 10

# Настройки мяча
BALL_COLOR = (255, 255, 255)
BALL_RADIUS = 10
BALL_SPEED = [5, 5]

# Настройки кирпичей
BRICK_COLOR = (255, 0, 0)
BRICK_WIDTH, BRICK_HEIGHT = 75, 30
BRICK_ROWS, BRICK_COLS = 5, 10


# Классы
class Paddle:
    def __init__(self):
        self.width = PADDLE_WIDTH
        self.height = PADDLE_HEIGHT
        self.x = (SCREEN_WIDTH - self.width) / 2
        self.y = SCREEN_HEIGHT - self.height - 10
        self.color = PADDLE_COLOR
        self.speed = PADDLE_SPEED

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

    def move(self, direction):
        if direction == "left" and self.x > 0:
            self.x -= self.speed
        if direction == "right" and self.x < SCREEN_WIDTH - self.width:
            self.x += self.speed


class Ball:
    def __init__(self):
        self.radius = BALL_RADIUS
        self.x = SCREEN_WIDTH / 2
        self.y = SCREEN_HEIGHT / 2
        self.color = BALL_COLOR
        self.speed = BALL_SPEED

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

    def move(self):
        self.x += self.speed[0]
        self.y += self.speed[1]

        # Отскок от стен
        if self.x <= 0 or self.x >= SCREEN_WIDTH:
            self.speed[0] = -self.speed[0]
        if self.y <= 0:
            self.speed[1] = -self.speed[1]


class Brick:
    def __init__(self, x, y):
        self.width = BRICK_WIDTH
        self.height = BRICK_HEIGHT
        self.x = x
        self.y = y
        self.color = BRICK_COLOR
        self.visible = True  # Состояние видимости кирпича

    def draw(self, screen):
        if self.visible:
            pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))


class GameManager:
    def __init__(self):
        self.paddle = Paddle()
        self.ball = Ball()
        self.bricks = [Brick(x * (BRICK_WIDTH + 5), y * (BRICK_HEIGHT + 5)) for y in range(BRICK_ROWS) for x in
                       range(BRICK_COLS)]
        self.score = 0  # Инициализация счета

    def run(self):
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Арканоид")
        clock = pygame.time.Clock()

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.paddle.move("left")
            if keys[pygame.K_RIGHT]:
                self.paddle.move("right")

            self.ball.move()

            # Проверка столкновения мяча с ракеткой
            if self.ball.y + self.ball.radius >= self.paddle.y and self.paddle.x <= self.ball.x <= self.paddle.x + self.paddle.width:
                self.ball.speed[1] = -self.ball.speed[1]

            # Перезапуск мяча, если не отбит
            elif self.ball.y > SCREEN_HEIGHT:
                self.ball.x, self.ball.y = SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2
                self.ball.speed = BALL_SPEED.copy()
                if self.score > 0:  # Уменьшаем счет, если мяч не отбит
                    self.score -= 1

            # Проверка столкновения мяча с кирпичами
            for brick in self.bricks:
                if brick.visible and brick.x <= self.ball.x <= brick.x + brick.width and brick.y <= self.ball.y <= brick.y + brick.height:
                    brick.visible = False  # Скрываем кирпич
                    self.ball.speed[1] = -self.ball.speed[1]  # Меняем направление мяча
                    self.score += 1  # Увеличиваем счет за выбитый кирпич

            screen.fill(BG_COLOR)
            self.paddle.draw(screen)
            self.ball.draw(screen)
            for brick in self.bricks:
                brick.draw(screen)

            # Отображение счета
            font = pygame.font.Font(None, 36)
            score_text = font.render(f"Score: {self.score}", 1, (255, 255, 255))
            screen.blit(score_text, (5, 5))

            pygame.display.flip()
            clock.tick(60)

        pygame.quit()


GameManager().run()
