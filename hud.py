# hud.py
from constants import SCREEN_WIDTH

class HUD:
    def __init__(self, screen, font):
        self.screen = screen
        self.font = font

    def draw_health(self, player):
        health_text = self.font.render(f"Health: {player.health}", True, (255, 255, 255))
        self.screen.blit(health_text, (10, 10))

    def draw_score(self, player):
        score_text = self.font.render(f"Score: {player.score}", True, (255, 255, 255))
        self.screen.blit(score_text, (SCREEN_WIDTH - 150, 10))