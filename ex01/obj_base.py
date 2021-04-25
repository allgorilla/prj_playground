# coding: utf-8
from pygame.locals import *
import pygame
import random

import sts_move

#-------------------------------------------------------------------------------
# マップ上のオブジェクトのベースクラス
#-------------------------------------------------------------------------------
class ObjectBase:

    #-------------------------------------------------------------------------------
    # Public
    #-------------------------------------------------------------------------------

    #-------------------------------------------------------------------------------
    # Private
    #-------------------------------------------------------------------------------

    #-------------------------------------------------------------------------------
    # コンストラクタ
    #-------------------------------------------------------------------------------
    def __init__( self, pygame, pos, grid_wh, acnt, tcnt ):

        self.pygame   = pygame
        self.loc_pos  = pos
        self.loc_ofs  = ( 0, 0 )
        self.grid_wh  = grid_wh

        self.acnt_cur = 0
        self.acnt_max = acnt
        self.tcnt_cur = 0
        self.tcnt_max = tcnt

        self.imgdir      = ( -1, 0 )
        self.view_pos = ( 0, 0 )
        self.view_ofs = ( 0, 0 )
        self.blit_pos = ( 0, 0 )
        self.img_list = []
        self.img_lr   = []

        # 状態管理 - 移動量
        self.move = sts_move.StsMove()
        self.move.set_destination( 16 )
        self.move.set_grid_size( grid_wh )
        return

    #-------------------------------------------------------------------------------
    # パターンを追加
    #-------------------------------------------------------------------------------
    def add_pattern( self, filename ):

        image_lr = []

        # 画像ファイルを読み込み
        image = self.pygame.image.load( filename ).convert()

        # カラーキーを設定
        colorkey = image.get_at(( 0, 0 ))
        image.set_colorkey( colorkey, RLEACCEL )

        # 左向きイメージをリストに追加
        image_lr.append( image )

        # 右向きイメージをリストに追加
        image = self.pygame.transform.flip( image, True, False )
        image_lr.append( image )

        # 左右のセットをリストについて
        self.img_list.append( image_lr )

        # 1枚目のパターンだったら
        if 0 == len( self.img_lr ):
            # 最初に表示する画像なのでリストに追加せずに保持
            self.img_lr = self.img_list.pop( 0 )

    #-------------------------------------------------------------------------------
    # ランダムな方向を得る
    #-------------------------------------------------------------------------------
    def get_random_direction( self ):
        val = random.randint( 1, 4 )
        if val == 1:
            dir = ( -1, 0 )
        elif val == 2:
            dir = ( 1, 0 )
        elif val == 3:
            dir = ( 0, -1 )
        elif val == 4:
            dir = ( 0, 1 )
        else:
            dir = ( 0, 0 )

        return dir

    #-------------------------------------------------------------------------------
    # 進行方向を取得する
    #-------------------------------------------------------------------------------
    def get_direction( self, cursor ):

        self.tcnt_cur += 1
        if  self.tcnt_max <= self.tcnt_cur:
            dir = self.get_random_direction()
            self.tcnt_cur = 0
        else:
            dir = ( 0, 0 )

        return dir

    #-------------------------------------------------------------------------------
    # 座標を更新
    #-------------------------------------------------------------------------------
    def update_common( self, dir, map, obj_list ):

        if self.move.is_stop():
            # ブロックの侵入可否チェック
            pos = ( self.loc_pos[ 0 ] + dir[ 0 ], self.loc_pos[ 1 ] + dir[ 1 ] )
            if True == map.can_walk( pos ):
                self.loc_pos = pos
                self.move.set_direction( dir )
        else:
            self.move.make_progress()

        self.loc_ofs  = self.move.get_move_offset()

        # 左右反転
        if self.imgdir == ( -1, 0 )  and dir == ( 1, 0 ):
            self.imgdir = dir
        elif self.imgdir == ( 1, 0 ) and dir == ( -1, 0 ):
            self.imgdir = dir

        self.view_pos = obj_list[ 0 ].loc_pos
        self.view_ofs = obj_list[ 0 ].move.get_move_offset()

    #-------------------------------------------------------------------------------
    # 状態を更新
    #-------------------------------------------------------------------------------
    def update_think( self, cursor, map, obj_list ):

        dir = self.get_direction( cursor )
        self.update_common( dir, map, obj_list )
        return

    #-------------------------------------------------------------------------------
    # 状態を更新
    #-------------------------------------------------------------------------------
    def update_animation( self ):

        self.acnt_cur += 1
        if  self.acnt_max <= self.acnt_cur:
            self.img_list.append( self.img_lr )
            self.img_lr = self.img_list.pop( 0 )
            self.acnt_cur = 0

    #-------------------------------------------------------------------------------
    # 状態を更新
    #-------------------------------------------------------------------------------
    def update_move( self, map ):
        return

    #-------------------------------------------------------------------------------
    # プレイヤーを描画
    #-------------------------------------------------------------------------------
    def set_blit_pos( self, screen ):

        x = ( screen.get_width() / self.grid_wh[ 0 ] ) / 2
        y = ( screen.get_height() / self.grid_wh[ 1 ] ) / 2
        x = x + self.loc_pos[ 0 ] - self.view_pos[ 0 ]
        y = y + self.loc_pos[ 1 ] - self.view_pos[ 1 ]

        ( vx, vy ) = self.view_ofs
        ( mx, my ) = self.loc_ofs
        x = ( x * self.grid_wh[ 0 ] ) + vx - mx
        y = ( y * self.grid_wh[ 1 ] ) + vy - my
        self.blit_pos = ( x, y )

    #-------------------------------------------------------------------------------
    # プレイヤーを描画
    #-------------------------------------------------------------------------------
    def draw( self, screen ):

        if self.imgdir == ( -1, 0 ):
            # 左向き画像
            image = self.img_lr[ 0 ]
        elif self.imgdir == ( 1, 0 ):
            # 右向き画像
            image = self.img_lr[ 1 ]

        ( x, y ) = self.blit_pos
        x = x - ( image.get_width() / 2 )
        y = y - ( image.get_height() - self.grid_wh[ 1 ] ) - ( self.grid_wh[ 1 ] / 2 )
        screen.blit( image, ( x, y ))

        return
