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
    def update_think( self, cursor, map, obj_list ):

        # 移動オフセットの進捗更新
        dir = cursor.get_direction()

        if self.move.get_direction() != ( 0, 0 ):
            self.move.make_progress()

        else:
            # ブロックの侵入可否チェック
            pos = ( self.loc_pos[ 0 ] + dir[ 0 ], self.loc_pos[ 1 ] + dir[ 1 ] )
            if True == map.can_walk( pos ):
                self.loc_pos = pos
                self.move.set_direction( dir )

        self.view_pos = self.loc_pos
        self.view_ofs = self.move.get_move_offset()
        self.loc_ofs  = self.move.get_move_offset()

        # 左右反転
        if self.dir == ( -1, 0 )  and dir == ( 1, 0 ):
            self.dir = dir
        elif self.dir == ( 1, 0 ) and dir == ( -1, 0 ):
            self.dir = dir

        return

