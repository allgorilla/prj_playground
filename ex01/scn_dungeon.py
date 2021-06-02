# coding: utf-8
from pygame.locals import *
import pygame
import sys
import time
import threading
import copy

import scn_base
import srf_map
import srf_wipe_btl
import sts_cursor

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
    __map      = None
    __cursor   = None
    __cnt      = None
    __t_flag   = False

    #-------------------------------------------------------------------------------
    # コンストラクタ
    #-------------------------------------------------------------------------------
    def __init__( self, pygame, screen ):

        self.__pygame = pygame
        self.__screen = screen
        self.scene  = scn_base.EnumScene.Dungeon

        # 状態管理 - カーソル
        self.__cursor = sts_cursor.StsCursor()

        # ワイプエフェクト
        self.__wipe = srf_wipe_btl.SrfWipeBattle( self.__pygame, 8 )

        self.__param_list = []
        return

    #-------------------------------------------------------------------------------
    # 周期処理開始
    #-------------------------------------------------------------------------------
    def begin( self, param_list ):

        self.__map = param_list.pop( 0 )
        portal_num = param_list.pop( 0 )
        self.__map.set_start_pos( portal_num )

        self.scene  = scn_base.EnumScene.Dungeon
        self.changed = False
        self.__cnt = 0
        self.__scene_state = scn_base.EnumSceneState.Opening
        print("ステートを再設定")

        self.__cursor.first_flag = True

        self.__wipe.begin( srf_wipe_btl.EnumWipeStatus.WIPE_SPREAD )

        if None == self.__thread:
            self.__t_flag = True
            self.__thread = threading.Thread( target = self.__update )
            self.__thread.setDaemon( True )
            self.__thread.start()
        else:
            self.__t_flag = False

        # オブジェクトアニメーション
        self.__map.reset_follower_pos()
        self.__map.update( self.__cursor )

    #-------------------------------------------------------------------------------
    # シーン終了
    #-------------------------------------------------------------------------------
    def end( self ):
        self.__t_flag = False
        self.__cursor.clear_event()
        self.__wipe.end()

        param_list = copy.copy( self.__param_list )
        self.__param_list.clear()

        self.__thread.join()
        self.__thread = None

        return param_list

    #-------------------------------------------------------------------------------
    # 周期更新
    #-------------------------------------------------------------------------------
    def __update( self ):

        while False != self.__t_flag:
            # システムとの同期
            self.__pygame.event.pump()
            self.__pygame.time.wait( 16 )

            if self.__scene_state == scn_base.EnumSceneState.Opened:

                # オブジェクトアニメーション
                self.__map.update( self.__cursor )

                # ポータル侵入チェック
                for object in self.__map.obj_list:
                    if object.find_contact_trigger( self.__map.obj_list ):
                        if object.type == "PORTAL":
                            if self.__cursor.first_flag == False:
                                self.__wipe.begin( srf_wipe_btl.EnumWipeStatus.WIPE_SHRINK )
                                self.__scene_state = scn_base.EnumSceneState.Closing

            elif self.__scene_state == scn_base.EnumSceneState.Closed:
                self.__param_list.append( self.__map )
                self.__param_list.append( 0 )
                self.change( scn_base.EnumScene.Dungeon )
                print( "Closed2" )
                return

            elif self.__scene_state == scn_base.EnumSceneState.Opening:
                if self.__wipe.get_state() == srf_wipe_btl.EnumWipeStatus.WIPE_COMPLETELY:
                    self.__scene_state = scn_base.EnumSceneState.Opened
                    print( "Opened1" )
                else:
                    # ワイプエフェクト
                    self.__wipe.make_progress()

            elif self.__scene_state == scn_base.EnumSceneState.Closing:
                if self.__wipe.get_state() == srf_wipe_btl.EnumWipeStatus.FILL_COMPLETELY:
                    self.__scene_state = scn_base.EnumSceneState.Closed
                    print( "Closed1" )
                else:
                    # ワイプエフェクト
                    self.__wipe.make_progress()
            else:
                pass

    #-------------------------------------------------------------------------------
    # 描画
    #-------------------------------------------------------------------------------
    def draw( self ):

        # 床と壁の表示
        self.__map.draw( self.__screen )
        self.__map.blit( self.__screen )

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
