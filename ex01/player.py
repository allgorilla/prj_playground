# coding: utf-8
from pygame.locals import *
import pygame

PLAYER_H = 80
PLAYER_W = 80

g_img_human_a = None
g_img_human_b = None

#-------------------------------------------------------------------------------
# 移動マネージャークラス
#-------------------------------------------------------------------------------
class Player:

    __pygame     = None
    __screen     = None
    __fcnt       = None
    __fcnt_max   = None
    __ptn_list   = []
    __image      = None
    __block_w    = None
    __block_h    = None

    #-------------------------------------------------------------------------------
    # コンストラクタ
    #-------------------------------------------------------------------------------
    def __init__( self, pygame, screen, fcnt_max, block_w, block_h ):

        global g_img_human_a
        global g_img_human_b

        self.__pygame   = pygame
        self.__screen   = screen
        self.__fcnt     = 0
        self.__fcnt_max = fcnt_max
        self.__block_w  = block_w
        self.__block_h  = block_h

        # プレイヤー読み込み "a"
        g_img_human_a = self.__pygame.image.load("human_a.bmp").convert()
        colorkey = g_img_human_a.get_at(( 0, 0 ))
        g_img_human_a.set_colorkey(colorkey, RLEACCEL)

        # プレイヤー読み込み "b"
        g_img_human_b = self.__pygame.image.load("human_b.bmp").convert()
        colorkey = g_img_human_b.get_at(( 0, 0 ))
        g_img_human_b.set_colorkey(colorkey, RLEACCEL)

        # パターンリストの作成
        self.__ptn_list.append( g_img_human_a )
        self.__ptn_list.append( g_img_human_b )
        self.__image = self.__ptn_list.pop( 0 )

        return

    #-------------------------------------------------------------------------------
    # プレイヤーを描画
    #-------------------------------------------------------------------------------
    def update( self ):

        self.__fcnt += 1
        if  self.__fcnt_max <= self.__fcnt:
            self.__ptn_list.append( self.__image )
            self.__image = self.__ptn_list.pop( 0 )
            self.__fcnt  = 0

    #-------------------------------------------------------------------------------
    # プレイヤーを描画
    #-------------------------------------------------------------------------------
    def draw( self, screen, x, y  ):

        pos_x = ( x * self.__block_w ) - ( PLAYER_W / 2 )
        pos_y = ( y * self.__block_h ) - ( self.__block_h / 2 ) - ( PLAYER_H - self.__block_h )
        screen.blit( self.__image, ( pos_x, pos_y ))

        return
