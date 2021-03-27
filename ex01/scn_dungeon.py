# coding: utf-8
from pygame.locals import *
import pygame
import sys
import time
import threading

import scn_base
import srf_map
import srf_chr
import srf_fade_btl
import sts_move
import sts_cursor

SCREEN_X = 10
SCREEN_Y = 8

CELL_H = 64
CELL_W = 64

#-------------------------------------------------------------------------------
# プレイヤー表示（ブロック指定）
#-------------------------------------------------------------------------------
def put_player( screen, img, x, y ):

    pos_x = ( x * CELL_W ) - ( PLAYER_W/2 )
    pos_y = ( y * CELL_H ) - ( CELL_H/2 ) - ( PLAYER_H - CELL_H )
    screen.blit( img, ( pos_x, pos_y ))
    return

#-------------------------------------------------------------------------------
# シーンクラス
#-------------------------------------------------------------------------------
class SceneDungeon( scn_base.SceneBase ):

    #-------------------------------------------------------------------------------
    # メンバ（Private）
    #-------------------------------------------------------------------------------
    __pygame  = None
    __screen  = None
    __thread  = None
    __fade    = None
    __mv      = None
    __px      = None
    __py      = None
    __chara   = None
    __map     = None
    __cursor  = None
    __cnt     = None

    #-------------------------------------------------------------------------------
    # コンストラクタ
    #-------------------------------------------------------------------------------
    def __init__( self, pygame, screen ):

        self.__pygame = pygame
        self.__screen = screen
        self.scene  = scn_base.EnumScene.Dungeon

        # プレイヤー初期化
        self.__chara = srf_chr.SrfCharacter( self.__pygame, self.__screen, 20, CELL_W, CELL_H )
        self.__chara.add_pattern( "image/human_a.bmp" )
        self.__chara.add_pattern( "image/human_b.bmp" )

        # マップ初期化
        self.__map = srf_map.SrfMap( self.__pygame, self.__screen, "image/map.bmp", SCREEN_X, SCREEN_Y, CELL_H, CELL_W )

        find, self.__px, self.__py = self.__map.get_start_pos()
        if find == False:
            print("")
            print("【異常終了】マップにスタート地点が見つかりません")
            print("")
            return

        # 状態管理 - 移動量
        self.__mv = sts_move.StsMove()
        self.__mv.set_destination( 16 )
        self.__mv.set_block_size( CELL_H, CELL_W )

        # 状態管理 - カーソル
        self.__cursor = sts_cursor.StsCursor()

        # フェード効果
        self.__fade = srf_fade_btl.SrfFadeBattle( self.__pygame, self.__screen )

        return
    #-------------------------------------------------------------------------------
    # 周期処理開始
    #-------------------------------------------------------------------------------
    def begin( self ):

        self.scene  = scn_base.EnumScene.Dungeon
        self.changed = False
        self.__cnt = 0

        state = srf_fade_btl.EnumFadeStatus.WIPE_SPREAD
        self.__fade.begin( state )

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

        self.__fade.end()
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
            
            # プレイヤーアニメーション
            self.__chara.update( x )

            # フェード効果
            self.__fade.make_progress()

            state = srf_fade_btl.EnumFadeStatus.FILL_COMPLETELY
            if state == self.__fade.get_state():
                self.change( scn_base.EnumScene.Battle )

    #-------------------------------------------------------------------------------
    # 描画
    #-------------------------------------------------------------------------------
    def draw( self ):

        # 床と壁の表示
        self.__map.draw( self.__mv, self.__px, self.__py )

        # プレイヤーの表示
        self.__chara.draw( SCREEN_X / 2, SCREEN_Y / 2 )

        # フェード効果
        self.__fade.draw()

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
                elif event.key == K_RETURN:
                    state = srf_fade_btl.EnumFadeStatus.WIPE_SHRINK
                    self.__fade.begin( state )

            self.__cursor.add_event( event )
        return
