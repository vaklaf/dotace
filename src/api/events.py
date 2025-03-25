
'''
This module provides a simple event system for the API. 
It allows to subscribe to events and post them to all subscribers.
'''

subscribers = {}

def subscirbe(event: str, callback) -> None:
    '''Subscribes a callback to an event'''
    if event not in subscribers:
        subscribers[event] = []
    subscribers[event].append(callback)

def post_event(event: str, data: dict) -> None:
    '''Posts an event to all subscribers'''
    if event in subscribers:
        for callback in subscribers[event]:
            callback(data)
    else:
        raise ValueError(f'Event {event} has no subscribers')
