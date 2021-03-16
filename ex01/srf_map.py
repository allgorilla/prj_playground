# coding: utf-8
from pygame.locals import *
import pygame

DOTCOL_START_POS = (0,0,255,255)
DOTCOL_FLOOR = (255,255,255,255)
DOTCOL_WALL = (0,0,0,255)

g_img_map   = None
g_img_black = None
g_img_floor = None
g_img_wall  = None

#-------------------------------------------------------------------------------
# ブロックマップ
#-------------------------------------------------------------------------------
class SrfMap:

    __pygame  = None
    __scr     = None
    __map_w   = None
    __map_h   = None
    __block_w = None
    __block_h = None

    #-------------------------------------------------------------------------------
    # コンストラクタ
    # param(in) pygameオブジェクト
    # param(in) screenオブジェクト
    # param(in) マップのサイズ(X方向ブロック数)
    # param(in) マップのサイズ(Y方向ブロック数)
    # param(in) ブロックのサイズ(X方向ドット数)
    # param(in) ブロックのサイズ(Y方向ドット数)
    #-------------------------------------------------------------------------------
    def __init__( self, pygame, screen, filename, map_w, map_h, block_w, block_h ):

        global g_img_map
        global g_img_black
        global g_img_floor
        global g_img_wall

        self.__pygame  = pygame
        self.__scr     = screen
        self.__map_w   = map_w
        self.__map_h   = map_h
        self.__block_w = block_w
        self.__block_h = block_h

        # マップ読み込み
        g_img_map = self.__pygame.image.load( filename )

        # イメージの読み込み
        g_img_black = self.__pygame.image.load( "image/black_64.bmp" )
        g_img_floor = self.__pygame.image.load( "image/floor.bmp" )
        g_img_wall  = self.__pygame.image.load( "image/wall.bmp" )

        return

    #-------------------------------------------------------------------------------
    # スタート位置を取得する
    #-------------------------------------------------------------------------------
    def get_start_pos( self ):

        rect = g_img_map.get_rect()
        for y in range( rect.top, rect.bottom ):
            for x in range( rect.left, rect.right ):
                color = g_img_map.get_at(( x, y ))
                if color == DOTCOL_START_POS:
                    return True, x, y

        return False, 0, 0

    #-------------------------------------------------------------------------------
    # 画像表示（ブロック指定）
    #-------------------------------------------------------------------------------
    def __put_block( self, move, img, x, y ):

        pos_x = ( x * self.__block_w ) - ( self.__block_w / 2 )
        pos_y = ( y * self.__block_h ) - ( self.__block_h / 2 )
        move_x, move_y = move.get_move_offset()
        self.__scr.blit( img, ( pos_x + move_x, pos_y + move_y ))

        return

    #-------------------------------------------------------------------------------
    # ブロックマップの表示
    # param(in) screenオブジェクト
    # param(in) 移動中の方向
    # param(in) プレイヤーのマップ上の現在地(X方向)
    # param(in) プレイヤーのマップ上の現在地(Y方向)
    #-------------------------------------------------------------------------------
    def draw( self, move, cx, cy ):

        rect = g_img_map.get_rect()
        bx = int( self.__map_w / 2 ) # マップ→ウインドウの表示範囲の補正値(X方向)
        by = int( self.__map_h / 2 ) # マップ→ウインドウの表示範囲の補正値(Y方向)
        sx = bx                      # マップの表示範囲の開始ブロック(X方向)
        sy = by                      # マップの表示範囲の開始ブロック(Y方向)
        ex = bx + 1                  # マップの表示範囲の終端ブロック(X方向)
        ey = by + 1                  # マップの表示範囲の終端ブロック(Y方向)

        dir = move.get_direction()
        if dir[ 0 ] == 1:
            sx += 1
        elif dir[ 0 ] == -1:
            ex += 1

        if dir[ 1 ] == 1:
            sy += 1
        elif dir[ 1 ] == -1:
            ey += 1

        for oy in range( -sy, ey ):
            for ox in range( -sx, ex ):

                mx = ox + cx # マップから読みだす対象のX座標
                my = oy + cy # マップから読みだす対象のY座標

                img = g_img_black
                if mx >= rect.left and mx < rect.right:
                    if my >= rect.top and my < rect.bottom:
                        dotcol = g_img_map.get_at(( mx, my ))
                        if dotcol == DOTCOL_START_POS:
                            img = g_img_floor
                        elif dotcol == DOTCOL_FLOOR:
                            img = g_img_floor
                        elif dotcol == DOTCOL_WALL:
                            img = g_img_wall
                self.__put_block( move, img, ox + bx, oy + by )

        return

    #-------------------------------------------------------------------------------
    # マップイメージの範囲チェック
    #-------------------------------------------------------------------------------
    def __is_out_of_map( self, x, y ):

        rect = g_img_map.get_rect()
        if rect.top <= x and x < rect.bottom:
            if rect.left <= y and y < rect.right:
                return False

        return True

    #-------------------------------------------------------------------------------
    # ブロックの侵入可否チェック
    #-------------------------------------------------------------------------------
    def can_walk( self, x, y ):

        # マップイメージの範囲外に出る場合侵入不可
        if True == self.__is_out_of_map( x, y ):
            return False

        elif DOTCOL_WALL != g_img_map.get_at(( x, y )):
            return True

        return False
