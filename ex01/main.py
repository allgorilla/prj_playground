from pygame.locals import *
import pygame
import sys
import dungeon

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

    # Pygameを初期化
    pygame.init()
    # 画面を作成
    g_screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
    # タイトルを作成
    pygame.display.set_caption("Pygame sample app")

    # シーンオブジェクトを作成
    g_scene = dungeon.SceneDungeon( pygame, g_screen )

    # 周期処理の開始
    g_scene.start()

    # メインループ
    while True:

        g_scene.draw()
        g_scene.input()

if __name__=="__main__":
    main()
