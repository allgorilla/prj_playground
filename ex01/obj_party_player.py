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
    def update_input( self, cursor, map, move, view ):

        # 移動オフセットの進捗更新
        x, y = cursor.get_direction()

        if move.get_direction() != ( 0, 0 ):
            move.make_progress()

        else:
            # ブロックの侵入可否チェック
            if True == map.can_walk( self.pos[ 0 ] + x, self.pos[ 1 ] + y ):
                self.pos = ( self.pos[ 0 ] + x, self.pos[ 1 ] + y )
                view = self.pos
                move.set_direction( x, y )

        # 左右反転
        if self.dir_x == -1  and x == 1:
            self.dir_x = x
        elif self.dir_x == 1 and x == -1:
            self.dir_x = x

        return view

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
