# coding: utf-8
from pygame.locals import *
import pygame

import obj_party_player
import obj_party_follower
import obj_enemy_base
import obj_enemy_mummy
import obj_portal_base
import blk_base
import map_base


#-------------------------------------------------------------------------------
# ブロックマップ
#-------------------------------------------------------------------------------
class MapDungeon2( map_base.MapBase ):

    #-------------------------------------------------------------------------------
    # コンストラクタ
    # param(in) pygameオブジェクト
    # param(in) screenオブジェクト
    # param(in) マップのサイズ(X方向ブロック数)
    # param(in) マップのサイズ(Y方向ブロック数)
    # param(in) ブロックのサイズ(X方向ドット数)
    # param(in) ブロックのサイズ(Y方向ドット数)
    #-------------------------------------------------------------------------------
    def __init__( self, pygame, filename, map_wh, block_wh ):

        self.__pygame   = pygame
        self.block_type_list = []

        # イメージの読み込み
        self.add_block_type( pygame, (   0,   0, 255, 255 ), "PORTAL", True,  "image/floor.bmp" )
        self.add_block_type( pygame, ( 255,   0,   0, 255 ), "ENEMY",  True,  "image/floor.bmp" )
        self.add_block_type( pygame, ( 255, 255, 255, 255 ), "NONE",   True,  "image/floor.bmp" )
        self.add_block_type( pygame, (   0,   0,   0, 255 ), "NONE",   False, "image/wall.bmp"  )

        # 共通初期化処理
        self.init_common( pygame, filename, map_wh, block_wh )

        # オブジェクト初期化
        self.add_party_object( pygame, "image/human",   block_wh, 20, 100 )
        self.add_party_object( pygame, "image/warrior", block_wh, 20, 100 )
        self.add_party_object( pygame, "image/thief",   block_wh, 20, 100 )
        self.add_party_object( pygame, "image/mage",    block_wh, 20, 100 )

        # エネミーのマップ配置
        for i in range( 18 ):
            self.add_enemy_object( pygame, "image/enemy_mummy", block_wh, 10, 20 )

        # ポータルのマップ配置
        self.add_portal_object( pygame, "image/stairs_d", block_wh, 2, 0 )
        self.add_portal_object( pygame, "image/circle",   block_wh, 1, 0 )

        return