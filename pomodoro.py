# -*- coding: utf-8 -*-
"""
Created on Fri Sep 24 08:27:09 2021

@author: rckst
"""

import tkinter as tk
from Timer import Timer


        
def buttonPress(event):
    print("Button Pressed")
    

if __name__ == "__main__":
    # Init timer class
    timer = Timer()
    
    # Create window    
    top = tk.Tk()
    
    # Add widgets to window
    # Frames
    frmImage = tk.Frame(bg="red", width = 100)
    frmImage.pack(side=tk.LEFT, fill=tk.Y)
    frmTimer = tk.Frame(bg="white")
    frmTimer.pack(fill=tk.X)
    frmButtons = tk.Frame()
    frmButtons.pack(fill=tk.X)
    
    # Timer Label
    lblTime = tk.Label(master=frmTimer, text="00:00")
    lblTime.pack()
    
    btnStart = tk.Button(master=frmButtons, text="Start")
    btnStart.pack(side = tk.LEFT)
    
    btnPause = tk.Button(master=frmButtons, text="Pause")
    btnPause.pack(side = tk.LEFT)
    btnStop = tk.Button(master=frmButtons, text="Stop")
    btnStop.pack(side = tk.LEFT)
    
    
    # Run
    top.mainloop()
 