# -*- coding: utf-8 -*-
"""
Created on Fri Sep 24 09:28:14 2021

@author: rckst
"""

from abc import ABC, abstractmethod
from datetime import datetime as dt


class Timer:
    _state = None
    _lastTime = 0    # Last time called
    _time = 0        # Count Time
    _timeLeft = 0    # Time left
    _event = None
    
    _observersTrans = []    # State Transition observers
    _observersTime = []     # Time event observers
    
    # Initialize
    def __init__(self):
        self._lastTime = dt.timestamp(dt.now())
        self.transition_to(Timer_State_Stopped())
        
    # Attach an observer function
    def attach(self, what, function):
        if (what.lower() == "transition"):
            self._observersTrans.append(function)
        elif (what.lower() == "time"):
            self._observersTime.append(function)
            
    # Remove an observer funciton
    def detach(self, what, function):
        if (what.lower() == "transition"):
            self._observersTrans.remove(function)
        elif (what.lower() == "time"):
            self._observersTime.remove(function)
            
    
    # State transistion
    def transition_to(self, state):
        self._state = state
        self._state.context = self
        self._state.postTransitionEvent()
        self._lastTime = dt.timestamp(dt.now())
        
        for o in self._observersTrans:
            o(self)

    def timeEvent(self):
        for o in self._observersTime:
            o(self)
            
    @property
    def state(self):
        return self._state.name
    
    @property
    def event(self):
        return self._event
    
    @event.setter
    def event(self, event):
        self._event = event
        
    # State handles
    def setTimer(self, timerTime):
        self._state.setTime(timerTime)
    
    def checkTime(self):
        return self._state.checkTime()
    
    def start(self):
        self._state.start()
    
    def stop(self):
        self._state.stop()
        
    def pause(self):
        self._state.pause()
    
class Timer_State(ABC):
    _context = None
    _name = ""
    
    @property
    def name(self):
        return self._name
    
    @property
    def context(self):
        return self._context
    
    @context.setter
    def context(self, context):
        self._context = context
        
    @abstractmethod
    def postTransitionEvent(self):
        pass
        
    @abstractmethod
    def setTime(self, timerTime):
        pass
    
    @abstractmethod
    def checkTime(self):
        pass
    
    @abstractmethod
    def start(self):
        pass
    
    @abstractmethod
    def stop(self):
        pass
    
    @abstractmethod
    def pause(self):
        pass
    
class Timer_State_Stopped(Timer_State):
    _name = "STOPPED"
    
    def postTransitionEvent(self):
        self.context.setTimer(self.context._time)
    
    def setTime(self, timerTime):
        self.context._time = timerTime
        self.context._timeLeft = timerTime
    
    def checkTime(self):
        self.context._lastTime = dt.timestamp(dt.now())
        return self.context._timeLeft
    
    def start(self):
        self.checkTime()
        self.context.transition_to(Timer_State_Running())
        
    def pause(self):
        pass
    
    def stop(self):
        pass

class Timer_State_Running(Timer_State):
    _name = "RUNNING"
    
    def postTransitionEvent(self):
        pass
    
    def setTime(self, timerTime):
        pass
    
    def checkTime(self):
        ct = dt.timestamp(dt.now())
        t = ct - self.context._lastTime
        self.context._timeLeft -= t
        self.context._lastTime = ct
        
        if (self.context._timeLeft <= 0):
            self.context._timeLeft = 0
            self.context.timeEvent()
            self.context.transition_to(Timer_State_Paused())
            
        return self.context._timeLeft
    
    def start(self):
        pass
    
    def pause(self):
        self.context.transition_to(Timer_State_Paused())
    
    def stop(self):
        self.context.transition_to(Timer_State_Stopped())
        
class Timer_State_Paused(Timer_State):
    _name = "PAUSED"
    
    def postTransitionEvent(self):
        pass
    
    def setTime(self, timerTime):
        self.context._time = timerTime
        self.context._timeLeft = timerTime
        
    def start(self):
        self.checkTime()
        self.context.transition_to(Timer_State_Running())
    
    def stop(self):
        self.context.transition_to(Timer_State_Stopped())
        
    def pause(self):
        pass
    
    def checkTime(self):
        self.context._lastTime = dt.timestamp(dt.now())
        return self.context._timeLeft
        
        
def exampleEvent(context):
    print("Time's Up!")
    
def exampleStateEvent(context):
    print(f"Entered State {context.state}")

if __name__ == "__main__":
    import time
    tmr = Timer()
    tmr.attach("time", exampleEvent)
    tmr.attach("transition", exampleStateEvent)

    tmr.setTimer(10)
    print(tmr.checkTime())
    tmr.start()
    
    for i in range(22):
        print(tmr.checkTime())
        time.sleep(0.5)
    
    tmr.stop()
    print(tmr.checkTime())