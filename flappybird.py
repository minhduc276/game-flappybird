import math
import os
from random import randint
from collections import deque

import pygame
from pygame.locals import *

#base variable

FPS = 60 

ANIMATION_SPEED = 0.18
WIN_WIDTH = 284 * 2 
WIN_HEIGHT = 512

class Bird(pygame.sprite.Sprites):
	"""create chim"""
	WIDTH = HEIGHT = 32
	SINK_SPEED = 0.18			#Toc do di xuong cua chim (pixel/miliseconds)
	CLIMB_SPEED = 0.3 			#Toc do di len cua chim
	CLIMB_DURATION = 333.3 		#msec can thiet de chim di len

	def __init__(self, x, y, msec_to_climb, images):
		"""Khoi tao chim"""
		super(Bird, self).__init__()
        self.x, self.y = x, y
        self.msec_to_climb = msec_to_climb			#So giay con lai cho 1 lan di len
        self._img_wingup, self._img_wingdown = images
        self._mask_wingup = pygame.mask.from_surface(self._img_wingup)
        self._mask_wingdown = pygame.mask.from_surface(self._img_wingdown)

    
    def update(self, delta_frames=1): 			#So luong khung hinh = 1
    	"""Cap nhat vi tri cua chim qua tung khung hinh"""
        if self.msec_to_climb > 0:				#Neu > 0 se tu dong giam
            frac_climb_done = 1 - self.msec_to_climb/Bird.CLIMB_DURATION
            self.y -= (Bird.CLIMB_SPEED * frames_to_msec(delta_frames) * (1 - math.cos(frac_climb_done * math.pi)))
            self.msec_to_climb -= frames_to_msec(delta_frames)
        else:
            self.y += Bird.SINK_SPEED * frames_to_msec(delta_frames)

    @property
    def image(self):
    	"""Cap nhat hinh anh len xuong cua canh chim"""
        if pygame.time.get_ticks() % 500 >= 250:
            return self._img_wingup
        else:
            return self._img_wingdown
    

    @property
    def rect(self):
        """Tra ve vi tri toa do cua chim"""
        return Rect(self.x, self.y, Bird.WIDTH, Bird.HEIGHT)


    @property
    def mask(self):
    	"""Trang thai chim len hay xuong"""
    	if pygame.time.get_ticks() % 500 >= 250:
    		return self._mask_wingup
    	else:
    		return self._mask_wingdown






def load_anh():
	"""load anh"""
	def load_path_anh(img_file_name):
		file_name = os.path.join('.','images',img_file_name)
		img = pygame.image.load(file_name)

		img.convert()
		return img

	return {
		'background': load_path_anh('background.png'),
		'pipe-end': load_path_anh('pipe_end.png'),
		'pipe-body': load_path_anh('pipe_body.png'),
        'bird-wingup': load_path_anh('bird_wing_up.png'),
        'bird-wingdown': load_path_anh('bird_wing_down.png')
	}

def frames_to_msec(frame, fps=FPS):
	return 1000.0 * frame/fps

def msec_to_frames(miliseconds, fps=FPS):
	return fps*miliseconds / 1000.0




def  main():
	"""main flow of program"""

	pygame.init()
	display_surface = pygame.display.set_mode((WIN_WIDTH,WIN_HEIGHT))
	
	pygame.display.set_caption("Flappy Bird")
	
	clock = pygame.time.Clock()

	score_font = pygame.font.SysFont(None, 32, bold=True) #Dinh dang font

	images = load_images()
