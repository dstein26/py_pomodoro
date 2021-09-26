# -*- coding: utf-8 -*-
"""
Created on Sat Sep 25 22:32:37 2021

@author: rckst
"""

from abc import ABC, abstractmethod

class Pomodoro_State_Machine:
    _state = None
    _cycleCount = 0  # How many cycles have passed
    
    # Time variables
    _timeWork = 25
    _timeBreak = 5
    _timeBreakLong = 20
    
    def __init__(self, timer):
        timer.stop()
        timer.setTimer(self._timeWork)
        timer.attach("time", self.timeOut)
        self.transition_to(State_Working())
        
    def transition_to(self, state):
        self._state = state
        self._state.context = self
    
    def timeOut(self, timer):
        self._state.timeEvent(timer)
        
    @property
    def state(self):
        return self._state.name
        
        
class Pomodoro_State(ABC):
    _name = ""
    _context = None
    
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
    def timeEvent(self, timer):
        pass
    
class State_Working(Pomodoro_State):
    def timeEvent(self, timer):
        timer.stop()
        timer.setTimer(self.context._timeBreak)    
        self._context.transition_to(State_Short_Break())
    
class State_Short_Break(Pomodoro_State):
    def timeEvent(self, timer):
        timer.stop()
        timer.setTimer(self.context._timeWork)
        self._context.transition_to(State_Working())
    
class State_Long_Break(Pomodoro_State):
    def timeEvent(self, timer):
        timer.stop()
        timer.setTimer(self.context._timeWork)
        self._context.transition_to(State_Working())
        
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