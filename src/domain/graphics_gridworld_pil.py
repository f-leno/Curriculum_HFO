# -*- coding: utf-8 -*-
"""
Created on May 25 15:40 2017
Graphic representation of the Gridworld
@author: Leno
"""


import os
from PIL import Image, ImageDraw



class GraphicsGridworld():
    width = 800
    height = 800
    window = None
    canvas = None
    imageFolder = os.path.dirname(os.path.abspath(__file__))



    # Images
    agent = None
    treasure = None
    pit = None
    fire = None

    squareX = None
    squareY = None
    sizeX = None
    sizeY = None

    def __init__(self, environment):
        """Visual illustration of the Gridworld domain. Needs a link with the GridWorld class (environment.py)"""
        #self.window = tkinter.Tk()

        self.sizeX = environment.sizeX
        self.sizeY = environment.sizeY
        # Calculates size of each square
        if self.squareX == 1:
            self.width / self.sizeY
        else:
            self.squareX = int(self.width / self.sizeX)
        if self.sizeY == 1:
            self.squareY = int(self.height / self.sizeX)
        else:
            self.squareY = int(self.height / self.sizeY)

        self.window = Image.new('RGB', (self.width,self.height),(255, 255, 255)) #Default white background
        self.canvas = ImageDraw.Draw(self.window)

        image = Image.open(self.imageFolder + "/agent.png")
        image = image.resize((self.squareX, self.squareY), Image.ANTIALIAS)
        self.agent = image


        image = Image.open(self.imageFolder + "/treasure.png")
        image = image.resize((self.squareX, self.squareY), Image.ANTIALIAS)
        self.treasure = image


        image = Image.open(self.imageFolder + "/fire.png")
        image = image.resize((self.squareX, self.squareY), Image.ANTIALIAS)
        self.fire = image


        image = Image.open(self.imageFolder + "/pit.png")
        image = image.resize((self.squareX, self.squareY), Image.ANTIALIAS)
        self.pit = image


        # Link to environment object
        self.environment = environment

        self.draw_lines(self.squareX * self.sizeX, self.sizeY)


    def draw_map(self,sizeX,sizeY):
        for x in range(0, sizeX):
            for y in range(0, sizeY):
                x1 = self.squareX * x
                y1 = self.squareY * y
                x2 = x1 + self.squareX
                y2 = y1 + self.squareY
                self.canvas.rectangle([x1,y1,x2,y2], (255,255,255)) #White square to erase space

    def draw_lines(self, sizeX, sizeY):
        """
            Draws the lines separating 'squares'
        """

        for i in range(1, sizeX):
            self.canvas.line([self.squareX * i, 0, self.squareX * i, self.height],fill=0)

        for i in range(1, sizeY):
            self.canvas.line([0, self.squareY * i, self.width, self.squareY * i],fill=0)

    def update_state(self):
        """
            Updates the state display according to the current state of the environment.
        """
        self.clear()
        self.draw_lines(self.sizeX, self.sizeY)

        for treasure in self.environment.treasurePositions:
            self.print_obj(treasure[0], treasure[1], self.treasure)
        for fire in self.environment.firePositions:
            self.print_obj(fire[0], fire[1], self.fire)
        for pit in self.environment.pitPositions:
            self.print_obj(pit[0], pit[1], self.pit)
        self.print_obj(self.environment.agentPositions[0], self.environment.agentPositions[1], self.agent)
        #self.update_screen()

        # self.window.mainloop()

    def print_obj(self, x, y, image):
        """
            Print one object in the screen
        """
        if x >= 1 and x <= self.sizeX and y >= 1 and y <= self.sizeY:
            realX = self.squareX * (x - 1)
            realY = self.squareY * (y - 1)
            #self.canvas.create_image(realX, realY, image=image, anchor=tkinter.NW, tags='obj')
            offset = (realX,realY)
            self.window.paste(image, offset,mask=image)

    def clear(self):
        self.draw_map(self.sizeX, self.sizeY)

    def close(self):
        self.window.destroy()

    def save_to_file(self, fileName):
        self.window.save(fileName)

    def process_video(self, videoFile):
        import os
        os.system("sh "+videoFile)



