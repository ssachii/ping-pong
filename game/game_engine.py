import pygame
import pygame
from .paddle import Paddle
from .ball import Ball

pygame.mixer.init()  # ✅ Initialize the sound mixer

from .paddle import Paddle
from .ball import Ball

# Game Engine

WHITE = (255, 255, 255)

class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.paddle_width = 10
        self.paddle_height = 100

        self.player = Paddle(10, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ai = Paddle(width - 20, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ball = Ball(width // 2, height // 2, 7, 7, width, height)

        self.player_score = 0
        self.ai_score = 0
        self.winning_score = 5  # default target
        self.font = pygame.font.SysFont("Arial", 30)

        # --- Sound Effects ---
        self.sound_paddle = pygame.mixer.Sound("assets/sounds/paddle_hit.wav")
        self.sound_wall = pygame.mixer.Sound("assets/sounds/wall_bounce.wav")
        self.sound_score = pygame.mixer.Sound("assets/sounds/score.wav")


    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.player.move(-10, self.height)
        if keys[pygame.K_s]:
            self.player.move(10, self.height)

    def update(self):
        # Move the ball
        self.ball.move()
    
        ball_rect = self.ball.rect()
        if ball_rect.colliderect(self.player.rect()):
            self.ball.velocity_x = abs(self.ball.velocity_x)  # bounce right
            self.sound_paddle.play()
        elif ball_rect.colliderect(self.ai.rect()):
            self.ball.velocity_x = -abs(self.ball.velocity_x)  # bounce left
            self.sound_paddle.play()

        # Scoring logic
        if self.ball.x <= 0:
            self.ai_score += 1
            self.sound_score.play()  # ✅ Play sound for AI scoring
            self.ball.reset()
        elif self.ball.x >= self.width:
            self.player_score += 1
            self.sound_score.play()  # ✅ Play sound for player scoring
            self.ball.reset()

    
        # AI movement
        self.ai.auto_track(self.ball, self.height)

    def check_game_over(self, screen):
        if self.player_score >= self.winning_score or self.ai_score >= self.winning_score:
            winner_text = "Player Wins!" if self.player_score > self.ai_score else "AI Wins!"
    
            # Show winner message
            screen.fill((0, 0, 0))
            text = self.font.render(winner_text, True, WHITE)
            screen.blit(
                text,
                (
                    self.width // 2 - text.get_width() // 2,
                    self.height // 2 - text.get_height() // 2 - 40
                )
            )
    
            # Replay options
            options = [
                "Press 3 for Best of 3",
                "Press 5 for Best of 5",
                "Press 7 for Best of 7",
                "Press ESC to Exit"
            ]
            for i, opt in enumerate(options):
                opt_text = self.font.render(opt, True, WHITE)
                screen.blit(
                    opt_text,
                    (
                        self.width // 2 - opt_text.get_width() // 2,
                        self.height // 2 + i * 40
                    )
                )
    
            pygame.display.flip()
    
            # Wait for user input
            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_3:
                            self.winning_score = 2  # best of 3 → first to 2
                            waiting = False
                        elif event.key == pygame.K_5:
                            self.winning_score = 3  # best of 5 → first to 3
                            waiting = False
                        elif event.key == pygame.K_7:
                            self.winning_score = 4  # best of 7 → first to 4
                            waiting = False
                        elif event.key == pygame.K_ESCAPE:
                            pygame.quit()
                            quit()
    
            # Reset for new game
            self.player_score = 0
            self.ai_score = 0
            self.ball.reset()
            self.player.y = self.height // 2 - self.paddle_height // 2
            self.ai.y = self.height // 2 - self.paddle_height // 2

    def render(self, screen):
        # Draw paddles and ball
        pygame.draw.rect(screen, WHITE, self.player.rect())
        pygame.draw.rect(screen, WHITE, self.ai.rect())
        pygame.draw.ellipse(screen, WHITE, self.ball.rect())
        pygame.draw.aaline(screen, WHITE, (self.width//2, 0), (self.width//2, self.height))
    
        # Draw score
        player_text = self.font.render(str(self.player_score), True, WHITE)
        ai_text = self.font.render(str(self.ai_score), True, WHITE)
        screen.blit(player_text, (self.width//4, 20))
        screen.blit(ai_text, (self.width * 3//4, 20))
    
        # --- Check for game over condition ---
        self.check_game_over(screen)


