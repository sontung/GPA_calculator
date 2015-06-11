import pygame
import sys


class GameGUI:
    def __init__(self, _game_state, core_calculator):
        pygame.init()
        self.core_calculator = core_calculator
        self.sound = None
        self.buttons = []  # keeping track of number of buttons according to each scene (state)
        self.state = _game_state
        self.window_width = 1200
        self.window_height = 500
        self.font_size = 30
        self.colors = {"white": (255, 255, 255),
                       "black": (41, 36, 33),
                       "navy": (0, 0, 128),
                       "red": (139, 0, 0),
                       "light blue": (152, 245, 255),
                       "blue": (0, 0, 255),
                       "dark": (3, 54, 73),
                       "yellow": (255, 255, 0),
                       "turquoise blue": (0, 199, 140),
                       "green": (0, 128, 0),
                       "light green": (118, 238, 0),
                       "turquoise": (0, 229, 238),
                       "pink": (255, 20, 147)}
        self.text_color = self.colors["red"]
        self.bg_color = self.colors["light blue"]
        self.tile_color = self.bg_color
        self.display_surface = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption("GPA Calculator")
        self.font = pygame.font.Font("assets\\fonts\Cutie Patootie Skinny.ttf", self.font_size)
        self.font_bold = pygame.font.Font("assets\\fonts\Cutie Patootie.ttf", self.font_size)
        self.error_mess = ""

        # Display text input
        self.subj_rect = pygame.Rect(self.window_width/12-50, 100, 100, 50)
        self.grade_rect = pygame.Rect(self.window_width/4-50, 100, 100, 50)
        self.credit_rect = pygame.Rect(self.window_width/2.4-50, 100, 100, 50)
        self.subj_prompt = Prompt(self.subj_rect.topleft, self)
        self.grade_prompt = Prompt(self.grade_rect.topleft, self)
        self.credit_prompt = Prompt(self.credit_rect.topleft, self)

    def make_text(self, text, color, bg_color, center):
        """
        Make a text object for drawing
        """
        text_surf = self.font.render(text, True, color, bg_color)
        text_rect = text_surf.get_rect()
        text_rect.center = center
        return text_surf, text_rect

    def output_strings_from_prompts(self):
        """
        Return the output strings from the prompts
        :return:
        """
        return self.subj_prompt.output()[0], self.grade_prompt.output()[0], self.credit_prompt.output()[0]

    def prompt_error_message(self, val):
        """
        Prompt a message when user enter an unexpected input
        :return:
        """
        self.error_mess = val

    def reset(self):
        """
        Reset the GUI
        :return:
        """
        self.core_calculator.reset()
        self.error_mess = ""
        self.reset_prompts()

    def reset_prompts(self):
        """
        Reset the prompts
        """
        self.subj_prompt.reset()
        self.grade_prompt.reset()
        self.credit_prompt.reset()

    def draw(self, state):
        """
        Draw the scene.
        """
        self.display_surface.fill(self.bg_color)
        if state == "welcome":
            start_point = self.window_height/3
            self.new = Button('New Season', self.text_color, self.tile_color,
                              (self.window_width/2, start_point), self)
            self.quit = Button('Quit', self.text_color, self.tile_color,
                               (self.window_width/2, start_point+60*3), self)
            self.help = Button('How to use', self.text_color, self.tile_color,
                               (self.window_width/2, start_point+60), self)
            self.author = Button('About the author', self.text_color, self.tile_color,
                                 (self.window_width/2, start_point+60*2), self)
            self.buttons = [self.new, self.quit, self.help, self.author]
            self.display_surface.blit(self.new.get_sr()[0], self.new.get_sr()[1])
            self.display_surface.blit(self.quit.get_sr()[0], self.quit.get_sr()[1])
            self.display_surface.blit(self.help.get_sr()[0], self.help.get_sr()[1])
            self.display_surface.blit(self.author.get_sr()[0], self.author.get_sr()[1])

        elif state == "help":
            sys.stdin = open("instruction.txt")
            for i in range(9):
                instructions = sys.stdin.readline().strip()
                self.instructions_sur, self.instructions_rect = self.make_text(instructions, self.colors["black"],
                                                                               self.tile_color,
                                                                               (self.window_width/2,
                                                                                self.window_height/2-120+i*35))
                self.display_surface.blit(self.instructions_sur, self.instructions_rect)
            self.back = Button("Back", self.text_color, self.tile_color,
                               (self.window_width-60, self.window_height/8), self)
            self.buttons = [self.back]
            self.display_surface.blit(self.back.get_sr()[0], self.back.get_sr()[1])

        elif state == "author":
            sys.stdin = open("author.txt")
            for i in range(8):
                if i == 0:
                    instructions = sys.stdin.readline().strip()
                    self.instructions_sur, self.instructions_rect = self.make_text(instructions, self.colors["green"],
                                                                                   self.tile_color,
                                                                                   (self.window_width/2,
                                                                                    self.window_height/2-180+i*35))
                    self.display_surface.blit(self.instructions_sur, self.instructions_rect)
                else:
                    instructions = sys.stdin.readline().strip()
                    self.instructions_sur, self.instructions_rect = self.make_text(instructions, self.colors["black"],
                                                                                   self.tile_color,
                                                                                   (self.window_width/2,
                                                                                    self.window_height/2-120+i*35))
                    self.display_surface.blit(self.instructions_sur, self.instructions_rect)
            self.back = Button("Back", self.text_color, self.tile_color, (self.window_width-60, self.window_height/8), self)
            self.buttons = [self.back]
            self.display_surface.blit(self.back.get_sr()[0], self.back.get_sr()[1])

        elif state == "new game":
            self.buttons = []
            subj_sur, subj_rect = self.make_text("Subject", self.colors["green"], self.tile_color,
                                                 (self.window_width/12, 50))
            grade_sur, grade_rect = self.make_text("Grade", self.colors["green"], self.tile_color,
                                                   (self.window_width/4, 50))
            credit_sur, credit_rect = self.make_text("Credits", self.colors["green"], self.tile_color,
                                                     (self.window_width/2.4, 50))
            self.display_surface.blit(subj_sur, subj_rect)
            self.display_surface.blit(grade_sur, grade_rect)
            self.display_surface.blit(credit_sur, credit_rect)
            pygame.draw.rect(self.display_surface, self.colors["white"], self.subj_rect)
            pygame.draw.rect(self.display_surface, self.colors["white"], self.grade_rect)
            pygame.draw.rect(self.display_surface, self.colors["white"], self.credit_rect)

            # Display text input
            self.display_surface.blit(self.subj_prompt.output()[1], self.subj_prompt.output()[2])
            self.display_surface.blit(self.grade_prompt.output()[1], self.grade_prompt.output()[2])
            self.display_surface.blit(self.credit_prompt.output()[1], self.credit_prompt.output()[2])

            # Submit button
            self.submit = Button("Submit", self.text_color, self.tile_color, (self.window_width/4, 200), self)
            self.display_surface.blit(self.submit.get_sr()[0], self.submit.get_sr()[1])

            # Done button
            self.done = Button("Done", self.text_color, self.tile_color, (self.window_width/4, 250), self)
            self.display_surface.blit(self.done.get_sr()[0], self.done.get_sr()[1])
            self.buttons = [self.submit, self.done]

            # Display error message
            error_sur, error_rect = self.make_text(self.error_mess, self.colors["pink"], self.tile_color,
                                                   (self.window_width/2, self.window_height/2+100))
            self.display_surface.blit(error_sur, error_rect)

            # Display data
            data_dict = self.core_calculator.get_data_display()
            for index in data_dict:
                subject, grade, credit = data_dict[index]
                subj_sur2, subj_rect2 = self.make_text(subject, self.colors["navy"], self.tile_color,
                                                       (7*self.window_width/12, 50+index*50))
                grade_sur2, grade_rect2 = self.make_text(grade, self.colors["navy"], self.tile_color,
                                                         (9*self.window_width/12, 50+index*50))
                credit_sur2, credit_rect2 = self.make_text(credit, self.colors["navy"], self.tile_color,
                                                           (11*self.window_width/12, 50+index*50))
                self.display_surface.blit(subj_sur2, subj_rect2)
                self.display_surface.blit(grade_sur2, grade_rect2)
                self.display_surface.blit(credit_sur2, credit_rect2)

        elif state == "displaying results":
            self.back = Button("Back", self.text_color, self.tile_color,
                               (self.window_width-60, self.window_height/8), self)
            self.buttons = [self.back]
            self.display_surface.blit(self.back.get_sr()[0], self.back.get_sr()[1])
            result_sur, result_rect = self.make_text("Your GPA: %s" % str(self.core_calculator.get_result()),
                                                     self.text_color, self.tile_color,
                                                     (self.window_width/2, self.window_height/2))
            credit_sur, credit_rect = self.make_text("Your total credits: %s" %
                                                     str(self.core_calculator.get_total_credits()),
                                                     self.text_color, self.tile_color,
                                                     (self.window_width/2, self.window_height/2+50))
            self.display_surface.blit(result_sur, result_rect)
            self.display_surface.blit(credit_sur, credit_rect)

