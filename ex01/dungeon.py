# coding: utf-8
from pygame.locals import *
import pygame
import sys
import movemgr

SCREEN_X = 10
SCREEN_Y = 8

CELL_H = 64
CELL_W = 64
PLAYER_H = 80
PLAYER_W = 80

DOTCOL_START_POS = (0,0,255,255)
DOTCOL_FLOOR = (255,255,255,255)
DOTCOL_WALL = (0,0,0,255)

g_img_black = None
g_img_floor = None
g_img_wall  = None
g_img_map   = None
g_img_human = None

#-------------------------------------------------------------------------------
# スタート位置を取得する
#-------------------------------------------------------------------------------
def get_start_pos(img):

    rect = img.get_rect()
    for y in range(rect.top,rect.bottom):
        for x in range(rect.left,rect.right):
            color = img.get_at((x,y))
            if color == DOTCOL_START_POS:
                return True,x,y

    return False,0,0

#-------------------------------------------------------------------------------
# 画像表示（ブロック指定）
#-------------------------------------------------------------------------------
def put_block( screen, move, img, x, y ):

    pos_x = ( x * CELL_W ) - ( CELL_W / 2 )
    pos_y = ( y * CELL_H ) - ( CELL_H / 2 )
    move_x, move_y = move.get_move_offset()
    screen.blit( img, ( pos_x + move_x, pos_y + move_y ))
    return
#-------------------------------------------------------------------------------
# プレイヤー表示（ブロック指定）
#-------------------------------------------------------------------------------
def put_player( screen, img, x, y ):

    pos_x = ( x * CELL_W ) - ( PLAYER_W/2 )
    pos_y = ( y * CELL_H ) - ( CELL_H/2 ) - ( PLAYER_H - CELL_H )
    screen.blit( img, ( pos_x, pos_y ))
    return

#-------------------------------------------------------------------------------
# 床と壁のループ表示
#-------------------------------------------------------------------------------
def put_floor_and_wall( screen, move, center_x, center_y ):
    global g_img_map
    global g_img_floor
    global g_img_wall

    rect = g_img_map.get_rect()
    sx = int( SCREEN_X / 2 )
    sy = int( SCREEN_Y / 2 )

    for ofs_y in range( -sy, sy+1 ):
        for ofs_x in range( -sx, sx+1 ):

            x = ofs_x + center_x
            y = ofs_y + center_y

            img = g_img_black
            if x >= rect.left and x < rect.right:
                if y >= rect.top and y < rect.bottom:
                    dotcol = g_img_map.get_at(( x, y ))
                    if dotcol == DOTCOL_START_POS:
                        img = g_img_floor
                    elif dotcol == DOTCOL_FLOOR:
                        img = g_img_floor
                    elif dotcol == DOTCOL_WALL:
                        img = g_img_wall
            put_block( screen, move, img, ofs_x + sx, ofs_y + sy )

    return

#-------------------------------------------------------------------------------
# 移動マネージャークラス
#-------------------------------------------------------------------------------
class SceneDungeon:

    #-------------------------------------------------------------------------------
    # メンバ（Private）
    #-------------------------------------------------------------------------------
    __pygame = None
    __scr    = None
    __mv     = None
    __px     = None
    __py     = None

    #-------------------------------------------------------------------------------
    # コンストラクタ
    #-------------------------------------------------------------------------------
    def __init__( self, pygame, screen ):
        global g_img_black
        global g_img_floor
        global g_img_wall
        global g_img_map
        global g_img_human

        self.__pygame = pygame
        self.__scr    = screen

        # マップ読み込み
        g_img_map = self.__pygame.image.load("map.bmp")
        find,self.__px,self.__py = get_start_pos(g_img_map)

        if find == False:
            print("")
            print("【異常終了】マップにスタート地点が見つかりません")
            print("")
            return

        # イメージの読み込み
        g_img_black = self.__pygame.image.load("black_64.bmp")
        g_img_floor = self.__pygame.image.load("floor.bmp")
        g_img_wall  = self.__pygame.image.load("wall.bmp")

        # プレイヤー読み込み
        g_img_human = self.__pygame.image.load("human_80.bmp").convert()
        colorkey = g_img_human.get_at((0,0))
        g_img_human.set_colorkey(colorkey, RLEACCEL)

        self.__mv = movemgr.MoveMgr()
        self.__mv.set_destination( 10 )
        self.__mv.set_block_size( CELL_H, CELL_W )
        return
    #-------------------------------------------------------------------------------
    # 描画
    #-------------------------------------------------------------------------------
    def draw( self ):
        global g_img_human

        # 画面を塗りつぶす
        self.__scr.fill(( 128, 128, 128 ))

        # 床と壁の表示
        put_floor_and_wall( self.__scr, self.__mv, self.__px,self.__py )

        #プレイヤーの表示
        put_player( self.__scr, g_img_human, SCREEN_X / 2, SCREEN_Y / 2 )

        # 描画処理を実行
        self.__pygame.display.update()

        return

    #-------------------------------------------------------------------------------
    # キー入力
    #-------------------------------------------------------------------------------
    def input( self ):
        # 移動オフセット進捗
        if self.__mv.get_direction() != ( 0, 0 ):
            self.__pygame.time.wait( 16 );
            self.__mv.make_progress()
        else:
            for event in self.__pygame.event.get():

                # 終了イベント
                if event.type == QUIT:  
                    #pygameのウィンドウを閉じる
                    self.__pygame.quit() 
                    #システム終了
                    sys.exit()

                # キ－入力イベント
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.__pygame.quit()
                        sys.exit()
                    elif event.key == K_UP:
                        self.__py -= 1
                        self.__mv.set_direction( "up" )
                    elif event.key == K_DOWN:
                        self.__py += 1
                        self.__mv.set_direction( "down" )
                    elif event.key == K_LEFT:
                        self.__px -= 1
                        self.__mv.set_direction( "left" )
                    elif event.key == K_RIGHT:
                        self.__px += 1
                        self.__mv.set_direction( "right" )
        return
