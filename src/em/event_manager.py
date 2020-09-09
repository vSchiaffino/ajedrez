import threading
from pydispatch import dispatcher


class Event_manager():
    def __init__(self, daemon):
        dispatcher.connect(self.post, signal='post')
        dispatcher.connect(self.subscribe, signal='subscribe')
        self.listeners = {
            "generic_event": [],
            'square_clicked': [],
            "game_ended": [],
            "new_game": []
        }

    def subscribe(self, event_name, listener):
        self.listeners[event_name].append(listener)

    def post(self, event):
        print(f"[EVENT] new event: {event.name}")
        for listener in self.listeners[event.name]:
            listener.notify(event)
