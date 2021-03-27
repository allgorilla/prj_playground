# coding: utf-8
from pygame.locals import *
import pygame
from enum import Enum, auto

#-------------------------------------------------------------------------------
# シーン列挙型
#-------------------------------------------------------------------------------
class EnumFadeStatus( Enum ):

    FILL_COMPLETELY = auto()
    FILL_SPREAD     = auto()
    FILL_SHRINK     = auto()
    WIPE_COMPLETELY = auto()
    WIPE_SPREAD     = auto()
    WIPE_SHRINK     = auto()

#-------------------------------------------------------------------------------
# 移動マネージャークラス
#-------------------------------------------------------------------------------
class SrfFadeBattle:

    __pygame     = None
    __screen     = None
    __scr_wh     = None
    __ofs_x      = None
    __ofs_y      = None
    __image      = None
    __image_w    = None
    __image_h    = None
    __state      = None
    __list       = None
    __pos_list   = []
    __dir_list   = []
    __dest       = None
    __is_spread  = None
    __is_enable  = None

    #-------------------------------------------------------------------------------
    # コンストラクタ
    #-------------------------------------------------------------------------------
    def __init__( self, pygame, screen ):

        self.__pygame   = pygame
        self.__screen   = screen

        # 画像ファイルを読み込み
        self.__image = self.__pygame.image.load( "image/black_64.bmp" ).convert()
        blk_w        = self.__image.get_width()
        blk_h        = self.__image.get_height()

        w = -( -self.__screen.get_width() // 2 )
        h = -( -self.__screen.get_height() // 2 )
        scr_w = -( -w // blk_w ) * 2
        scr_h = -( -h // blk_h ) * 2

        # エフェクト範囲を正方形にする
        # アスペクト比の差は描画時に補正する
        if scr_w < scr_h:
            self.__scr_wh = scr_h
            ofs_x = h - w
            ofs_y = 0
        else:
            self.__scr_wh = scr_w
            ofs_y = w - h
            ofs_x = 0

        self.__blk_w     = blk_w
        self.__blk_h     = blk_h
        self.__ofs_x     = ofs_x
        self.__ofs_y     = ofs_y
        self.__is_enable = False

        return

    #-------------------------------------------------------------------------------
    # データ生成
    #-------------------------------------------------------------------------------
    def __setup( self ):

        state = self.__state
        if EnumFadeStatus.FILL_COMPLETELY == state:
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
        elif EnumFadeStatus.WIPE_COMPLETELY == state:
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
            wh = ( self.__scr_wh // 2 )
            self.__pos_list.append(( wh - 1, wh + 0 ))
            self.__pos_list.append(( wh + 0, wh - 1 ))
            self.__pos_list.append(( wh + 0, wh + 0 ))
            self.__pos_list.append(( wh - 1, wh - 1 ))
        else:
            wh = self.__scr_wh
            self.__pos_list.append(( 0,      0      ))
            self.__pos_list.append(( wh - 1, wh - 1 ))
            self.__pos_list.append(( 0,      wh - 1 ))
            self.__pos_list.append(( wh - 1, 0      ))

        # 進行方向リスト
        self.__dir_list.append((  0, 1 ))
        self.__dir_list.append((  0,-1 ))
        self.__dir_list.append((  1, 0 ))
        self.__dir_list.append(( -1, 0 ))

        # マップを初期化
        self.__list = [[ init for i in range( self.__scr_wh )] for j in range( self.__scr_wh )]

        return

    #-------------------------------------------------------------------------------
    # アニメーションを進める
    #-------------------------------------------------------------------------------
    def make_progress( self ):

        if False == self.__is_enable:
            return

        cnt = len( self.__pos_list )
        for i in range( cnt, 0, -1 ):
            idx = i - 1
            pos = self.__pos_list[ idx ]
            dir = self.__dir_list[ idx ]
            self.__list[ pos[ 1 ] ][ pos[ 0 ] ] = self.__dest

            ret, dir = self.__is_finished( pos, dir )
            if True == ret:
                self.__pos_list.pop( idx )
                self.__dir_list.pop( idx )

                if 0 == len( self.__pos_list ):

                    if EnumFadeStatus.FILL_SPREAD == self.__state:
                        self.__state = EnumFadeStatus.FILL_COMPLETELY

                    elif EnumFadeStatus.WIPE_SHRINK == self.__state:
                        self.__state = EnumFadeStatus.FILL_COMPLETELY

                    elif EnumFadeStatus.FILL_SHRINK == self.__state:
                        self.__state = EnumFadeStatus.WIPE_COMPLETELY

                    elif EnumFadeStatus.WIPE_SPREAD == self.__state:
                        self.__state = EnumFadeStatus.WIPE_COMPLETELY
                    else:
                        pass

            else:
                self.__dir_list[ idx ] = dir
                self.__pos_list[ idx ] = ( pos[ 0 ] + dir[ 0 ], pos[ 1 ] + dir[ 1 ] )

        return

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

        if x < 0 or self.__scr_wh <= x:
            return False

        if y < 0 or self.__scr_wh <= y:
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

        if False == self.__is_enable:
            return

        for y in range( self.__scr_wh ):
            for x in range( self.__scr_wh ):
                if True == self.__list[ y ][ x ]:
                    pos_x = x * self.__blk_w - self.__ofs_x
                    pos_y = y * self.__blk_h - self.__ofs_y
                    self.__screen.blit( self.__image, ( pos_x, pos_y ))
        return

    #-------------------------------------------------------------------------------
    # フェード開始
    #-------------------------------------------------------------------------------
    def begin( self, state ):

        self.__state     = state
        self.__is_enable = True

        # データ生成
        self.__setup()

    #-------------------------------------------------------------------------------
    # フェード終了
    #-------------------------------------------------------------------------------
    def end( self ):

        self.__is_enable = False

    #-------------------------------------------------------------------------------
    # 状態取得
    #-------------------------------------------------------------------------------
    def get_state( self ):

        return self.__state
