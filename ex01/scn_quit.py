# coding: utf-8
from pygame.locals import *
import pygame
import sys
import time
import threading

import scn_base

#-------------------------------------------------------------------------------
# シーンクラス
#-------------------------------------------------------------------------------
class SceneQuit( scn_base.SceneBase ):

    #-------------------------------------------------------------------------------
    # メンバ（Private）
    #-------------------------------------------------------------------------------
    __pygame  = None
    __screen  = None
    __image   = None

    #-------------------------------------------------------------------------------
    # コンストラクタ
    #-------------------------------------------------------------------------------
    def __init__( self, pygame, screen ):

        self.__pygame = pygame
        self.__screen = screen
        self.scene  = scn_base.EnumScene.Quit

        return
    #-------------------------------------------------------------------------------
    # シーン開始
    #-------------------------------------------------------------------------------
    def begin( self ):
        # アプリケーション終了
        self.__pygame.quit() 
        sys.exit()
        return

    #-------------------------------------------------------------------------------
    # シーン終了
    #-------------------------------------------------------------------------------
    def end( self ):
        return

    #-------------------------------------------------------------------------------
    # 周期更新
    #-------------------------------------------------------------------------------
    def __update( self ):
        return

    #-------------------------------------------------------------------------------
    # 描画
    #-------------------------------------------------------------------------------
    def draw( self ):
        return

    #-------------------------------------------------------------------------------
    # キー入力
    #-------------------------------------------------------------------------------
    def input( self ):
        return