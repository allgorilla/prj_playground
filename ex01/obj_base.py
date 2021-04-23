# coding: utf-8
from pygame.locals import *
import pygame
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
    def __init__( self, pygame, pos, grid_wh, fmax ):

        self.pygame   = pygame
        self.loc_pos  = pos
        self.loc_ofs  = ( 0, 0 )
        self.grid_wh  = grid_wh
        self.fmax     = fmax
        self.fcur     = 0
        self.dir      = ( -1, 0 )
        self.view_pos = ( 0, 0 )
        self.view_ofs = ( 0, 0 )
        self.img_list = []
        self.img_lr   = []

        # 状態管理 - 移動量
        self.move = sts_move.StsMove()
        self.move.set_destination( 16 )
        self.move.set_block_size( grid_wh )
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
    # 状態を更新
    #-------------------------------------------------------------------------------
    def update_think( self, cursor, map, obj_list ):

        if self.move.get_direction() != ( 0, 0 ):
            self.move.make_progress()

        self.view_pos = obj_list[ 0 ].loc_pos
        self.view_ofs = obj_list[ 0 ].move.get_move_offset()
        self.loc_ofs  = self.move.get_move_offset()

        return

    #-------------------------------------------------------------------------------
    # 状態を更新
    #-------------------------------------------------------------------------------
    def update_animation( self ):

        self.fcur += 1
        if  self.fmax <= self.fcur:
            self.img_list.append( self.img_lr )
            self.img_lr = self.img_list.pop( 0 )
            self.fcur = 0

    #-------------------------------------------------------------------------------
    # 状態を更新
    #-------------------------------------------------------------------------------
    def update_move( self, map ):
        return

    #-------------------------------------------------------------------------------
    # プレイヤーを描画
    #-------------------------------------------------------------------------------
    def blit( self, screen, pos ):

        if self.dir == ( -1, 0 ):
            # 左向き画像
            image = self.img_lr[ 0 ]
        elif self.dir == ( 1, 0 ):
            # 右向き画像
            image = self.img_lr[ 1 ]

        ( vx, vy ) = self.view_ofs
        ( mx, my ) = self.loc_ofs
        x = ( pos[ 0 ] * self.grid_wh[ 0 ] ) + vx - mx
        y = ( pos[ 1 ] * self.grid_wh[ 1 ] ) + vy - my
        x = x  - ( image.get_width() / 2 )
        y = y  - ( image.get_height() - self.grid_wh[ 1 ] ) - ( self.grid_wh[ 1 ] / 2 )
        screen.blit( image, ( x, y ))

    #-------------------------------------------------------------------------------
    # プレイヤーを描画
    #-------------------------------------------------------------------------------
    def draw( self, screen ):

        x = ( screen.get_width() / self.grid_wh[ 0 ] ) / 2
        y = ( screen.get_height() / self.grid_wh[ 1 ] ) / 2
        x = x + self.loc_pos[ 0 ] - self.view_pos[ 0 ]
        y = y + self.loc_pos[ 1 ] - self.view_pos[ 1 ]
        self.blit( screen, ( x, y ))

        return
