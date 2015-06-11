import pygame
import gui
import state
import event_handler
import core


if __name__ == "__main__":
    FPS_clock = pygame.time.Clock()
    core_calculator = core.Core()
    game_state = state.GameState()
    game_gui = gui.GameGUI(game_state, core_calculator)
    game_event_handler = event_handler.EventLogic(game_state, game_gui, core_calculator)
    game_gui.draw(game_state.get_state())
    pygame.display.update()
    while True:
        game_gui.draw(game_state.get_state())
        game_event_handler.event_handler()
        pygame.display.update()
        FPS_clock.tick(30)