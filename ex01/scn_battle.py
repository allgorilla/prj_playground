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
class SceneBattle( scn_base.SceneBase ):

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
        self.scene  = scn_base.EnumScene.Battle

        # 画像ファイルを読み込み
        self.__image = self.__pygame.image.load( "image/battle.png" ).convert()

        return
    #-------------------------------------------------------------------------------
    # シーン開始
    #-------------------------------------------------------------------------------
    def begin( self ):
        self.scene  = scn_base.EnumScene.Battle
        self.changed = False

        return

    #-------------------------------------------------------------------------------
    # シーン終了
    #-------------------------------------------------------------------------------
    def end( self ):
        pass
        return

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

        # 画像を描画
        self.__screen.blit( self.__image, ( 0, 0 ))

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
                    self.change( scn_base.EnumScene.Dungeon )

        return
