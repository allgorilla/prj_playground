# coding: utf-8
from pygame.locals import *
import pygame

import obj_base

#-------------------------------------------------------------------------------
# 移動マネージャークラス
#-------------------------------------------------------------------------------
class ObjectEnemyMino( obj_base.ObjectBase ):

    #-------------------------------------------------------------------------------
    # プレイヤーを描画
    #-------------------------------------------------------------------------------
    def test( self, x ):

        # 左右反転
        if self.dir_x == -1  and x == 1:
            self.dir_x = x
        elif self.dir_x == 1 and x == -1:
            self.dir_x = x

        self.fcur += 1
        if  self.fmax <= self.fcur:
            self.img_list.append( self.img_lr )
            self.img_lr = self.img_list.pop( 0 )
            self.fcur = 0

