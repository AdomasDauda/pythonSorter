from PIL import Image, ImageTk

import tkinter as tk, tkinter.ttk as ttk
from typing import Union
import textwrap
import itertools
from textwrap import fill
from textwrap import wrap
from itertools import zip_longest

from matplotlib import lines

Widget = Union[tk.Widget, ttk.Widget]



class ToolTip(tk.Toplevel):
    #amount to adjust fade by on every animation frame
    FADE_INC:float = .07
    #amount of milliseconds to wait before next animation state
    FADE_MS :int   = 20
    
    def __init__(self, master, **kwargs):
        tk.Toplevel.__init__(self, master)
        #make window invisible, on the top, and strip all window decorations/features
        self.attributes('-alpha', 0, '-topmost', True)
        self.overrideredirect(1)
        #style and create label. you can override style with kwargs
        style = dict(bd=2, font='Century', bg='white', anchor='w')
        self.label = tk.Label(self, **{**style, **kwargs})
        self.label.grid(row=0, column=0, sticky='w')
        #used to determine if an opposing fade is already in progress
        self.fout:bool = False
        global descripDictionary
        global descriptionsFile
        descripDictionary = {
        "selection": 0,
        "bubble": 1,
        "quick": 2,
        "shell": 3,
        "heap": 4,
        "gnome": 5,
        "slider": 6,
        "widthOfTheBars": 7
        }
        descriptionsFile = open('descriptions.txt', 'r')
        lines = descriptionsFile.readlines()
        global listOfDescriptions
        listOfDescriptions = []
        for line in lines:
            listOfDescriptions.append("{}".format(line.strip()))
    def bind(self, target:Widget, type:str, **kwargs):
        #bind Enter(mouseOver) and Leave(mouseOut) events to the target of this tooltip


        descriptionType = descripDictionary.get(f"{type}")
        #print(descriptionType, type)
        description = listOfDescriptions[descriptionType]
        target.bind('<Enter>', lambda e: self.fadein(0, f"{description}", e))
        target.bind('<Leave>', lambda e: self.fadeout(1-ToolTip.FADE_INC, e))
        
    def fadein(self, alpha:float, text:str=None, event:tk.Event=None):
        #if event and text then this call came from target
        #~ we can consider this a "fresh/new" call
        if event and text:
            #if we are in the middle of fading out jump to end of fade
            if self.fout:
                self.attributes('-alpha', 0)
                #indicate that we are fading in
                self.fout = False
            #assign text to label
            self.label.configure(text=formatItem(left=text))
            #update so the proceeding geometry will be correct
            self.update()
            #x and y offsets
            offset_x = event.widget.winfo_width()+20
            offset_y = int((event.widget.winfo_height()-self.label.winfo_height()))
            #get geometry
            w = self.label.winfo_width()
            h = self.label.winfo_height()
            x = event.widget.winfo_rootx()+offset_x
            y = event.widget.winfo_rooty()+offset_y
            #apply geometry
            self.geometry(f'{w}x{h}+{x}+{y}')
               
        #if we aren't fading out, fade in
        if not self.fout:
            self.attributes('-alpha', alpha)
        
            if alpha < 1:
                self.after(ToolTip.FADE_MS, lambda: self.fadein(min(alpha+ToolTip.FADE_INC, 1)))

    def fadeout(self, alpha:float, event:tk.Event=None):
        #if event then this call came from target 
        #~ we can consider this a "fresh/new" call
        if event:
            #indicate that we are fading out
            self.fout = True
        
        #if we aren't fading in, fade out        
        if self.fout:
            self.attributes('-alpha', alpha)
        
            if alpha > 0:
                self.after(ToolTip.FADE_MS, lambda: self.fadeout(max(alpha-ToolTip.FADE_INC, 0)))


from textwrap import fill

def formatItem(left):
    width = 30
    for i in range(30, round(len(left)/2)):
        if len(left) % i == 0:
            width = i
        if len(left) % i == len(left) - 1:
            width = i
        i += 1
    wrapped = fill(left, width=width, subsequent_indent=' '*0)
    return '{1}'.format(left, wrapped)