class Button:
    def __init__(self, text, color, bg_color, center, _game_gui):
        self.gui = _game_gui
        self.text = text
        self.center = center
        self.color = color
        self.bg_color = bg_color
        self.bold = False
        self.font = self.gui.font
        self.font_bold = self.gui.font_bold
        self.surf = self.font.render(text, True, color, bg_color)
        self.rect = self.surf.get_rect()
        self.rect.center = self.center

    def make_text(self):
        """
        Make a text object for drawing
        """
        if not self.bold:
            text_surf = self.font.render(self.text, True, self.color, self.bg_color)
        else:
            text_surf = self.font_bold.render(self.text, True, self.color, self.bg_color)
        text_rect = text_surf.get_rect()
        text_rect.center = self.center
        return text_surf, text_rect

    def get_rect(self):
        return self.rect

    def get_sr(self):
        return self.surf, self.rect

    def update_sr(self):
        self.surf, self.rect = self.make_text()

    def set_bold(self, pos):
        """
        Highlight the button when the user hovers mouse over
        """
        if self.rect.collidepoint(pos):
            self.bold = True
            self.update_sr()
            self.gui.display_surface.blit(self.surf, self.rect)

class Prompt:
    def __init__(self, topleft, _gui):
        self.string = ""
        self.color = _gui.text_color
        self.bg_color = _gui.colors["white"]
        self.topleft = topleft  # position where the string is supposed to be displayed
        self.font = _gui.font

    def make_text(self):
        """
        Make a text object for drawing
        """
        text_surf = self.font.render(self.string, True, self.color, self.bg_color)
        text_rect = text_surf.get_rect()
        text_rect.topleft = self.topleft
        return text_surf, text_rect

    def take_char(self, char):
        """
        Take in character or delete previous one.
        :return:
        """
        if char != "del":
            if len(self.string) <= 8:
                self.string += char
        else:
            self.string = self.string[:-1]

    def output(self):
        """
        Output the string
        :return:
        """
        sur, rect = self.make_text()
        return self.string, sur, rect

    def reset(self):
        """
        Reset the prompt
        :return:
        """
        self.string = ""
