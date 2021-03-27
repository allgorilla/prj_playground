# coding: utf-8
from pygame.locals import *
import pygame
import sys
import time
import threading

import scn_base
import srf_wipe_btl

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
    __wipe    = None
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

        # ワイプエフェクト
        self.__wipe = srf_wipe_btl.SrfWipeBattle( self.__pygame, self.__screen, 8 )

        return

    #-------------------------------------------------------------------------------
    # シーン開始
    #-------------------------------------------------------------------------------
    def begin( self ):

        self.scene  = scn_base.EnumScene.Battle
        self.changed = False

        # ワイプエフェクト
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

            # ワイプエフェクト
            self.__wipe.make_progress()

            state = srf_wipe_btl.EnumWipeStatus.FILL_COMPLETELY
            if state == self.__wipe.get_state():
                self.change( scn_base.EnumScene.Dungeon )

    #-------------------------------------------------------------------------------
    # 描画
    #-------------------------------------------------------------------------------
    def draw( self ):

        # 画像を描画
        self.__screen.blit( self.__image, ( 0, 0 ))

        # ワイプエフェクト
        self.__wipe.draw()

    #-------------------------------------------------------------------------------
    # キー入力
    #-------------------------------------------------------------------------------
    def input( self ):

        for event in self.__pygame.event.get():

            # 終了イベント
            if event.type == QUIT:
                self.change( scn_base.EnumScene.Quit )

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

        return
