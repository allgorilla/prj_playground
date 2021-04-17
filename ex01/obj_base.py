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
    fcnt       = None
    fcnt_max   = None
    img_list   = []
    img_lr     = []
    block_w    = None
    block_h    = None
    dir_x      = None

    #-------------------------------------------------------------------------------
    # Private
    #-------------------------------------------------------------------------------

    #-------------------------------------------------------------------------------
    # コンストラクタ
    #-------------------------------------------------------------------------------
    def __init__( self, pygame, fcnt_max, block_w, block_h ):

        self.pygame   = pygame
        self.fcnt     = 0
        self.fcnt_max = fcnt_max
        self.block_w  = block_w
        self.block_h  = block_h
        self.dir_x    = -1

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
    # プレイヤーを描画
    #-------------------------------------------------------------------------------
    def update( self, x ):

        # 左右反転
        if self.dir_x == -1  and x == 1:
            self.dir_x = x
        elif self.dir_x == 1 and x == -1:
            self.dir_x = x

        self.fcnt += 1
        if  self.fcnt_max <= self.fcnt:
            self.img_list.append( self.img_lr )
            self.img_lr = self.img_list.pop( 0 )
            self.fcnt = 0

    #-------------------------------------------------------------------------------
    # プレイヤーを描画
    #-------------------------------------------------------------------------------
    def draw( self, screen, x, y  ):

        if self.dir_x == -1:
            # 左向き画像
            image = self.img_lr[ 0 ]
        elif self.dir_x == 1:
            # 右向き画像
            image = self.img_lr[ 1 ]

        img_w = image.get_width()
        img_h = image.get_height()
        pos_x = ( x * self.block_w ) - ( img_w / 2 )
        pos_y = ( y * self.block_h ) - ( self.block_h / 2 ) - ( img_h - self.block_h )
        screen.blit( image, ( pos_x, pos_y ))

        return
