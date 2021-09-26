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
    _afterID = None
    
    def __init__(self, timer):
        self.timer = timer
        self.timer.attach("time", self.bringToTop)
        
        # Create TK window    
        self.top = tk.Tk()
        self.top.title("Pomodoro Timer")
        
        # Add widgets to window
        # Frames
        # TODO: Add light indicators to indicate which cycle we are on
        # TODO: create constants to manage appearance (fg and bg colors)
        self.frmImage = tk.Frame(bg="red", width = 100)
        self.frmImage.pack(side=tk.LEFT, fill=tk.Y)
        self.frmTimer = tk.Frame(bg="white")
        self.frmTimer.pack(fill=tk.X)
        self.frmButtons = tk.Frame()
        self.frmButtons.pack(fill=tk.X)
        self.frmState = tk.Frame()
        self.frmState.pack(fill=tk.X)
        
        # Labels
        # Label to display time
        self.strTime = tk.StringVar()
        self.strTime.set("MM:SS")
        self.lblTime = tk.Label(master=self.frmTimer, 
                                textvariable=self.strTime,
                                font=self._fontTime)
        self.lblTime.pack()
        
        # Label to display current state (Working, short break, long break)
        self.strState = tk.StringVar()
        self.strState.set("STATE")
        self.lblState = tk.Label(master=self.frmState,
                                 textvariable=self.strState,
                                 font=self._fontTime)
        self.lblState.pack()
        
        # Buttons
        # TODO: Buttons look should indicate which buttons can be pressed
        # Button to start timer
        self.btnStart = tk.Button(master=self.frmButtons, 
                                  command=self.timer.start, text="Start",
                                  font=self._fontButton)
        self.btnStart.pack(side = tk.LEFT)
        
        # Button to pause timer
        self.btnPause = tk.Button(master=self.frmButtons, 
                                  command=self.timer.pause, text="Pause",
                                  font=self._fontButton)
        self.btnPause.pack(side = tk.LEFT)
        
        # Button to stop timer
        # TODO: Should reset the pomo state
        self.btnStop = tk.Button(master=self.frmButtons, 
                                 command=self.timer.stop, text="Stop",
                                  font=self._fontButton)
        self.btnStop.pack(side = tk.LEFT)
        
        # Bind the close function to clear the pending after function
        self.top.protocol("WM_DELETE_WINDOW", self.onClose)
        
    # Start the GUI after everything is initialized
    def run(self):
        self.timeEvent()
        # Run
        self.top.mainloop()
        
    # Periodic event to update the time
    def timeEvent(self):
        t = self.timer.checkTime()
        (m, s) = convertToMS(t)
        
        self.strTime.set(f"{m:02d}:{s:02d}")
        self._afterID = self.top.after(300, self.timeEvent)
        
    def onClose(self):
        # Clear the after buffer to remove the annoying warnings
        self.top.after_cancel(self._afterID)
        self.top.quit()
        self.top.destroy()
        
    def bringToTop(self, timer):
        self.top.attributes('-topmost', 1)
        self.top.attributes('-topmost', 0)

def convertToMS(time):
    m = (int) (time / 60)
    s = (int) (time % 60)
    return (m, s)
        

if __name__ == "__main__":
    tmr = Timer()
    gui = GUI(tmr)
    sm = Pomodoro_State_Machine(tmr)
    gui.run()
    
 