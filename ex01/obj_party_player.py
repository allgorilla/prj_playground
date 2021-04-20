# coding: utf-8
from pygame.locals import *
import pygame

import obj_base

#-------------------------------------------------------------------------------
# 移動マネージャークラス
#-------------------------------------------------------------------------------
class ObjectPartyPlayer( obj_base.ObjectBase ):

    #-------------------------------------------------------------------------------
    # 状態を更新
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

    #-------------------------------------------------------------------------------
    # プレイヤーを描画
    #-------------------------------------------------------------------------------
    def draw( self, screen, view_pos, move ):

        if self.dir_x == -1:
            # 左向き画像
            image = self.img_lr[ 0 ]
        elif self.dir_x == 1:
            # 右向き画像
            image = self.img_lr[ 1 ]

        x = ( screen.get_width() / self.block[ 0 ] ) / 2
        y = ( screen.get_height() / self.block[ 1 ] ) / 2
        pos_x = ( x * self.block[ 0 ] ) - ( image.get_width() / 2 )
        pos_y = ( y * self.block[ 1 ] ) - ( self.block[ 0 ] / 2 ) - ( image.get_height() - self.block[ 0 ] )
        screen.blit( image, ( pos_x, pos_y ))

        return
