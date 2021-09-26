# -*- coding: utf-8 -*-
"""
Created on Fri Sep 24 08:27:09 2021

@author: rckst
"""

import tkinter as tk
from Timer import Timer
from Pomodoro_State_Machine import Pomodoro_State_Machine
import numpy as np
    
class GUI:
    
    _fontTime=('Bell MT', 30)
    _fontButton=('Centaur', 15)
    
    def __init__(self):
        # Initialize Timer
        self.timer = Timer()
        self.timer.setTimer(25*60)
        
        # Create window    
        self.top = tk.Tk()
        
        # Add widgets to window
        # Frames
        self.frmImage = tk.Frame(bg="red", width = 100)
        self.frmImage.pack(side=tk.LEFT, fill=tk.Y)
        self.frmTimer = tk.Frame(bg="white")
        self.frmTimer.pack(fill=tk.X)
        self.frmButtons = tk.Frame()
        self.frmButtons.pack(fill=tk.X)
        
        # Timer Label
        self.strTime = tk.StringVar()
        self.lblTime = tk.Label(master=self.frmTimer, 
                                textvariable=self.strTime,
                                font=self._fontTime)
        self.lblTime.pack()
        
        self.btnStart = tk.Button(master=self.frmButtons, 
                                  command=self.timer.start, text="Start",
                                  font=self._fontButton)
        self.btnStart.pack(side = tk.LEFT)
        
        self.btnPause = tk.Button(master=self.frmButtons, 
                                  command=self.timer.pause, text="Pause",
                                  font=self._fontButton)
        self.btnPause.pack(side = tk.LEFT)
        self.btnStop = tk.Button(master=self.frmButtons, 
                                 command=self.timer.stop, text="Stop",
                                  font=self._fontButton)
        self.btnStop.pack(side = tk.LEFT)
        
    def run(self):
        self.timeEvent()

        # Run
        self.top.mainloop()
        
    def timeEvent(self):
        t = self.timer.checkTime()
        (m, s) = convertToMS(t)
        
        self.strTime.set(f"{m:02d}:{s:02d}")
        self.top.after(300, self.timeEvent)
        

def convertToMS(time):
    m = (int) (time / 60)
    s = (int) (time % 60)
    return (m, s)
        

if __name__ == "__main__":
    gui = GUI()
    sm = Pomodoro_State_Machine(gui.timer)
    gui.run()
    
 