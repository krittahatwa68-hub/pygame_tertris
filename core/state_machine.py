"""
Generic State Machine
Handles game states like menu, playing, paused
"""


class StateMachine:

    def __init__(self, initial_state):
        self._state = initial_state

    def change_state(self, new_state):
        self._state = new_state

    def get_state(self):
        return self._state

    def is_state(self, state):
        return self._state == state