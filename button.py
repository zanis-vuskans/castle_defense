# button.py
import pygame

class Button:
    def __init__(self, x, y, width, height, text, padding=10):
        self.rect = pygame.Rect(x, y, width, height)
        self.padding = padding
        self.enabled = True
        self.font = pygame.font.Font(None, 24)
        self.text = ""
        self.set_text(text)

    def set_text(self, text):
        if text == self.text:
            return
        self.text = text
        text_width = self.font.size(text)[0]  # (width, height) without rendering
        anchor = self.rect.bottomright        # remember the anchored corner
        self.rect.width = text_width + self.padding * 2
        self.rect.bottomright = anchor        # grow leftward, stay in the corner

    def draw(self, screen):
        bg = (70, 130, 180) if self.enabled else (60, 60, 60)
        fg = (255, 255, 255) if self.enabled else (120, 120, 120)

        pygame.draw.rect(screen, bg, self.rect, border_radius=8)
        label = self.font.render(self.text, True, fg)
        screen.blit(label, label.get_rect(center=self.rect.center))

    def is_clicked(self, pos):
        return self.enabled and self.rect.collidepoint(pos)