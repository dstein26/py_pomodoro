# -*- coding: utf-8 -*-
"""
Created on Fri Sep 24 08:27:09 2021

@author: rckst
"""

import tkinter as tk
from Timer import Timer
import numpy as np
    
class GUI:
    def __init__(self):
        # Initialize Timer
        self.timer = Timer()
        self.timer.setTimer(120)
        
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
                                font=('Helvatical bold',30))
        self.lblTime.pack()
        
        self.btnStart = tk.Button(master=self.frmButtons, 
                                  command=self.timer.start, text="Start")
        self.btnStart.pack(side = tk.LEFT)
        
        self.btnPause = tk.Button(master=self.frmButtons, 
                                  command=self.timer.pause, text="Pause")
        self.btnPause.pack(side = tk.LEFT)
        self.btnStop = tk.Button(master=self.frmButtons, 
                                 command=self.timer.stop, text="Stop")
        self.btnStop.pack(side = tk.LEFT)
    
    
        self.timeEvent()
        
        # Run
        self.top.mainloop()
        
    def timeEvent(self):
        t = self.timer.checkTime()
        (m, s) = convertToMS(t)
        
        self.strTime.set(f"{m}:{s:02d}")
        self.top.after(300, self.timeEvent)
        

def convertToMS(time):
    m = (int) (time / 60)
    s = (int) (time % 60)
    return (m, s)
        

if __name__ == "__main__":
    gui = GUI()
    
    
 