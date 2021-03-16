# coding: utf-8
from pygame.locals import *
import pygame

PLAYER_H = 80
PLAYER_W = 80

#-------------------------------------------------------------------------------
# 移動マネージャークラス
#-------------------------------------------------------------------------------
class Player:

    __pygame     = None
    __screen     = None
    __fcnt       = None
    __fcnt_max   = None
    __img_list   = []
    __image      = None
    __block_w    = None
    __block_h    = None
    __dir_x      = None

    #-------------------------------------------------------------------------------
    # コンストラクタ
    #-------------------------------------------------------------------------------
    def __init__( self, pygame, screen, fcnt_max, block_w, block_h ):

        self.__pygame   = pygame
        self.__screen   = screen
        self.__fcnt     = 0
        self.__fcnt_max = fcnt_max
        self.__block_w  = block_w
        self.__block_h  = block_h
        self.__dir_x    = -1

        return

    #-------------------------------------------------------------------------------
    # パターンを追加
    #-------------------------------------------------------------------------------
    def add_pattern( self, filename ):

        # パターンをimageリストに追加
        image = self.__pygame.image.load( filename ).convert()

        # カラーキーを設定
        colorkey = image.get_at(( 0, 0 ))
        image.set_colorkey( colorkey, RLEACCEL )

        self.__img_list.append( image )
        # 1枚目のパターンだったら
        if self.__image == None:
            # 最初に表示する画像なのでリストに追加せずに保持
            self.__image = self.__img_list.pop( 0 )

    #-------------------------------------------------------------------------------
    # プレイヤーを描画
    #-------------------------------------------------------------------------------
    def update( self, x ):

        # 左右反転
        if self.__dir_x == -1  and x == 1:
            self.__dir_x = x
        elif self.__dir_x == 1 and x == -1:
            self.__dir_x = x

        self.__fcnt += 1
        if  self.__fcnt_max <= self.__fcnt:
            self.__img_list.append( self.__image )
            self.__image = self.__img_list.pop( 0 )
            self.__fcnt  = 0

    #-------------------------------------------------------------------------------
    # プレイヤーを描画
    #-------------------------------------------------------------------------------
    def draw( self, x, y  ):

        if self.__dir_x == -1:
            image = self.__image
        elif self.__dir_x == 1:
            image = self.__pygame.transform.flip( self.__image, True, False )

        pos_x = ( x * self.__block_w ) - ( PLAYER_W / 2 )
        pos_y = ( y * self.__block_h ) - ( self.__block_h / 2 ) - ( PLAYER_H - self.__block_h )
        self.__screen.blit( image, ( pos_x, pos_y ))

        return
