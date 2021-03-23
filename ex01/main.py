from pygame.locals import *
import pygame
import sys

import scn_base
import scn_dungeon
import scn_battle

SCREEN_H = ( 512 )
SCREEN_W = ( 640 )

#グローバルSurfaceを宣言
g_screen = None
g_scene = None

#-------------------------------------------------------------------------------
# Main関数
#-------------------------------------------------------------------------------
def main():
    global g_screen
    
    scene_list = []

    # Pygameを初期化
    pygame.init()
    # 画面を作成
    g_screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
    # タイトルを作成
    pygame.display.set_caption("Pygame sample app")

    # シーンオブジェクトを作成
    scene_list.append( scn_battle.SceneBattle( pygame, g_screen ) )
    scene_list.append( scn_dungeon.SceneDungeon( pygame, g_screen ) )
    g_scene = scene_list[ 1 ]
    g_scene.start()

    # メインループ
    while True:

        bak     = g_scene
        g_scene = scene_list[ g_scene.get_scene() ]
        if g_scene != bak:
            # 周期処理の開始
            g_scene.start()

        g_scene.draw()
        g_scene.input()

if __name__=="__main__":
    main()
