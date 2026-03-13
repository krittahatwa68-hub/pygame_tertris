"""
Simple Event System
Implements Observer Pattern
"""


class EventSystem:

    def __init__(self):
        self._listeners = {}

    def subscribe(self, event_type, listener):

        if event_type not in self._listeners:
            self._listeners[event_type] = []

        self._listeners[event_type].append(listener)

    def emit(self, event_type, data=None):

        if event_type not in self._listeners:
            return

        for listener in self._listeners[event_type]:
            listener(data)