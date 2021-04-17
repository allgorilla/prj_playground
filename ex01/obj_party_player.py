# coding: utf-8
from pygame.locals import *
import pygame

import obj_base

#-------------------------------------------------------------------------------
# 移動マネージャークラス
#-------------------------------------------------------------------------------
class ObjectPartyPlayer( obj_base.ObjectBase ):

    #-------------------------------------------------------------------------------
    # コンストラクタ
    #-------------------------------------------------------------------------------
    def __init__( self, pygame, fcnt_max, block_w, block_h ):

        self.pygame   = pygame
        self.fcnt     = 0
        self.fcnt_max = fcnt_max
        self.block_w  = block_w
        self.block_h  = block_h
        self.dir_x    = -1

        return
