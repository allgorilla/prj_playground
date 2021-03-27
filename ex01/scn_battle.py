# coding: utf-8
from pygame.locals import *
import pygame
import sys
import time
import threading

import scn_base
import srf_fade_btl

#-------------------------------------------------------------------------------
# シーンクラス
#-------------------------------------------------------------------------------
class SceneBattle( scn_base.SceneBase ):

    #-------------------------------------------------------------------------------
    # メンバ（Private）
    #-------------------------------------------------------------------------------
    __pygame  = None
    __screen  = None
    __thread  = None
    __fade    = None
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

        # フェード効果
        self.__fade = srf_fade_btl.SrfFadeBattle( self.__pygame, self.__screen )

        return

    #-------------------------------------------------------------------------------
    # シーン開始
    #-------------------------------------------------------------------------------
    def begin( self ):

        self.scene  = scn_base.EnumScene.Battle
        self.changed = False

        # フェード効果
        state = srf_fade_btl.EnumFadeStatus.FILL_SHRINK
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

            # フェード効果
            self.__fade.make_progress()

            state = srf_fade_btl.EnumFadeStatus.FILL_COMPLETELY
            if state == self.__fade.get_state():
                self.change( scn_base.EnumScene.Dungeon )

    #-------------------------------------------------------------------------------
    # 描画
    #-------------------------------------------------------------------------------
    def draw( self ):

        # 画像を描画
        self.__screen.blit( self.__image, ( 0, 0 ))

        # フェード効果
        self.__fade.draw()

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
                    state = srf_fade_btl.EnumFadeStatus.FILL_SPREAD
                    self.__fade.begin( state )

        return
