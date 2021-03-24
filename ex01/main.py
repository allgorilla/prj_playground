from pygame.locals import *
import pygame
import sys

import scn_base
import scn_dungeon
import scn_battle

SCREEN_H = ( 512 )
SCREEN_W = ( 640 )

#-------------------------------------------------------------------------------
# Main関数
#-------------------------------------------------------------------------------
def main():

    scene_list = []

    # Pygameを初期化
    pygame.init()

    # 画面サーフェースを作成
    screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))

    # タイトルを作成
    pygame.display.set_caption("Pygame sample app")

    # シーンオブジェクトを作成
    scene_list.append( scn_dungeon.SceneDungeon( pygame, screen ) )
    scene_list.append( scn_battle.SceneBattle( pygame, screen ) )
    scene = scene_list[ 0 ]
    scene.begin()

    # メインループ
    while True:

        # シーン切り替え
        if True == scene.is_changed():
            scene.end()
            scene = scene_list[ scene.get_scene() ]
            scene.begin()

        # 描画
        scene.draw()

        # 入力
        scene.input()

if __name__=="__main__":
    main()
