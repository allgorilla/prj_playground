# coding: utf-8
from pygame.locals import *
import pygame
import sys
import time
import threading
from enum import IntEnum

#-------------------------------------------------------------------------------
# シーン列挙型
#-------------------------------------------------------------------------------
class EnumScene( IntEnum ):
    Dungeon = 0
    Battle  = 1
    Quit    = 2

#-------------------------------------------------------------------------------
# シーン状態列挙型
#-------------------------------------------------------------------------------
class EnumStatus( IntEnum ):
    Opening = 0
    Opened  = 1
    Closed  = 2
    Closing = 3

#-------------------------------------------------------------------------------
# シーンクラス
#-------------------------------------------------------------------------------
class SceneBase:

    #-------------------------------------------------------------------------------
    # メンバ（Public）
    #-------------------------------------------------------------------------------
    scene   = None
    changed = None

    #-------------------------------------------------------------------------------
    # シーン変更
    #-------------------------------------------------------------------------------
    def change( self, scene ):
        self.scene  = scene
        self.changed = True
        return

    #-------------------------------------------------------------------------------
    # シーン取得
    #-------------------------------------------------------------------------------
    def get_scene( self ):
        return self.scene

    #-------------------------------------------------------------------------------
    # シーン変更チェック
    #-------------------------------------------------------------------------------
    def is_changed( self ):
        return self.changed

