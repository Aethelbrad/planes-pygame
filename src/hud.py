from src.settings import Settings

class HUD:
    def __init__(self, font):
        self.font = font

    def draw(self, screen, player, fps):
        # Health Text
        health_text = self.font.render(f"Health: {player.health}", True, Settings.Colors.BLACK)
        screen.blit(health_text, (10, 10))

        # Score Text
        score_text = self.font.render(f"Score: {player.score}", True, Settings.Colors.BLACK)
        score_rect = score_text.get_rect(topright=(Settings.Screen.WIDTH - 10, 10))
        screen.blit(score_text, score_rect)

        # Framerate
        fps_text = self.font.render(f"FPS: {fps}", True, Settings.Colors.BLACK)
        fps_rect = fps_text.get_rect(topright=(Settings.Screen.WIDTH - 10, 40))
        screen.blit(fps_text, fps_rect)
        
        # Health Bar
        # fill = (player.health / Settings.Player.MAX_HEALTH) * Settings.HUD.HEALTH_BAR_W
        # outline_rect = pygame.Rect(10, 40, Settings.HUD.HEALTH_BAR_W, Settings.HUD.HEALTH_BAR_H)
        # fill_rect = pygame.Rect(10, 40, fill, Settings.HUD.HEALTH_BAR_H)
        # pygame.draw.rect(screen, Settings.Colors.RED, fill_rect)
        # pygame.draw.rect(screen, Settings.Colors.WHITE, outline_rect, 2)