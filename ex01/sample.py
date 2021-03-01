from pygame.locals import *
import pygame
import sys


CELL_H = 64
CELL_W = 64
PLAYER_H = 80
PLAYER_W = 80
SCREEN_H = (CELL_H*10)
SCREEN_W = (CELL_W*8)


DOTCOL_START_POS = (0,0,255,255)
DOTCOL_FLOOR = (255,255,255,255)
DOTCOL_WALL = (0,0,0,255)

#グローバルSurfaceを宣言
g_screen = None
g_img_floor = None
g_img_wall = None
g_img_map = None

#-------------------------------------------------------------------------------
# 画像表示（ブロック指定）
#-------------------------------------------------------------------------------
def put_img( img, x, y ):
    global g_screen

    pos_x = ( x * CELL_W ) - ( CELL_W/2 )
    pos_y = ( y * CELL_H ) - ( CELL_H/2 )
    g_screen.blit( img, ( pos_x, pos_y ))
    return
#-------------------------------------------------------------------------------
# プレイヤー表示（ブロック指定）
#-------------------------------------------------------------------------------
def put_player( img, x, y ):
    global g_screen

    pos_x = ( x * CELL_W ) - ( PLAYER_W/2 )
    pos_y = ( y * CELL_H ) - ( CELL_H/2 ) - ( PLAYER_H - CELL_H )
    g_screen.blit( img, ( pos_x, pos_y ))
    return

#-------------------------------------------------------------------------------
# 床と壁のループ表示
#-------------------------------------------------------------------------------
def put_floor_and_wall( center_x, center_y ):
    global g_img_map
    global g_img_floor
    global g_img_wall

    for ofs_y in range( -4, +5 ):
        for ofs_x in range( -5, +6 ):
            x = ofs_x + center_x
            y = ofs_y + center_y
            dotcol = g_img_map.get_at(( x, y ))
            if dotcol == DOTCOL_START_POS or dotcol == DOTCOL_FLOOR:
                put_img( g_img_floor, ofs_x + 5, ofs_y + 4 )
            elif dotcol == DOTCOL_WALL:
                put_img( g_img_wall, ofs_x + 5, ofs_y + 4 )

    return

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
# Main関数
#-------------------------------------------------------------------------------
def main():
    global g_screen
    global g_img_map
    global g_img_floor
    global g_img_wall

    # Pygameを初期化
    pygame.init()
    # 画面を作成
    g_screen = pygame.display.set_mode((SCREEN_H, SCREEN_W))
    # タイトルを作成
    pygame.display.set_caption("Pygame sample app")

    #マップ読み込み
    g_img_map = pygame.image.load("map.bmp")
    find,cur_x,cur_y = get_start_pos(g_img_map)

    if find == False:
        print("")
        print("【異常終了】マップにスタート地点が見つかりません")
        print("")
        return

    #床
    g_img_floor = pygame.image.load("floor.bmp")
    g_img_wall = pygame.image.load("wall.bmp")
    img_human = pygame.image.load("human_80.bmp").convert()
    colorkey = img_human.get_at((0,0))
    img_human.set_colorkey(colorkey, RLEACCEL)

    running = True
    #メインループ
    while running:
        g_screen.fill((0,128,128))  #画面を塗りつぶす
        #床と壁の表示
        put_floor_and_wall( cur_x,cur_y )
        #プレイヤーの表示
        put_player(img_human,5,4)

        pygame.display.update() #描画処理を実行
        for event in pygame.event.get():
            if event.type == QUIT:  # 終了イベント
                running = False
                pygame.quit()  #pygameのウィンドウを閉じる
                sys.exit() #システム終了
                
if __name__=="__main__":
    main()
