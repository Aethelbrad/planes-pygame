import pygame
import sys
from settings import *


# 1. The Base State Class
class BaseState:
    """
    An abstract base class for all game states.
    """
    def __init__(self, game):
        self.game = game # Store a reference to the main game object

    def handle_events(self, events):
        """Handle all user input for this state."""
        # Default behavior: check for quit
        for event in events:
            if event.type == pygame.QUIT:
                return "QUIT" # Signal to the game to quit
        return self.get_next_state() # Return key for the next state

    def update(self, delta_time):
        """Update game logic for this state."""
        pass # Most states will override this

    def draw(self, screen):
        """Draw all graphics for this state."""
        pass # Most states will override this
    
    def get_next_state(self):
        """Return the key for the next state (or self)."""
        return "SELF" # Default: stay in this state

# 2. Concrete State Classes

class PlayingState(BaseState):
    def __init__(self, game):
        super().__init__(game)

    def handle_events(self, events):
        # First, check for generic events (like quit)
        next_state_key = super().handle_events(events)
        if next_state_key != "SELF":
            return next_state_key # e.g., "QUIT"

        # Handle state-specific inputs
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p or event.key == pygame.K_ESCAPE:
                    return "PAUSED" # Signal to transition to PAUSED
        
        # Pass keys to player update
        self.game.keys = pygame.key.get_pressed()
        return "SELF" # Stay in PLAYING state

    def update(self, delta_time):
        # All of your game logic from Game.update() goes here
        self.game.player.update(self.game.keys, delta_time)
        if self.game.keys[pygame.K_SPACE]:
            self.game.handle_shooting()

        self.game.spawn_enemy()
        self.game.handle_collisions()

        self.game.enemies.update()
        self.game.bullets.update()

        # Check for state transition
        if self.game.player.health <= 0:
            print("Shot Down")
            return "GAME_OVER" # Signal to transition
        
        return "SELF" # Stay in PLAYING state

    def draw(self, screen):
        # All of your main drawing logic from Game.draw()
        screen.fill(WHITE)
        self.game.all_sprites.draw(screen)
        self.game.hud.draw(screen, self.game.player, self.game.clock)


class PausedState(BaseState):
    def __init__(self, game):
        super().__init__(game)
        # Pre-render text surfaces
        self.overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        self.overlay.fill((0, 0, 0, 180))
        
        self.pause_text = self.game.big_font.render("PAUSED", True, WHITE)
        self.resume_text = self.game.font.render("Press 'R' or 'P' to Resume", True, WHITE)
        self.quit_text = self.game.font.render("Press 'Q' to Quit", True, WHITE)
        
        self.p_rect = self.pause_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        self.r_rect = self.resume_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))
        self.q_rect = self.quit_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 70))

    def handle_events(self, events):
        next_state_key = super().handle_events(events)
        if next_state_key != "SELF":
            return next_state_key # "QUIT"

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p or event.key == pygame.K_ESCAPE or event.key == pygame.K_r:
                    return "PLAYING" # Signal to resume
                if event.key == pygame.K_q:
                    return "QUIT" # Signal to quit
        return "SELF"

    def update(self, delta_time):
        # Nothing happens when paused!
        pass

    def draw(self, screen):
        # IMPORTANT: Draw the playing screen *first*
        self.game.states["PLAYING"].draw(screen)
        
        # Then draw the pause overlay and text on top
        screen.blit(self.overlay, (0, 0))
        screen.blit(self.pause_text, self.p_rect)
        screen.blit(self.resume_text, self.r_rect)
        screen.blit(self.quit_text, self.q_rect)


class GameOverState(BaseState):
    def __init__(self, game):
        super().__init__(game)
        # Pre-render text surfaces
        self.overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        self.overlay.fill((0, 0, 0, 180))

        self.game_over_text = self.game.big_font.render("Shot Down", True, RED)
        self.score_text = self.game.font.render(f"Final Score: {self.game.player.score}", True, WHITE) # Use WHITE for dark bg
        self.quit_text = self.game.font.render("Press ENTER to Quit", True, WHITE) # Use WHITE
        
        self.go_rect = self.game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        self.score_rect = self.score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))
        self.quit_rect = self.quit_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 70))

    def handle_events(self, events):
        next_state_key = super().handle_events(events)
        if next_state_key != "SELF":
            return next_state_key # "QUIT"
        
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return "QUIT" # Signal to quit
        return "SELF"

    def update(self, delta_time):
        # Nothing happens on game over screen
        pass

    def draw(self, screen):
        # Draw the final playing screen *first*
        self.game.states["PLAYING"].draw(screen)
        
        # Then draw the game over overlay and text
        screen.blit(self.overlay, (0, 0))
        screen.blit(self.game_over_text, self.go_rect)
        screen.blit(self.score_text, self.score_rect)
        screen.blit(self.quit_text, self.quit_rect)