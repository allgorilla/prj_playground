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
class MapTown0( map_base.MapBase ):

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
        self.add_block_type( pygame, (   0,   0,   0, 255 ), "NONE",   False, "image/black_64.bmp"  )
        self.add_block_type( pygame, (  64,  64,  64, 255 ), "NONE",   False, "image/t_wall.bmp" )
        self.add_block_type( pygame, (   0, 127,   0, 255 ), "NONE",   False, "image/t_tree.bmp" )
        self.add_block_type( pygame, ( 191, 191, 191, 255 ), "NONE",   True,  "image/t_road.bmp" )
        self.add_block_type( pygame, ( 255, 255, 255, 255 ), "NONE",   True,  "image/t_grass.bmp" )
        self.add_block_type( pygame, (   0,   0, 255, 255 ), "PORTAL", True,  "image/t_portal.bmp" )

        # 共通初期化処理
        self.init_common( pygame, filename, map_wh, block_wh )

        # オブジェクト初期化
        self.add_party_object( pygame, "image/human",   block_wh, 20, 100 )
        self.add_party_object( pygame, "image/warrior", block_wh, 20, 100 )
        self.add_party_object( pygame, "image/thief",   block_wh, 20, 100 )
        self.add_party_object( pygame, "image/mage",    block_wh, 20, 100 )

        # エネミーのマップ配置

        # ポータルのマップ配置
        self.add_portal_object( pygame, "image/t_portal", block_wh, 1, 3 )
        self.add_portal_object( pygame, "image/t_portal", block_wh, 1, 4 )
        self.add_portal_object( pygame, "image/t_portal", block_wh, 0, 2 )
        self.add_portal_object( pygame, "image/t_portal", block_wh, 0, 3 )
        self.add_portal_object( pygame, "image/t_portal", block_wh, 0, 4 )
        self.add_portal_object( pygame, "image/t_portal", block_wh, 0, 5 )
        self.add_portal_object( pygame, "image/t_portal", block_wh, 0, 6 )
        self.add_portal_object( pygame, "image/t_portal", block_wh, 0, 7 )
        self.add_portal_object( pygame, "image/t_portal", block_wh, 0, 8 )
        self.add_portal_object( pygame, "image/t_portal", block_wh, 0, 9 )
        self.add_portal_object( pygame, "image/t_portal", block_wh, 0, 10 )
        self.add_portal_object( pygame, "image/t_portal", block_wh, 0, 11 )
        self.add_portal_object( pygame, "image/t_portal", block_wh, 0, 12 )
        self.add_portal_object( pygame, "image/t_portal", block_wh, 0, 13 )
        self.add_portal_object( pygame, "image/t_portal", block_wh, 0, 14 )
        self.add_portal_object( pygame, "image/t_portal", block_wh, 0, 15 )
        self.add_portal_object( pygame, "image/t_portal", block_wh, 0, 16 )
        self.add_portal_object( pygame, "image/t_portal", block_wh, 0, 17 )
        self.add_portal_object( pygame, "image/t_portal", block_wh, 0, 18 )
        self.add_portal_object( pygame, "image/t_portal", block_wh, 0, 19 )
        self.add_portal_object( pygame, "image/t_portal", block_wh, 0, 20 )
        self.add_portal_object( pygame, "image/t_portal", block_wh, 0, 21 )
        self.add_portal_object( pygame, "image/t_portal", block_wh, 0, 22 )
        self.add_portal_object( pygame, "image/t_portal", block_wh, 0, 23 )
        self.add_portal_object( pygame, "image/t_portal", block_wh, 0, 24 )
        self.add_portal_object( pygame, "image/t_portal", block_wh, 0, 25 )

        return
