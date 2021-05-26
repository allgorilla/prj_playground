# coding: utf-8
from pygame.locals import *
import pygame

import obj_base

#-------------------------------------------------------------------------------
# マップ上のオブジェクトのベースクラス
#-------------------------------------------------------------------------------
class ObjectPortalBase( obj_base.ObjectBase ):

    #-------------------------------------------------------------------------------
    # Public
    #-------------------------------------------------------------------------------
    

    #-------------------------------------------------------------------------------
    # Private
    #-------------------------------------------------------------------------------

    #-------------------------------------------------------------------------------
    # コンストラクタ
    #-------------------------------------------------------------------------------
    def __init__( self, pygame, pos, grid_wh, link_map, potal_num ):

        self.type       = "PORTAL"
        self.link_map   = link_map
        self.portal_num = potal_num
        self.init_common( pygame, pos, grid_wh, 1000, 1000 )

        return

    #-------------------------------------------------------------------------------
    # 状態を更新
    #-------------------------------------------------------------------------------
    def update_think( self, cursor, map, obj_list ):
        self.update_common(( 0, 0 ), map, obj_list )
        return

    #-------------------------------------------------------------------------------
    # 接触を検知する
    #-------------------------------------------------------------------------------
    def find_contact_trigger( self, objerct_list ):

        player = objerct_list[ 0 ]
        if self.loc_pos == player.loc_pos:
            if player.move.is_stop():
                if self.contact_triger == False:
                    self.contact_triger = True
                    print( "ポータルに接触しました", self.loc_pos )
                    return True
                else:
                    return False
        self.contact_triger = False
        return False
