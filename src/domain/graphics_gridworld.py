# -*- coding: utf-8 -*-
"""
Created on May 25 15:40 2017
Graphic representation of the Gridworld
@author: Leno
"""

import tkinter
import os
from PIL import Image, ImageTk
import pyscreenshot as ImageGrab #Only works for Linux (Maybe use ImageGrab from PIL package for Windows/Mac)

class GraphicsGridworld():
    width = 800
    height = 800    
    window = None
    canvas = None
    imageFolder = os.path.dirname(os.path.abspath(__file__))

    imageRepo = [] #preventing garbage collection
    
    #Images
    agent = None
    treasure = None
    pit = None
    fire = None
    
    squareX = None
    squareY = None
    sizeX = None
    sizeY = None


    
    
    def __init__(self,environment):
        """Visual illustration of the Gridworld domain. Needs a link with the GridWorld class (environment.py)"""
        self.window = tkinter.Tk()
        
        self.sizeX = environment.sizeX
        self.sizeY = environment.sizeY
        #Calculates size of each square
        if self.squareX==1:
             self.width / self.sizeY
        else:
            self.squareX = int(self.width / self.sizeX)
        if self.sizeY==1:
             self.squareY = int(self.height / self.sizeX)
        else:
             self.squareY = int(self.height / self.sizeY)
        
        self.canvas = tkinter.Canvas(self.window,width=self.squareX * self.sizeX, height=self.squareY * self.sizeY)


        
        
        image = Image.open(self.imageFolder + "/agent.png")
        image = image.resize((self.squareX, self.squareY), Image.ANTIALIAS)
        self.agent = ImageTk.PhotoImage(image)
        self.imageRepo.append(image)
        
        image = Image.open(self.imageFolder + "/treasure.png")
        image = image.resize((self.squareX, self.squareY), Image.ANTIALIAS)
        self.treasure = ImageTk.PhotoImage(image)
        self.imageRepo.append(image)

        image = Image.open(self.imageFolder + "/fire.png")
        image = image.resize((self.squareX, self.squareY), Image.ANTIALIAS)
        self.fire = ImageTk.PhotoImage(image)
        self.imageRepo.append(image)

        image = Image.open(self.imageFolder + "/pit.png")
        image = image.resize((self.squareX, self.squareY), Image.ANTIALIAS)
        self.pit = ImageTk.PhotoImage(image)
        self.imageRepo.append(image)

        #Link to environment object        
        self.environment = environment
        
        self.draw_lines(self.squareX * self.sizeX,self.sizeY)
        self.update_screen()
        
        

    def draw_lines(self,sizeX,sizeY):
        """
            Draws the lines separating 'squares'
        """
        for i in range(1,sizeX):
            self.canvas.create_line(self.squareX*i,0,self.squareX*i,self.height)
            
        for i in range(1,sizeY):
            self.canvas.create_line(0,self.squareY*i,self.width,self.squareY*i)
            
    def update_state(self):
        """
            Updates the state display according to the current state of the environment.
        """
        self.clear()
        self.draw_lines(self.sizeX,self.sizeY)

        for treasure in self.environment.treasurePositions:
            self.print_obj(treasure[0],treasure[1],self.treasure)
        for fire in self.environment.firePositions:
            self.print_obj(fire[0],fire[1],self.fire)
        for pit in self.environment.pitPositions:
            self.print_obj(pit[0],pit[1],self.pit)
        self.print_obj(self.environment.agentPositions[0],self.environment.agentPositions[1],self.agent)
        self.update_screen()
        
    def update_screen(self):
        self.canvas.pack()
        self.canvas.update()
        self.window.update()

        
        #self.window.mainloop()
        
            
    def print_obj(self,x,y,image):
        """
            Print one object in the screen
        """
        if x>=1 and x<=self.sizeX and y>=1 and y<=self.sizeY:
            realX = self.squareX*(x-1)
            realY = self.squareY*(y-1)
            self.canvas.create_image(realX, realY, image = image, anchor = tkinter.NW,tags = 'obj')

    def clear(self):
        self.canvas.delete('obj')        
      
    def close(self):
        self.window.destroy()
        
    def save_to_file(self,fileName):
        grab = ImageGrab.grab(bbox=(self.canvas.winfo_rootx(),
                                    self.canvas.winfo_rooty(),
                                    self.canvas.winfo_rootx()+self.canvas.winfo_width(),
                                    self.canvas.winfo_rooty() + self.canvas.winfo_height(),
                                    ))
        grab.save(fileName)

        

