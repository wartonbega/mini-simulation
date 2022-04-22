from locale import D_T_FMT
import pygame
import os

class animation:
    def __init__(self, images, frequency = 5, time = 0):

        self._frames = []
        self._scaled_frames = []
        self.time = time
        self._d_time = 0
        self.frequency = frequency

        dir = os.listdir(images)
        dir.sort()
        for i in dir:
            if ".png" in i:
                self._frames.append(pygame.image.load(images+i))    
                
                self._scaled_frames.append(pygame.image.load(images+i))    
        
        self._current_frame = 0

    def image(self, time):
        self._d_time = time - self.time
        if self._d_time >= self.frequency:
            self._current_frame += 1
            self._current_frame %= len(self._frames)
            self.time = time
        
        return self._scaled_frames[self._current_frame]
        

    def rescale(self, side):
        for i in range(len(self._frames)):
            self._scaled_frames[i] = pygame.transform.scale(self._frames[i], (side, side))
