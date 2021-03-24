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

    # 画面サーフェースを作成
    g_screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))

    # タイトルを作成
    pygame.display.set_caption("Pygame sample app")

    # シーンオブジェクトを作成
    scene_list.append( scn_battle.SceneBattle( pygame, g_screen ) )
    scene_list.append( scn_dungeon.SceneDungeon( pygame, g_screen ) )
    g_scene = scene_list[ 1 ]
    g_scene.begin()

    # メインループ
    while True:

        # シーン切り替え
        if True == g_scene.is_changed():
            g_scene.end()
            g_scene = scene_list[ g_scene.get_scene() ]
            g_scene.begin()

        # 描画
        g_scene.draw()

        # 入力
        g_scene.input()

if __name__=="__main__":
    main()
