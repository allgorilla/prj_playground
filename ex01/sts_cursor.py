# coding: utf-8
from pygame.locals import *
import pygame

#-------------------------------------------------------------------------------
# 移動マネージャークラス
#-------------------------------------------------------------------------------
class StsCursor:

    __key_list = []

    #-------------------------------------------------------------------------------
    # コンストラクタ
    #-------------------------------------------------------------------------------
    def __init__( self ):
        pass
        return

    #-------------------------------------------------------------------------------
    # イベントを追加
    #-------------------------------------------------------------------------------
    def add_event( self, event ):

        # イベントタイプが範囲外
        if event.type != KEYDOWN:
            if event.type != KEYUP:
                return False

        # キーが範囲外
        if event.key != K_UP:
            if event.key != K_DOWN:
                if event.key != K_LEFT:
                    if event.key != K_RIGHT:
                        return False

        # イベントタイプがキーダウン
        if event.type == KEYDOWN:
            self.__key_list.append( event.key )
            return True

        # イベントタイプがキーアップ
        elif event.type == KEYUP:
            # 指定のキーイベントをリストから削除する
            self.__key_list = [ item for item in self.__key_list if item != event.key ]
            return True

    #-------------------------------------------------------------------------------
    # イベントをクリア
    #-------------------------------------------------------------------------------
    def clear_event( self ):
        self.__key_list.clear()
        return

    #-------------------------------------------------------------------------------
    # 進行方向を取得
    #-------------------------------------------------------------------------------
    def get_direction( self ):

        if 0 == len( self.__key_list ):
            return ( 0, 0 )

        key = self.__key_list[ -1 ]
        if key == K_UP:
            return ( 0, -1 )
        elif key == K_DOWN:
            return ( 0, +1 )
        elif key == K_LEFT:
            return ( -1, 0 )
        elif key == K_RIGHT:
            return ( +1, 0 )

        return ( 0, 0 )
