# coding: utf-8
from pygame.locals import *
import pygame
import sys
import time
import threading

import blockmap
import movemgr
import keyevt

SCREEN_X = 10
SCREEN_Y = 8

CELL_H = 64
CELL_W = 64
PLAYER_H = 80
PLAYER_W = 80

g_img_human = None

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
class SceneDungeon:

    #-------------------------------------------------------------------------------
    # メンバ（Private）
    #-------------------------------------------------------------------------------
    __pygame = None
    __scr    = None
    __mv     = None
    __px     = None
    __py     = None
    __map     = None
    __key    = None
    __thread = None

    #-------------------------------------------------------------------------------
    # コンストラクタ
    #-------------------------------------------------------------------------------
    def __init__( self, pygame, screen ):
        global g_img_human

        self.__pygame = pygame
        self.__scr    = screen

        # プレイヤー読み込み
        g_img_human = self.__pygame.image.load("human_80.bmp").convert()
        colorkey = g_img_human.get_at((0,0))
        g_img_human.set_colorkey(colorkey, RLEACCEL)

        # マップ初期化
        self.__map = blockmap.BlockMap( self.__pygame, self.__scr, "map.bmp", SCREEN_X, SCREEN_Y, CELL_H, CELL_W )

        find, self.__px, self.__py = self.__map.get_start_pos()

        if find == False:
            print("")
            print("【異常終了】マップにスタート地点が見つかりません")
            print("")
            return

        self.__mv = movemgr.MoveMgr()
        self.__mv.set_destination( 12 )
        self.__mv.set_block_size( CELL_H, CELL_W )

        self.__key = keyevt.KeyEvent()

        return
    #-------------------------------------------------------------------------------
    # 周期処理開始
    #-------------------------------------------------------------------------------
    def start( self ):

        if None != self.__thread:
            return False

        else:
            self.__thread = threading.Thread( target = self.__update )
            self.__thread.start()
            return True

    #-------------------------------------------------------------------------------
    # 終了処理
    #-------------------------------------------------------------------------------
    def __finalize( self ):

        self.__thread = None
        self.__pygame.quit() 
        sys.exit()

    #-------------------------------------------------------------------------------
    # 周期更新
    #-------------------------------------------------------------------------------
    def __update( self ):

        while None != self.__thread:
            self.__pygame.time.wait( 16 )

            # 移動オフセットの進捗更新
            if self.__mv.get_direction() != ( 0, 0 ):
                self.__mv.make_progress()

            else:
                x, y = self.__key.get_direction()

                # ブロックの侵入可否チェック
                if True == self.__map.can_walk( self.__px + x, self.__py + y ):
                    self.__px += x 
                    self.__py += y
                    self.__mv.set_direction( x, y )

    #-------------------------------------------------------------------------------
    # 描画
    #-------------------------------------------------------------------------------
    def draw( self ):
        global g_img_human

        # 画面を塗りつぶす
        self.__scr.fill(( 0, 0, 255 ))

        # 床と壁の表示
        self.__map.draw( self.__mv, self.__px, self.__py )

        #プレイヤーの表示
        put_player( self.__scr, g_img_human, SCREEN_X / 2, SCREEN_Y / 2 )

        # 描画処理を実行
        self.__pygame.display.update()

        return

    #-------------------------------------------------------------------------------
    # キー入力
    #-------------------------------------------------------------------------------
    def input( self ):

        # システムとの同期
        self.__pygame.event.pump()

        for event in self.__pygame.event.get():

            # 終了イベント
            if event.type == QUIT:
                self.__finalize()

            # キ－入力イベント
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.__finalize()

            self.__key.add_event( event )

        return
