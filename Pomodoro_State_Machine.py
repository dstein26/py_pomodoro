# -*- coding: utf-8 -*-
"""
Created on Sat Sep 25 22:32:37 2021

@author: rckst
"""

from abc import ABC, abstractmethod
from enum import Enum

class Pomodoro_State_Machine:
    class State(Enum):
        UNINITIALIZED = -1
        WORKING = 0
        BREAK_SHORT = 1
        BREAK_LONG = 2
    
    _state = None    # Current state
    _cycleCount = 0  # How many cycles have passed
    _timer = None    # Timer instance
    
    def __init__(self, timer):
        self.attachTimer(timer)
        self.transition_to(State_Working())
        
    def attachTimer(self, timer):
        self._timer = timer
        self.timer.attach("time", self.timeOut)
    
    def transition_to(self, state):
        self._state = state
        self._state.context = self
        self._state.setupTimer()
        
    def timeOut(self, timer):
        self._state.timeEvent()
        
    @property
    def state(self):
        return self._state.name
    
    @property
    def timer(self):
        return self._timer
    
    @property
    def cycles(self):
        return self._cycleCount
    
    def incCycles(self):
        self._cycleCount += 1
        return self.cycles
    
    def resetCycles(self):
        self._cycleCount = 0
        
        
class Pomodoro_State(ABC):
    _state = Pomodoro_State_Machine.State.UNINITIALIZED
    _context = None
    _time = 0
    
    @property
    def time(self):
        return self._time
    
    @property
    def name(self):
        return self._name
    
    @property
    def context(self):
        return self._context
    
    @context.setter
    def context(self, context):
        self._context = context
        
    def setupTimer(self):
        self.context.timer.stop()
        self.context.timer.setTimer(self.time)
    
    @abstractmethod
    def timeEvent(self):
        pass
    
class State_Working(Pomodoro_State):
    _state = Pomodoro_State_Machine.State.WORKING
    _time = 25 # *60
    
    def timeEvent(self):   
        if (self._context.cycles < 1):
            self._context.transition_to(State_Short_Break())
        else:
            self._context.transition_to(State_Long_Break())
    
class State_Short_Break(Pomodoro_State):
    _state = Pomodoro_State_Machine.State.BREAK_SHORT
    _time = 5 # *60
    
    def timeEvent(self):
        self._context.incCycles()
        self._context.transition_to(State_Working())
    
class State_Long_Break(Pomodoro_State):
    _state = Pomodoro_State_Machine.State.BREAK_LONG
    _time = 30 # *60
    
    def timeEvent(self):
        self._context.resetCycles()
        self._context.transition_to(State_Working())
        
# Basic timer for testing    
class timerBasic:
    def stop(self):
        pass
    
    def setTimer(self, time):
        pass
    
    def attach(self, what, function):
        pass
    
if __name__ == "__main__":
    tmr = timerBasic()
    pomo = Pomodoro_State_Machine(tmr)
    pomo.timeOut(tmr)