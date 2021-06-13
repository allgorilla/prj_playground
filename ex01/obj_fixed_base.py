# coding: utf-8
from pygame.locals import *
import pygame

import obj_base

#-------------------------------------------------------------------------------
# 移動マネージャークラス
#-------------------------------------------------------------------------------
class ObjectFixedBase( obj_base.ObjectBase ):

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

    #-------------------------------------------------------------------------------
    # 状態を更新
    #-------------------------------------------------------------------------------
    def update_think( self, cursor, map, obj_list ):
        self.update_common(( 0,0 ), map, obj_list )
        return
