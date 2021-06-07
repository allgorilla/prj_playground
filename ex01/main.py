from pygame.locals import *
import pygame
import sys

import scn_base
import scn_dungeon
import scn_battle
import scn_quit
import map_t0
import map_d1
import map_d2

SCREEN_H = ( 512 )
SCREEN_W = ( 640 )

#-------------------------------------------------------------------------------
# Main関数
#-------------------------------------------------------------------------------
def main():

    scene_list = []
    param_list = []
    map_list   = []

    # Pygameを初期化
    pygame.init()

    # 画面サーフェースを作成
    screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))

    # タイトルを作成
    pygame.display.set_caption("Pygame sample app")

    # マップ初期化
    cell_wh = ( 64, 64 )
    screen_wh = ( screen.get_width() / cell_wh[ 0 ], screen.get_height() / cell_wh[ 1 ])
    map_list.append( map_t0.MapTown0( pygame, "image/town1.bmp", screen_wh, cell_wh ) )
    map_list.append( map_d1.MapDungeon1( pygame, "image/map1.bmp", screen_wh, cell_wh ) )
    map_list.append( map_d2.MapDungeon2( pygame, "image/map2.bmp", screen_wh, cell_wh ) )
    param_list.append( 0 )
    param_list.append( 25 )

    # シーンオブジェクトを作成
    scene_list.append( scn_dungeon.SceneDungeon( pygame, screen ) )
    scene_list.append( scn_battle.SceneBattle( pygame, screen ) )
    scene_list.append( scn_quit.SceneQuit( pygame, screen ) )
    scene = scene_list[ 0 ]
    scene.begin( param_list, map_list )

    # メインループ
    while True:

        # シーン切り替え
        if True == scene.is_changed():
            param_list = scene.end()
            scene = scene_list[ scene.get_scene() ]
            scene.begin( param_list, map_list )

        # 描画
        screen.fill(( 0, 0, 255 ))
        scene.draw()
        pygame.display.update()

        # 入力
        scene.input()

if __name__=="__main__":
    print( "                                                                                " )
    print( "--- PROGRAM START ---" )
    print( "                                                                                " )
    main()
