# coding: utf-8
from pygame.locals import *
import pygame
from enum import Enum, auto

#-------------------------------------------------------------------------------
# シーン列挙型
#-------------------------------------------------------------------------------
class EnumFadeStatus( Enum ):

    FILL_COMPLETLY = auto()
    FILL_SPREAD    = auto()
    FILL_SHRINK    = auto()
    WIPE_COMPLETLY = auto()
    WIPE_SPREAD    = auto()
    WIPE_SHRINK    = auto()

#-------------------------------------------------------------------------------
# 移動マネージャークラス
#-------------------------------------------------------------------------------
class SrfFadeBattle:

    __pygame     = None
    __screen     = None
    __screen_w   = None
    __screen_h   = None
    __offset_x   = None
    __offset_y   = None
    __image      = None
    __image_w    = None
    __image_h    = None
    __state      = None
    __list       = None
    __pos_list   = []
    __dir_list   = []
    __dest       = None
    __is_spread  = None

    #-------------------------------------------------------------------------------
    # コンストラクタ
    #-------------------------------------------------------------------------------
    def __init__( self, pygame, screen, state ):

        self.__pygame   = pygame
        self.__screen   = screen

        # 画像ファイルを読み込み
        self.__image = self.__pygame.image.load( "image/black_64.bmp" ).convert()
        block_w      = self.__image.get_width()
        block_h      = self.__image.get_height()

        w = -( -self.__screen.get_width() // 2 )
        h = -( -self.__screen.get_height() // 2 )
        screen_w = -( -w // block_w ) * 2
        screen_h = -( -h // block_h ) * 2

        # エフェクト範囲を正方形にする
        # アスペクト比の差は描画時に補正する
        if screen_w < screen_h:
            screen_w = screen_h
            offset_x = h - w
            offset_y = 0
        else:
            screen_h = screen_w
            offset_y = w - h
            offset_x = 0

        self.__state = state
        self.__screen_w = screen_w
        self.__screen_h = screen_h
        self.__block_w  = block_w
        self.__block_h  = block_h
        self.__offset_x = offset_x
        self.__offset_y = offset_y

        # データ生成
        self.__setup()

        return

    #-------------------------------------------------------------------------------
    # データ生成
    #-------------------------------------------------------------------------------
    def __setup( self ):

        state = self.__state
        if EnumFadeStatus.FILL_COMPLETLY == state:
            self.__is_spread = True
            self.__dest      = True
            init             = self.__dest
        elif EnumFadeStatus.FILL_SPREAD == state:
            self.__is_spread = True
            self.__dest      = True
            init             = not self.__dest
        elif EnumFadeStatus.FILL_SHRINK == state:
            self.__is_spread = False
            self.__dest      = False
            init             = not self.__dest
        elif EnumFadeStatus.WIPE_COMPLETLY == state:
            self.__is_spread = False
            self.__dest      = False
            init             = self.__dest
        elif EnumFadeStatus.WIPE_SPREAD == state:
            self.__is_spread = True
            self.__dest      = False
            init             = not self.__dest
        elif EnumFadeStatus.WIPE_SHRINK == state:
            self.__is_spread = False
            self.__dest      = True
            init             = not self.__dest

        # 開始位置リスト
        if True == self.__is_spread:
            self.__pos_list.append(( self.__screen_w // 2 - 1, self.__screen_h // 2 + 0 ))
            self.__pos_list.append(( self.__screen_w // 2 + 0, self.__screen_h // 2 - 1 ))
            self.__pos_list.append(( self.__screen_w // 2 + 0, self.__screen_h // 2 + 0 ))
            self.__pos_list.append(( self.__screen_w // 2 - 1, self.__screen_h // 2 - 1 ))
        else:
            self.__pos_list.append(( 0,0 ))
            self.__pos_list.append(( self.__screen_w - 1,self.__screen_h - 1 ))
            self.__pos_list.append(( 0,self.__screen_h - 1 ))
            self.__pos_list.append(( self.__screen_w - 1,0 ))

        # 進行方向リスト
        self.__dir_list.append(( 0,1 ))
        self.__dir_list.append(( 0,-1 ))
        self.__dir_list.append(( 1,0 ))
        self.__dir_list.append(( -1,0 ))

        # マップを初期化
        self.__list = [[ init for i in range( self.__screen_w )] for j in range( self.__screen_h )]

        return

    #-------------------------------------------------------------------------------
    # アニメーションを進める
    #-------------------------------------------------------------------------------
    def make_progress( self ):
        cnt = len( self.__pos_list )
        for i in range( cnt, 0, -1 ):
            index = i - 1
            pos = self.__pos_list[ index ]
            dir = self.__dir_list[ index ]
            self.__list[ pos[ 1 ] ][ pos[ 0 ] ] = self.__dest

            ret, dir = self.__is_finished( pos, dir )
            if True == ret:
                self.__pos_list.pop( index )
                self.__dir_list.pop( index )
            else:
                self.__dir_list[ index ] = dir
                self.__pos_list[ index ] = ( pos[ 0 ] + dir[ 0 ], pos[ 1 ] + dir[ 1 ] )

    #-------------------------------------------------------------------------------
    # 侵入可能な方向があるか
    #
    # 進行方向を変えながら侵入できる方向を探す
    # 4方向（上下左右）をチェックして、
    # いずれも侵入不可であれば探索を終了
    #-------------------------------------------------------------------------------
    def __is_finished( self, pos, dir ):
        if True == self.__is_spread:
            ret, dir = self.__is_finished_spread( pos, dir )
            return ret, dir
        else:
            ret, dir = self.__is_finished_shrink( pos, dir )
            return ret, dir

    #-------------------------------------------------------------------------------
    # 拡散用
    #-------------------------------------------------------------------------------
    def __is_finished_spread( self, pos, cur ):

        nxt = self.__change_dir( cur )
        if True == self.__can_move( pos, nxt ):
            return False, nxt
        else:
            if True == self.__can_move( pos, cur ):
                return False, cur
            else:
                return True, nxt

    #-------------------------------------------------------------------------------
    # 収縮用
    #-------------------------------------------------------------------------------
    def __is_finished_shrink( self, pos, dir ):
        if True == self.__can_move( pos, dir ):
            return False, dir
        else:
            dir = self.__change_dir( dir )
            if True == self.__can_move( pos, dir ):
                return False, dir
            else:
                dir = self.__change_dir( dir )
                if True == self.__can_move( pos, dir ):
                    return False, dir
                else:
                    dir = self.__change_dir( dir )
                    if True == self.__can_move( pos, dir ):
                        return False, dir
                    else:
                        return True, dir

    #-------------------------------------------------------------------------------
    # 侵入チェック
    #
    # 現在値に進行方向を加えた座標がマップの範囲外、
    # または目標値に変更済みのブロックであればFalseをリターン
    #-------------------------------------------------------------------------------
    def __can_move( self, pos, dir ):

        x = pos[ 0 ] + dir[ 0 ]
        y = pos[ 1 ] + dir[ 1 ]

        if x < 0 or self.__screen_w <= x:
            return False

        if y < 0 or self.__screen_h <= y:
            return False

        if self.__list[ y ][ x ] == self.__dest:
            return False

        return True

    #-------------------------------------------------------------------------------
    # 方向転換
    #
    # dirで指定された進行方向を90度回転する（反計回り）
    # (1) 右 → 上
    # (2) 上 → 左
    # (3) 左 → 下
    # (4) 下 → 右
    #-------------------------------------------------------------------------------
    def __change_dir( self, dir ):

        if dir[ 0 ] == 1 and dir[ 1 ] == 0:
            x = 0
            y = -1
        elif dir[ 0 ] == 0 and dir[ 1 ] == -1:
            x = -1
            y = 0
        elif dir[ 0 ] == -1 and dir[ 1 ] == 0:
            x = 0
            y = 1
        elif dir[ 0 ] == 0 and dir[ 1 ] == 1:
            x = 1
            y = 0

        return ( x, y )

    #-------------------------------------------------------------------------------
    # 描画
    #-------------------------------------------------------------------------------
    def draw( self ):
        for y in range( self.__screen_h ):
            for x in range( self.__screen_w ):
                if True == self.__list[ y ][ x ]:
                    pos_x = x * self.__block_w - self.__offset_x
                    pos_y = y * self.__block_h - self.__offset_y
                    self.__screen.blit( self.__image, ( pos_x, pos_y ))




