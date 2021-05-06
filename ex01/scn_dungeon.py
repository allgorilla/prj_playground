# coding: utf-8
from pygame.locals import *
import pygame
import sys
import time
import threading

import scn_base
import srf_map
import obj_party_player
import obj_party_follower
import obj_enemy_base
import obj_enemy_mummy
import obj_portal_base
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
    __obj_list = []

    #-------------------------------------------------------------------------------
    # コンストラクタ
    #-------------------------------------------------------------------------------
    def __init__( self, pygame, screen ):

        self.__pygame = pygame
        self.__screen = screen
        self.scene  = scn_base.EnumScene.Dungeon

        # マップ初期化
        cell_wh = ( 64, 64 )
        screen_wh = ( screen.get_width() / cell_wh[ 0 ], screen.get_height() / cell_wh[ 1 ])
        self.__map = srf_map.SrfMap( self.__pygame, "image/map1.bmp", screen_wh, cell_wh )

        # オブジェクト初期化
        self.add_party_object( "image/human", cell_wh, 20, 100 )
        self.add_party_object( "image/warrior", cell_wh, 20, 100 )
        self.add_party_object( "image/thief", cell_wh, 20, 100 )
        self.add_party_object( "image/mage", cell_wh, 20, 100 )

        for i in range( 6 ):
            self.add_enemy_object( "image/enemy_mino", cell_wh, 10, 20 )
            self.add_enemy_object( "image/enemy_mummy", cell_wh, 40, 100 )
            self.add_enemy_object( "image/enemy_dragon", cell_wh, 20, 50 )

        self.add_portal_object( "image/stairs_d", cell_wh, 20, 100 )
        self.add_portal_object( "image/circle", cell_wh, 20, 100 )
        self.add_portal_object( "image/circle", cell_wh, 20, 100 )
        self.add_portal_object( "image/circle", cell_wh, 20, 100 )
        self.add_portal_object( "image/circle", cell_wh, 20, 100 )

        # 状態管理 - カーソル
        self.__cursor = sts_cursor.StsCursor()

        # ワイプエフェクト
        self.__wipe = srf_wipe_btl.SrfWipeBattle( self.__pygame, 8 )

        return
    #-------------------------------------------------------------------------------
    # 敵を追加するサブルーチン
    #-------------------------------------------------------------------------------
    def add_party_object( self, file, cell_wh, acnt, tcnt ):
        if 0 == len( self.__obj_list ):
            pos = self.__map.get_start_pos()
            object = obj_party_player.ObjectPartyPlayer( self.__pygame, pos, cell_wh, acnt, tcnt )
        elif 0 < len( self.__obj_list ) and len( self.__obj_list ) < 4:
            pos = self.__obj_list[ 0 ].loc_pos
            object = obj_party_follower.ObjectPartyFollower( self.__pygame, pos, cell_wh, acnt, tcnt )

        object.add_pattern( file + "_a.png" )
        object.add_pattern( file + "_b.png" )
        self.__obj_list.append( object )

    #-------------------------------------------------------------------------------
    # 敵を追加するサブルーチン
    #-------------------------------------------------------------------------------
    def add_enemy_object( self, file, cell_wh, acnt, tcnt ):
        pos = self.__map.get_enemy_pos()
        object = obj_enemy_base.ObjectEnemyBase( self.__pygame, pos, cell_wh, acnt, tcnt )

        object.add_pattern( file + "_a.png" )
        object.add_pattern( file + "_b.png" )
        self.__obj_list.append( object )

    #-------------------------------------------------------------------------------
    # 敵を追加するサブルーチン
    #-------------------------------------------------------------------------------
    def add_portal_object( self, file, cell_wh, acnt, tcnt ):
        pos = self.__map.get_portal_pos()
        object = obj_portal_base.ObjectPortalBase( self.__pygame, pos, cell_wh, acnt, tcnt )
        object.add_pattern( file + ".png" )
        self.__obj_list.append( object )

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
            self.__thread.setDaemon( True )
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

            # オブジェクトアニメーション
            for object in self.__obj_list:
                object.update_think( self.__cursor, self.__map, self.__obj_list )
                object.update_animation()
                object.update_move( self.__map )

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
        self.__map.draw( self.__screen, self.__obj_list[ 0 ].loc_pos, self.__obj_list[ 0 ].move )

        # オブジェクトアニメーション
        for object in self.__obj_list:
            object.set_blit_pos( self.__screen )

        # 全オブジェクトの優先度リストを作成
        pri_list = []
        i = 0;
        for object in self.__obj_list:
            # Y座標は大きいほど優先
            y = object.blit_pos[ 1 ]
            x = len( self.__obj_list ) - i
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
            self.__obj_list[ index ].draw( self.__screen )

        # ワイプエフェクト
        self.__wipe.draw( self.__screen )

        # ポータル侵入チェック
        for object in self.__obj_list:
            if object.find_contact_trigger( self.__obj_list ):
                pass

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
