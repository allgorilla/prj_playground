# coding: utf-8
from pygame.locals import *
import pygame
import sys
import time
import threading

import scn_base
import srf_map
import obj_party_player
import obj_enemy_mino
import obj_enemy_mummy
import srf_wipe_btl
import sts_move
import sts_cursor

SCREEN_X = 10
SCREEN_Y = 8

CELL_H = 64
CELL_W = 64

#-------------------------------------------------------------------------------
# シーンクラス
#-------------------------------------------------------------------------------
class SceneDungeon( scn_base.SceneBase ):

    #-------------------------------------------------------------------------------
    # メンバ（Private）
    #-------------------------------------------------------------------------------
    __pygame   = None
    __screen   = None
    __thread   = None
    __wipe     = None
    __mv       = None
    __px       = None
    __py       = None
    __map      = None
    __cursor   = None
    __cnt      = None
    __obj_list = []

    #-------------------------------------------------------------------------------
    # コンストラクタ
    #-------------------------------------------------------------------------------
    def __init__( self, pygame, screen ):

        self.__pygame = pygame
        self.__screen = screen
        self.scene  = scn_base.EnumScene.Dungeon

        # マップ初期化
        self.__map = srf_map.SrfMap( self.__pygame, "image/map.bmp", SCREEN_X, SCREEN_Y, CELL_H, CELL_W )

        # オブジェクト初期化：敵ミノタウロス
        pos = self.__map.get_enemy_pos()
        object = obj_enemy_mino.ObjectEnemyMino( self.__pygame, pos, ( CELL_W, CELL_H ), 20 )
        object.add_pattern( "image/enemy_mino_a.png" )
        object.add_pattern( "image/enemy_mino_b.png" )
        self.__obj_list.append( object )

        # オブジェクト初期化：敵マミー
        pos = self.__map.get_enemy_pos()
        object = obj_enemy_mummy.ObjectEnemyMummy( self.__pygame, pos, ( CELL_W, CELL_H ), 20 )
        object.add_pattern( "image/enemy_mummy_a.png" )
        object.add_pattern( "image/enemy_mummy_b.png" )
        self.__obj_list.append( object )

        # オブジェクト初期化：ドラゴン
        pos = self.__map.get_enemy_pos()
        object = obj_enemy_mummy.ObjectEnemyMummy( self.__pygame, pos, ( CELL_W, CELL_H ), 20 )
        object.add_pattern( "image/enemy_dragon_a.png" )
        object.add_pattern( "image/enemy_dragon_b.png" )
        self.__obj_list.append( object )

        # オブジェクト初期化：プレイヤー
        pos = self.__map.get_player_pos()
        ( self.__px, self.__py ) = pos
        object = obj_party_player.ObjectPartyPlayer( self.__pygame, pos, ( CELL_W, CELL_H ), 20 )
        object.add_pattern( "image/human_a.png" )
        object.add_pattern( "image/human_b.png" )
        self.__obj_list.append( object )

        # 状態管理 - 移動量
        self.__mv = sts_move.StsMove()
        self.__mv.set_destination( 16 )
        self.__mv.set_block_size( CELL_H, CELL_W )

        # 状態管理 - カーソル
        self.__cursor = sts_cursor.StsCursor()

        # ワイプエフェクト
        self.__wipe = srf_wipe_btl.SrfWipeBattle( self.__pygame, 8 )

        return
    #-------------------------------------------------------------------------------
    # 周期処理開始
    #-------------------------------------------------------------------------------
    def begin( self ):

        self.scene  = scn_base.EnumScene.Dungeon
        self.changed = False
        self.__cnt = 0

        state = srf_wipe_btl.EnumWipeStatus.WIPE_SPREAD
        self.__wipe.begin( state )

        if None != self.__thread:
            return False

        else:
            self.__thread = threading.Thread( target = self.__update )
            self.__thread.start()
            return True

    #-------------------------------------------------------------------------------
    # シーン終了
    #-------------------------------------------------------------------------------
    def end( self ):
        self.__thread = None
        self.__cursor.clear_event()

        self.__wipe.end()
        return

    #-------------------------------------------------------------------------------
    # 周期更新
    #-------------------------------------------------------------------------------
    def __update( self ):

        while None != self.__thread:
            # システムとの同期
            self.__pygame.event.pump()
            self.__pygame.time.wait( 16 )

            # 移動オフセットの進捗更新
            x, y = self.__cursor.get_direction()
            if self.__mv.get_direction() != ( 0, 0 ):
                self.__mv.make_progress()

            else:
                # ブロックの侵入可否チェック
                if True == self.__map.can_walk( self.__px + x, self.__py + y ):
                    self.__px += x 
                    self.__py += y
                    self.__mv.set_direction( x, y )
            
            # オブジェクトアニメーション
            for object in self.__obj_list:
                object.update( x )

            # ワイプエフェクト
            self.__wipe.make_progress()

            state = srf_wipe_btl.EnumWipeStatus.FILL_COMPLETELY
            if state == self.__wipe.get_state():
                self.change( scn_base.EnumScene.Battle )

    #-------------------------------------------------------------------------------
    # 描画
    #-------------------------------------------------------------------------------
    def draw( self ):

        # 床と壁の表示
        self.__map.draw( self.__screen, ( self.__px, self.__py ), self.__mv )

        # オブジェクトアニメーション
        for object in self.__obj_list:
            object.draw( self.__screen, ( self.__px, self.__py ), self.__mv )

        # ワイプエフェクト
        self.__wipe.draw( self.__screen )

        return

    #-------------------------------------------------------------------------------
    # キー入力
    #-------------------------------------------------------------------------------
    def input( self ):

        for event in self.__pygame.event.get():

            # 終了イベント
            if event.type == QUIT:
                self.change( scn_base.EnumScene.Quit )

            # キ－入力イベント
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.change( scn_base.EnumScene.Quit )

            # 以降のキー入力はワイプ中には受け付けない
            state = srf_wipe_btl.EnumWipeStatus.WIPE_COMPLETELY
            if state != self.__wipe.get_state():
                return

            # 方向キー、決定キーの入力
            if event.type == KEYDOWN:
                if event.key == K_RETURN:
                    state = srf_wipe_btl.EnumWipeStatus.WIPE_SHRINK
                    self.__wipe.begin( state )
            self.__cursor.add_event( event )

        return
