from pygame.locals import *
import pygame
import sys

import scn_base
import scn_dungeon
import scn_battle
import scn_quit
import srf_map

SCREEN_H = ( 512 )
SCREEN_W = ( 640 )

#-------------------------------------------------------------------------------
# Main関数
#-------------------------------------------------------------------------------
def main():

    scene_list = []
    param_list = []

    # Pygameを初期化
    pygame.init()

    # 画面サーフェースを作成
    screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))

    # タイトルを作成
    pygame.display.set_caption("Pygame sample app")

    # マップ初期化
    cell_wh = ( 64, 64 )
    screen_wh = ( screen.get_width() / cell_wh[ 0 ], screen.get_height() / cell_wh[ 1 ])
    map = srf_map.SrfMap( pygame, "image/map1.bmp", screen_wh, cell_wh )

    # オブジェクト初期化
    map.add_party_object( "image/human", cell_wh, 20, 100 )
    map.add_party_object( "image/warrior", cell_wh, 20, 100 )
    map.add_party_object( "image/thief", cell_wh, 20, 100 )
    map.add_party_object( "image/mage", cell_wh, 20, 100 )

    for i in range( 18 ):
        map.add_enemy_object( "image/enemy_mino", cell_wh, 10, 20 )

    map.add_portal_object( "image/stairs_d", cell_wh, map, 0 )
    map.add_portal_object( "image/circle",   cell_wh, map, 2 )
    map.add_portal_object( "image/circle",   cell_wh, map, 1 )
    map.add_portal_object( "image/circle",   cell_wh, map, 3 )
    map.add_portal_object( "image/circle",   cell_wh, map, 4 )
    param_list.append( map )
    param_list.append( 4 )

    # シーンオブジェクトを作成
    scene_list.append( scn_dungeon.SceneDungeon( pygame, screen ) )
    scene_list.append( scn_battle.SceneBattle( pygame, screen ) )
    scene_list.append( scn_quit.SceneQuit( pygame, screen ) )
    scene = scene_list[ 0 ]
    scene.begin( param_list )

    # メインループ
    while True:

        # シーン切り替え
        if True == scene.is_changed():
            param_list = scene.end()
            scene = scene_list[ scene.get_scene() ]
            scene.begin( param_list )

        # 描画
        screen.fill(( 0, 0, 255 ))
        scene.draw()
        pygame.display.update()

        # 入力
        scene.input()

if __name__=="__main__":
    main()
