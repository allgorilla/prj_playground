# coding: utf-8
from pygame.locals import *
import pygame

#-------------------------------------------------------------------------------
# マップ上のオブジェクトのベースクラス
#-------------------------------------------------------------------------------
class ObjectBase:

    #-------------------------------------------------------------------------------
    # Public
    #-------------------------------------------------------------------------------
    pygame     = None
    fcur       = None
    fmax       = None
    pos        = None
    block      = None
    dir_x      = None

    #-------------------------------------------------------------------------------
    # Private
    #-------------------------------------------------------------------------------

    #-------------------------------------------------------------------------------
    # コンストラクタ
    #-------------------------------------------------------------------------------
    def __init__( self, pygame, pos, block, fmax ):

        self.pygame   = pygame
        self.pos      = pos
        self.block    = block
        self.fmax     = fmax
        self.fcur     = 0
        self.dir_x    = -1
        self.img_list = []
        self.img_lr   = []

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
    def update_input( self, cursor, map, move, view ):
        return view

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
    def draw( self, screen, view_pos, move ):

        if self.dir_x == -1:
            # 左向き画像
            image = self.img_lr[ 0 ]
        elif self.dir_x == 1:
            # 右向き画像
            image = self.img_lr[ 1 ]

        move_x, move_y = move.get_move_offset()
        x = self.pos[ 0 ] - view_pos[ 0 ] + ( screen.get_width() / self.block[ 0 ] ) / 2
        y = self.pos[ 1 ] - view_pos[ 1 ] + ( screen.get_height() / self.block[ 1 ] ) / 2
        pos_x = ( x * self.block[ 0 ] ) - ( image.get_width() / 2 )
        pos_y = ( y * self.block[ 1 ] ) - ( self.block[ 1 ] / 2 ) - ( image.get_height() - self.block[ 1 ] )
        screen.blit( image, ( pos_x + move_x, pos_y + move_y ))

        return
