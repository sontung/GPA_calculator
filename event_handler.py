import pygame
import sys
from pygame.locals import *


class EventLogic:
    def __init__(self, _game_state, _game_gui, core_calculator):
        self._game_state = _game_state
        self._game_gui = _game_gui
        self.error_message = ""
        self.current_prompt = None
        self.core_calculator = core_calculator

    def check_mouse_click(self, pos):
        """
        Determine which box user just clicks
        :param pos:
        :return:
        """
        if self._game_gui.subj_rect.collidepoint(pos):
            self.current_prompt = "subj"
        elif self._game_gui.grade_rect.collidepoint(pos):
            self.current_prompt = "grade"
        elif self._game_gui.credit_rect.collidepoint(pos):
            self.current_prompt = "credit"
        else:
            self.current_prompt = None
        return self.current_prompt

    def valid_input(self):
        """
        Valid the string inputs from user
        :return:
        """
        grade = self._game_gui.grade_prompt.output()[0]
        credit = self._game_gui.credit_prompt.output()[0]
        error_id = 0
        try:
            dummy_var = float(grade)
        except ValueError:
            error_id += 1

        try:
            dummy_var = float(credit)
        except ValueError:
            error_id += 2

        if error_id == 0:
            self.error_message = ""
        elif error_id == 1:
            self.error_message = "Error! Grade and Credit blanks take only integers and floats." \
                                 " Check your input for Grade again!"
        elif error_id == 2:
            self.error_message = "Error! Grade and Credit blanks take only integers and floats." \
                                 " Check your input for Credit again!"
        elif error_id == 3:
            self.error_message = "Error! Grade and Credit blanks take only integers and floats." \
                                 " Check your input for Grade and Credit again!"

    def quit(self):
        pygame.quit()
        sys.exit()

    def send_char_to_prompt(self, val):
        """
        Send character to the current prompt
        :param val:
        :return:
        """
        if self.current_prompt == "subj":
            self._game_gui.subj_prompt.take_char(val)
        elif self.current_prompt == "grade":
            self._game_gui.grade_prompt.take_char(val)
        elif self.current_prompt == "credit":
            self._game_gui.credit_prompt.take_char(val)
        elif self.current_prompt is None:
            pass

    def event_handler(self):
        event = pygame.event.poll()
        if event.type == MOUSEBUTTONUP:
            if self._game_state.get_state() == "welcome":
                if self._game_gui.new.get_rect().collidepoint(event.pos):
                    self._game_state.set_state("new game")
                elif self._game_gui.help.get_rect().collidepoint(event.pos):
                    self._game_state.set_state("help")
                elif self._game_gui.author.get_rect().collidepoint(event.pos):
                    self._game_state.set_state("author")
                elif self._game_gui.quit.get_rect().collidepoint(event.pos):
                    self.quit()
            elif self._game_state.get_state() in ["help", "author"]:
                if self._game_gui.back.get_rect().collidepoint(event.pos):
                    self._game_state.set_state("welcome")
            elif self._game_state.get_state() == "new game":
                self.check_mouse_click(event.pos)
                self.error_message = ""
                self._game_gui.prompt_error_message(self.error_message)
                if self._game_gui.submit.get_rect().collidepoint(event.pos):
                    self.valid_input()
                    self._game_gui.prompt_error_message(self.error_message)
                    if self.error_message == "":
                        self.core_calculator.take_data(self._game_gui.output_strings_from_prompts())
                    self._game_gui.reset_prompts()
                elif self._game_gui.done.get_rect().collidepoint(event.pos):
                    self._game_state.set_state("displaying results")
                    self.core_calculator.calculate()
            elif self._game_state.get_state() == "displaying results":
                if self._game_gui.back.get_rect().collidepoint(event.pos):
                    self._game_state.set_state("welcome")
                    self._game_gui.reset()

        elif event.type == MOUSEMOTION or event.type == NOEVENT:
            if self._game_gui.buttons:
                self._game_gui.draw(self._game_state.get_state())
                for button in self._game_gui.buttons:
                    button.set_bold(pygame.mouse.get_pos())
                pygame.display.update()

        elif event.type == pygame.QUIT:
            self.quit()

        elif event.type == KEYDOWN:
            if self._game_state.get_state() == "new game":
                if event.key in range(97, 123) or event.key in range(48, 58) or event.key in range(256, 267):
                    self.send_char_to_prompt(event.unicode)
                elif event.key == K_BACKSPACE:
                    self.send_char_to_prompt("del")