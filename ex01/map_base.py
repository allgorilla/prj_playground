# coding: utf-8
from pygame.locals import *
import pygame

import obj_party_player
import obj_party_follower
import obj_enemy_base
import obj_enemy_mummy
import obj_portal_base
import blk_base

#-------------------------------------------------------------------------------
# ブロックマップ
#-------------------------------------------------------------------------------
class MapBase:

    __pygame          = None
    __map_wh          = None
    __block_wh        = None

    __enemy_pos_list  = []
    __portal_pos_list = []
    obj_list          = []

    __img_map         = None
    __img_black       = None

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

        # 共通初期化処理
        self.init_common( filename, map_wh, block_wh )

        # オブジェクト初期化

        # エネミーのマップ配置

        # ポータルのマップ配置

        return

    #-------------------------------------------------------------------------------
    # コンストラクタの共通部分
    #-------------------------------------------------------------------------------
    def init_common( self, pygame, filename, map_wh, block_wh ):

        self.__map_wh   = map_wh
        self.__block_wh = block_wh

        self.__enemy_pos_list  = []
        self.__portal_pos_list = []
        self.obj_list          = []

        # マップ読み込み
        self.__img_map = pygame.image.load( filename )
        self.__img_black = pygame.image.load( "image/black_64.bmp" )

        for y in range( 0, self.__img_map.get_height() ):
            for x in range( 0, self.__img_map.get_width() ):

                pos = ( x, y )
                color = self.__img_map.get_at( pos )
                type = self.__get_blcock_type( color ).obj_type

                if type == "PORTAL":
                    self.__portal_pos_list.append( pos )
                elif type == "ENEMY":
                    self.__enemy_pos_list.append( pos )
                elif type == "NONE":
                    pass
                else:
                    pass
                    print( "未登録" )
        return

    #-------------------------------------------------------------------------------
    # ドットカラーを指定して、オブジェクトタイプを取得する
    #-------------------------------------------------------------------------------
    def __get_blcock_type( self, color ):

        for block in self.block_type_list:
            if block.color == color:
                return block

        return None

    #-------------------------------------------------------------------------------
    # 画像表示（ブロック指定）
    #-------------------------------------------------------------------------------
    def __put_block( self, screen, move, img, pos ):

        pos_x = ( self.__block_wh[ 0 ] * pos[ 0 ] ) - ( self.__block_wh[ 0 ] / 2 )
        pos_y = ( self.__block_wh[ 1 ] * pos[ 1 ] ) - ( self.__block_wh[ 1 ] / 2 )
        move_x, move_y = move.get_move_offset()
        screen.blit( img, ( pos_x + move_x, pos_y + move_y ) )

        return

    #-------------------------------------------------------------------------------
    # マップの更新
    #-------------------------------------------------------------------------------
    def update( self, cursor ):

        for object in self.obj_list:
            object.update_think( cursor, self, self.obj_list )
            object.update_animation()
            object.update_move( self )

        return

    #-------------------------------------------------------------------------------
    # マップの描画処理
    #-------------------------------------------------------------------------------
    def draw( self, screen ):

        player_object = self.__get_player_object()
        view_pos = player_object.loc_pos
        move     = player_object.move
        rect     = self.__img_map.get_rect()
        bx = int( self.__map_wh[ 0 ] / 2 ) # マップ→ウインドウの表示範囲の補正値(X方向)
        by = int( self.__map_wh[ 1 ] / 2 ) # マップ→ウインドウの表示範囲の補正値(Y方向)
        sx = bx                      # マップの表示範囲の開始ブロック(X方向)
        sy = by                      # マップの表示範囲の開始ブロック(Y方向)
        ex = bx + 1                  # マップの表示範囲の終端ブロック(X方向)
        ey = by + 1                  # マップの表示範囲の終端ブロック(Y方向)

        dir = move.get_direction()
        if dir[ 0 ] == 1:
            sx += 1
        elif dir[ 0 ] == -1:
            ex += 1

        if dir[ 1 ] == 1:
            sy += 1
        elif dir[ 1 ] == -1:
            ey += 1

        for oy in range( -sy, ey ):
            for ox in range( -sx, ex ):

                mx = ox + view_pos[ 0 ] # マップから読みだす対象のX座標
                my = oy + view_pos[ 1 ] # マップから読みだす対象のY座標

                img = self.__img_black
                if mx >= rect.left and mx < rect.right:
                    if my >= rect.top and my < rect.bottom:
                        color = self.__img_map.get_at(( mx, my ))
                        img = self.__get_blcock_type( color ).image
                self.__put_block( screen, move, img, ( ox + bx, oy + by ))
        return

    #-------------------------------------------------------------------------------
    # マップの描画処理
    #-------------------------------------------------------------------------------
    def blit( self, screen ):

        # オブジェクトアニメーション
        for object in self.obj_list:
            object.set_blit_pos( screen )

        # 全オブジェクトの優先度リストを作成
        pri_list = []
        i = 0;
        for object in self.obj_list:
            # Y座標は大きいほど優先
            y = object.blit_pos[ 1 ]
            x = len( self.obj_list ) - i
            i += 1
            pri_list.append( y * 1000 + x )

        # 優先度リストから表示順リストを作成
        seq_list = []
        while len( seq_list ) != len( pri_list ):
            # 優先度リストから値の小さい順にindexを保存する
            y_min = min( pri_list )
            index = pri_list.index( y_min )
            seq_list.append( index )
            pri_list[ index ] = 0xFFFFFFFF

        # 表示順リストに従ってオブジェクトを描画
        for index in seq_list:
            self.obj_list[ index ].draw( screen )

        return

    #-------------------------------------------------------------------------------
    # マップイメージの範囲チェック
    #-------------------------------------------------------------------------------
    def __is_out_of_map( self, pos ):

        ( x, y ) = pos
        rect = self.__img_map.get_rect()
        if rect.top <= x and x < rect.bottom:
            if rect.left <= y and y < rect.right:
                return False

        return True

    #-------------------------------------------------------------------------------
    # ブロックの侵入可否チェック
    #-------------------------------------------------------------------------------
    def can_walk( self, pos ):

        # マップイメージの範囲外に出る場合侵入不可
        if True == self.__is_out_of_map( pos ):
            return False

        color = self.__img_map.get_at( pos )
        if self.__get_blcock_type( color ).can_walk:
            return True

        return False
    #-------------------------------------------------------------------------------
    # 敵の座標を１つ取得
    #-------------------------------------------------------------------------------
    def get_enemy_pos( self ):

        if 0 == len( self.__enemy_pos_list ):
            print( "★エラー：エネミーリストが空っぽです" )
            return ( -1, -1 )
        else:
            return self.__enemy_pos_list.pop( 0 )

    #-------------------------------------------------------------------------------
    # ポータルの座標を１つ取得
    #-------------------------------------------------------------------------------
    def get_portal_pos( self ):

        if 0 == len( self.__portal_pos_list ):
            print( "★エラー：ポータルリストが空っぽです" )
            return ( -1, -1 )
        else:
            return self.__portal_pos_list.pop( 0 )

    #-------------------------------------------------------------------------------
    # プレイヤーの開始座標を取得
    #-------------------------------------------------------------------------------
    def set_start_pos( self, num ):

        object_cnt = 0
        portal_cnt = 0
        player_object = self.__get_player_object()
        for object in self.obj_list:
            if object.type == "PORTAL":
                if portal_cnt == num:
                    player_object.loc_pos = self.obj_list[ object_cnt ].loc_pos
                portal_cnt += 1
            object_cnt += 1

        return

    #-------------------------------------------------------------------------------
    # プレイヤーの開始座標を取得
    #-------------------------------------------------------------------------------
    def get_start_pos( self ):
        return self.__portal_pos_list[ 0 ]

    #-------------------------------------------------------------------------------
    # ブロックタイプを追加する
    #-------------------------------------------------------------------------------
    def add_block_type( self, pygame, color, obj_type, can_walk, file ):

        type = self.__get_blcock_type( color )
        if type == None:
            block = blk_base.BlockBase( pygame, color, obj_type, can_walk, file )
            self.block_type_list.append( block )

        return

    #-------------------------------------------------------------------------------
    # 味方オブジェクトを追加するメソッド
    #-------------------------------------------------------------------------------
    def add_party_object( self, pygame, file, block_wh, acnt, tcnt ):

        player_object = self.__get_player_object()
        if 0 == len( self.obj_list ):
            pos = self.get_start_pos()
            object = obj_party_player.ObjectPartyPlayer( pygame, pos, block_wh, acnt, tcnt )
        elif 0 < len( self.obj_list ) and len( self.obj_list ) < 4:
            pos = player_object.loc_pos
            object = obj_party_follower.ObjectPartyFollower( pygame, pos, block_wh, acnt, tcnt )

        object.add_pattern( pygame, file + "_a.png" )
        object.add_pattern( pygame, file + "_b.png" )
        self.obj_list.append( object )

    #-------------------------------------------------------------------------------
    # 敵オブジェクトを追加するメソッド
    #-------------------------------------------------------------------------------
    def add_enemy_object( self, pygame, file, block_wh, acnt, tcnt ):

        pos = self.get_enemy_pos()
        object = obj_enemy_base.ObjectEnemyBase( pygame, pos, block_wh, acnt, tcnt )

        object.add_pattern( pygame, file + "_a.png" )
        object.add_pattern( pygame, file + "_b.png" )
        self.obj_list.append( object )

    #-------------------------------------------------------------------------------
    # 敵を追加するサブルーチン
    #-------------------------------------------------------------------------------
    def add_portal_object( self, pygame, file, block_wh, map, num ):

        pos = self.get_portal_pos()
        object = obj_portal_base.ObjectPortalBase( pygame, pos, block_wh, map, num )
        object.add_pattern( pygame, file + ".png" )
        self.obj_list.append( object )

    #-------------------------------------------------------------------------------
    # プレイヤーの座標をオブジェクトを取得する
    #-------------------------------------------------------------------------------
    def __get_player_object( self ):

        for object in self.obj_list:
            if object.type == "PLAYER":
                return object

    #-------------------------------------------------------------------------------
    # 仲間の座標をリセットする
    #-------------------------------------------------------------------------------
    def reset_follower_pos( self ):

        player_object = self.__get_player_object()
        for object in self.obj_list:
            if object.type == "FOLLOWER":
                object.loc_pos = player_object.loc_pos

        return