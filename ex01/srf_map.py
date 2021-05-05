# coding: utf-8
from pygame.locals import *
import pygame

DOTCOL_PORTAL = (0,0,255,255)
DOTCOL_ENEMY = (255,0,0,255)
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

    __pygame         = None
    __map_wh         = None
    __block_wh       = None
    __enemy_pos_list = []
    __portal_pos_list = []

    #-------------------------------------------------------------------------------
    # コンストラクタ
    # param(in) pygameオブジェクト
    # param(in) screenオブジェクト
    # param(in) マップのサイズ(X方向ブロック数)
    # param(in) マップのサイズ(Y方向ブロック数)
    # param(in) ブロックのサイズ(X方向ドット数)
    # param(in) ブロックのサイズ(Y方向ドット数)
    #-------------------------------------------------------------------------------
    def __init__( self, pygame, filename, map_wh, block_wh ):

        global g_img_map
        global g_img_black
        global g_img_floor
        global g_img_wall

        self.__pygame   = pygame
        self.__map_wh   = map_wh
        self.__block_wh = block_wh

        self.__enemy_pos_list  = []
        self.__portal_pos_list = []

        # マップ読み込み
        g_img_map = self.__pygame.image.load( filename )

        # イメージの読み込み
        g_img_black = self.__pygame.image.load( "image/black_64.bmp" )
        g_img_floor = self.__pygame.image.load( "image/floor.bmp" )
        g_img_wall  = self.__pygame.image.load( "image/wall.bmp" )

        for y in range( 0, g_img_map.get_height() ):
            for x in range( 0, g_img_map.get_width() ):
                pos = ( x, y )
                dotcol = g_img_map.get_at( pos )
                if dotcol == DOTCOL_PORTAL:
                    self.__portal_pos_list.append( pos )
                elif dotcol == DOTCOL_ENEMY:
                    self.__enemy_pos_list.append( pos )
        return

    #-------------------------------------------------------------------------------
    # 画像表示（ブロック指定）
    #-------------------------------------------------------------------------------
    def __put_block( self, screen, move, img, pos ):

        pos_x = ( self.__block_wh[ 0 ] * pos[ 0 ] ) - ( self.__block_wh[ 0 ] / 2 )
        pos_y = ( self.__block_wh[ 1 ] * pos[ 1 ] ) - ( self.__block_wh[ 1 ] / 2 )
        move_x, move_y = move.get_move_offset()
        screen.blit( img, ( pos_x + move_x, pos_y + move_y ) )

        return

    #-------------------------------------------------------------------------------
    # ブロックマップの表示
    # param(in) screenオブジェクト
    # param(in) 移動中の方向
    # param(in) プレイヤーのマップ上の現在地(X方向)
    # param(in) プレイヤーのマップ上の現在地(Y方向)
    #-------------------------------------------------------------------------------
    def draw( self, screen, view_pos, move ):

        rect = g_img_map.get_rect()
        bx = int( self.__map_wh[ 0 ] / 2 ) # マップ→ウインドウの表示範囲の補正値(X方向)
        by = int( self.__map_wh[ 1 ] / 2 ) # マップ→ウインドウの表示範囲の補正値(Y方向)
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

                mx = ox + view_pos[ 0 ] # マップから読みだす対象のX座標
                my = oy + view_pos[ 1 ] # マップから読みだす対象のY座標

                img = g_img_black
                if mx >= rect.left and mx < rect.right:
                    if my >= rect.top and my < rect.bottom:
                        dotcol = g_img_map.get_at(( mx, my ))
                        if dotcol == DOTCOL_PORTAL:
                            img = g_img_floor
                        elif dotcol == DOTCOL_FLOOR:
                            img = g_img_floor
                        elif dotcol == DOTCOL_ENEMY:
                            img = g_img_floor
                        elif dotcol == DOTCOL_WALL:
                            img = g_img_wall
                self.__put_block( screen, move, img, ( ox + bx, oy + by ) )

        return

    #-------------------------------------------------------------------------------
    # マップイメージの範囲チェック
    #-------------------------------------------------------------------------------
    def __is_out_of_map( self, pos ):

        ( x, y ) = pos
        rect = g_img_map.get_rect()
        if rect.top <= x and x < rect.bottom:
            if rect.left <= y and y < rect.right:
                return False

        return True

    #-------------------------------------------------------------------------------
    # ブロックの侵入可否チェック
    #-------------------------------------------------------------------------------
    def can_walk( self, pos ):

        # マップイメージの範囲外に出る場合侵入不可
        if True == self.__is_out_of_map( pos ):
            return False

        elif DOTCOL_WALL != g_img_map.get_at( pos ):
            return True

        return False
    #-------------------------------------------------------------------------------
    # 敵の座標を１つ取得
    #-------------------------------------------------------------------------------
    def get_enemy_pos( self ):
        if 0 == len( self.__enemy_pos_list ):
            print( "★エラー：エネミーリストが空っぽです" )
            return ( -1, -1 )
        else:
            return self.__enemy_pos_list.pop( 0 )

    #-------------------------------------------------------------------------------
    # ポータルの座標を１つ取得
    #-------------------------------------------------------------------------------
    def get_portal_pos( self ):
        if 0 == len( self.__portal_pos_list ):
            print( "★エラー：ポータルリストが空っぽです" )
            return ( -1, -1 )
        else:
            return self.__portal_pos_list.pop( 0 )

    #-------------------------------------------------------------------------------
    # プレイヤーの開始座標を取得
    #-------------------------------------------------------------------------------
    def get_start_pos( self ):
        return self.__portal_pos_list[ 0 ]

