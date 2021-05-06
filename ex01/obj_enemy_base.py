# coding: utf-8
from pygame.locals import *
import pygame

import obj_base

#-------------------------------------------------------------------------------
# 移動マネージャークラス
#-------------------------------------------------------------------------------
class ObjectEnemyBase( obj_base.ObjectBase ):

    #-------------------------------------------------------------------------------
    # プレイヤーを描画
    #-------------------------------------------------------------------------------
    def test( self, x ):

        # 左右反転
        if self.dir_x == -1  and x == 1:
            self.dir_x = x
        elif self.dir_x == 1 and x == -1:
            self.dir_x = x

        self.fcur += 1
        if  self.fmax <= self.fcur:
            self.img_list.append( self.img_lr )
            self.img_lr = self.img_list.pop( 0 )
            self.fcur = 0

    #-------------------------------------------------------------------------------
    # 接触を検知する
    #-------------------------------------------------------------------------------
    def find_contact_trigger( self, objerct_list ):

        list = []
        for i in range( 4 ):
            object = objerct_list[ i ]
            if self.loc_pos == object.loc_pos:
                list.append( i )

        if 0 != len( list ):
            if self.contact_triger == False:
                self.contact_triger = True
                print( list, "が敵に接触しました", self.loc_pos )
                return True
            else:
                return False
        self.contact_triger = False
        return False
