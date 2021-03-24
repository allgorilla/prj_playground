# coding: utf-8
from pygame.locals import *
import pygame
import sys
import time
import threading
from enum import IntEnum

#-------------------------------------------------------------------------------
# シーン列挙型
#-------------------------------------------------------------------------------
class EnumScene( IntEnum ):
    Dungeon = 0
    Battle  = 1

#-------------------------------------------------------------------------------
# シーンクラス
#-------------------------------------------------------------------------------
class SceneBase:

    #-------------------------------------------------------------------------------
    # メンバ（Private）
    #-------------------------------------------------------------------------------
    __pygame = None
    __screen = None

    #-------------------------------------------------------------------------------
    # コンストラクタ
    #-------------------------------------------------------------------------------
    def __init__( self, pygame, screen ):

        self.__pygame = pygame
        self.__screen = screen

        return
    #-------------------------------------------------------------------------------
    # 周期処理開始
    #-------------------------------------------------------------------------------
    def start( self ):
        pass
        return

    #-------------------------------------------------------------------------------
    # 終了処理
    #-------------------------------------------------------------------------------
    def __finalize( self ):
        self.__pygame.quit() 
        sys.exit()

    #-------------------------------------------------------------------------------
    # 周期更新
    #-------------------------------------------------------------------------------
    def __update( self ):
        pass
        return

    #-------------------------------------------------------------------------------
    # 描画
    #-------------------------------------------------------------------------------
    def draw( self ):

        # 画面を塗りつぶす
        self.__screen.fill(( 0, 0, 255 ))

        # 描画処理を実行
        self.__pygame.display.update()

        return

    #-------------------------------------------------------------------------------
    # キー入力
    #-------------------------------------------------------------------------------
    def input( self ):

        for event in self.__pygame.event.get():

            # 終了イベント
            if event.type == QUIT:
                self.__finalize()

            # キ－入力イベント
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.__finalize()

