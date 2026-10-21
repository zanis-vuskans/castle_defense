import pygame


class Button:
    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        text: str,
        font_size: int = 30,
    ):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = pygame.font.Font(None, font_size)
        self.color = (60, 60, 60)
        self.hover_color = (100, 100, 100)
        self.text_color = (255, 255, 255)

    def draw(self, screen: pygame.Surface) -> None:
        mouse_pos = pygame.mouse.get_pos()

        # Change color when hovering over the button
        color = (
            self.hover_color
            if self.rect.collidepoint(mouse_pos)
            else self.color
        )

        pygame.draw.rect(screen, color, self.rect, border_radius=8)

        # Center the text inside the button
        text_surface = self.font.render(
            self.text, True, self.text_color
        )
        text_rect = text_surface.get_rect(center=self.rect.center)

        screen.blit(text_surface, text_rect)

    def is_clicked(self, event: pygame.event.Event) -> bool:
        return (
            event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
            and self.rect.collidepoint(event.pos)
        )
