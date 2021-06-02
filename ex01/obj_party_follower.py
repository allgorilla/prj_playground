# coding: utf-8
from pygame.locals import *
import pygame

import obj_base

#-------------------------------------------------------------------------------
# 移動マネージャークラス
#-------------------------------------------------------------------------------
class ObjectPartyFollower( obj_base.ObjectBase ):

    #-------------------------------------------------------------------------------
    # コンストラクタ
    #-------------------------------------------------------------------------------
    def __init__( self, pygame, pos, grid_wh, acnt, tcnt ):

        self.type       = "FOLLOWER"
        self.init_common( pygame, pos, grid_wh, acnt, tcnt )

        return
    #-------------------------------------------------------------------------------
    # 状態を更新
    #-------------------------------------------------------------------------------
    def update_think( self, cursor, map, obj_list ):

        # ターゲットのオブジェクトを取得
        i = 0
        for obj in obj_list:
            if obj == self:
               target = obj_list[ i - 1 ]
               break
            i += 1

        # ターゲットとの距離が2以上で移動する
        t = target.loc_pos
        s = self.loc_pos
        if target.move.is_stop():
            dir = ( 0, 0 )
        else:
            dir = target.move.get_direction()
            dir = ( t[ 0 ] - s[ 0 ] - dir[ 0 ], t[ 1 ] - s[ 1 ] - dir[ 1 ] )
        self.update_common( dir, map, obj_list )
        return
