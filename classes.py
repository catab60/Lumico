import pygame

PrimaryColor = (30, 30, 30)
SecondaryColor = (50,50,50)
class Button:
    def __init__(self, x, y, w, h, text, callback, color, hovered_color, fg, font_size=26, font=None):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.callback = callback
        self.was_pressed = False

        self.color = color
        self.hovered_color = hovered_color
        self.foreground_color = fg
        if font == None:
            self.font = pygame.font.SysFont("Century Gothic", font_size)
        else:
            self.font = font

    def draw(self, surface):
        mouse_pos = pygame.mouse.get_pos()
        is_hovered = self.rect.collidepoint(mouse_pos)
        color = self.color if is_hovered else self.hovered_color
        pygame.draw.rect(surface, color, self.rect)
        text_surf = self.font.render(self.text, True, self.foreground_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def handle_event(self, event):
    # only react to left‐click (button 1)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.was_pressed = True

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.was_pressed and self.rect.collidepoint(event.pos):
                self.callback()
            self.was_pressed = False




import pygame

class Checkbox:
    def __init__(self, x, y, size, id, text=""):
        # Colors

        self.color_active = (73, 159, 102)
        self.color_inactive = PrimaryColor
        self.border_color = (20,20,20)
        self.background_color = PrimaryColor

        # Rectangles
        self.rect = pygame.Rect(x + 20, y + 25, size, size)
        self.frame = pygame.Rect(x, y, 400, 100)

        # Identification and state
        self.id = id
        self.text = text
        self.active = False

        # Font for rendering text
        self.font = pygame.font.SysFont('centurygothic', 24)

    def handle_event(self, event):
        """
        Call this method from your main event loop to handle mouse clicks.
        Toggles the checkbox if clicked.
        """
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
                # Optional callback or event posting could go here

    def draw(self, surface):
        # Draw background frame
        pygame.draw.rect(surface, SecondaryColor, self.frame)

        # Draw checkbox (filled)
        fill_color = self.color_active if self.active else self.color_inactive
        pygame.draw.rect(surface, fill_color, self.rect)
        pygame.draw.rect(surface, self.border_color, self.rect, 5)

        # Draw label text
        if self.text:
            text_surface = self.font.render(self.text, True, (250,250,250))
            text_rect = text_surface.get_rect()
            text_rect.topleft = (self.rect.right + 10, self.rect.top + 10)
            surface.blit(text_surface, text_rect)




class TextEntry:
    def __init__(self, rect, bg_color=PrimaryColor, font_color=(250,250,250)):
        self.rect = pygame.Rect(rect)
        self.font = pygame.font.SysFont("Century Gothic", 30)
        self.bg_color = bg_color
        self.font_color = font_color
        self.text = ''
        self.active = False

        # Pre-render a surface for the background
        self.surface = pygame.Surface(self.rect.size)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Toggle active state if click inside
            if self.rect.collidepoint(event.pos):
                self.active = True
            else:
                self.active = False
        if self.active and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.key == pygame.K_RETURN:
                # You could handle Enter here if desired
                self.active = False
            else:
                self.text += event.unicode

    def draw(self, screen):
        # Draw background
        self.surface.fill(self.bg_color)

        # Render text
        txt_surf = self.font.render(self.text, True, self.font_color)
        txt_rect = txt_surf.get_rect(midleft=(5, self.rect.height // 2))
        self.surface.blit(txt_surf, txt_rect)

        # Optionally draw a border when active
        if self.active:
            pygame.draw.rect(self.surface, self.font_color, self.surface.get_rect(), 2)

        # Blit to main screen
        screen.blit(self.surface, self.rect.topleft)


