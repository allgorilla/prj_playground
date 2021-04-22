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
        dir = cursor.get_direction()

        if move.get_direction() != ( 0, 0 ):
            move.make_progress()

        else:
            # ブロックの侵入可否チェック
            pos = ( self.pos[ 0 ] + dir[ 0 ], self.pos[ 1 ] + dir[ 1 ] )
            if True == map.can_walk( pos ):
                self.pos = pos
                move.set_direction( dir )

        # 左右反転
        if self.dir == ( -1, 0 )  and dir == ( 1, 0 ):
            self.dir = dir
        elif self.dir == ( 1, 0 ) and dir == ( -1, 0 ):
            self.dir = dir

        return self.pos

    #-------------------------------------------------------------------------------
    # プレイヤーを描画
    #-------------------------------------------------------------------------------
    def draw( self, screen, view_pos, move ):

        if self.dir == ( -1, 0 ):
            # 左向き画像
            image = self.img_lr[ 0 ]
        elif self.dir == ( 1, 0 ):
            # 右向き画像
            image = self.img_lr[ 1 ]

        x = ( screen.get_width() / self.block[ 0 ] ) / 2
        y = ( screen.get_height() / self.block[ 1 ] ) / 2
        x = self.pos[ 0 ] - view_pos[ 0 ] + x
        y = self.pos[ 1 ] - view_pos[ 1 ] + y
        pos_x = ( x * self.block[ 0 ] ) - ( image.get_width() / 2 )
        pos_y = ( y * self.block[ 1 ] ) - ( image.get_height() - self.block[ 1 ] ) - ( self.block[ 1 ] / 2 ) 
        screen.blit( image, ( pos_x, pos_y ))

        return
