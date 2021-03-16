# coding: utf-8

#-------------------------------------------------------------------------------
# 移動マネージャークラス
#-------------------------------------------------------------------------------
class StsMove:

    destination = 0
    progress    = 0
    direction   = ( 0, 0 )
    block_w     = 0
    block_h     = 0

    #-------------------------------------------------------------------------------
    # 目標値を設定
    #-------------------------------------------------------------------------------
    def set_destination( self, destination ):
        self.destination = destination
        return
    #-------------------------------------------------------------------------------
    # ブロックのサイズを設定
    #-------------------------------------------------------------------------------
    def set_block_size( self, width, height ):
        self.block_w = width
        self.block_h = height
        return
    #-------------------------------------------------------------------------------
    # 方向を設定
    #-------------------------------------------------------------------------------
    def set_direction( self, x, y ):
        self.direction = ( x, y )
        return
    #-------------------------------------------------------------------------------
    # 進捗値を更新
    #-------------------------------------------------------------------------------
    def make_progress(self):
        self.progress += 1
        if self.progress >= self.destination:
            self.direction = ( 0, 0 )
            self.progress  = 0
        return
    #-------------------------------------------------------------------------------
    # 移動量のオフセット値を取得する
    #-------------------------------------------------------------------------------
    def get_move_offset(self):
        ratio = 1 - float( self.progress / self.destination )
        x = 0
        y = 0
        if self.direction == ( 0, -1 ):
            y -= int( float( self.block_h ) * ratio )
        elif self.direction == ( 0, +1 ):
            y += int( float( self.block_h ) * ratio )
        elif self.direction == ( -1, 0 ):
            x -= int( float( self.block_w ) * ratio )
        elif self.direction == ( +1, 0 ):
            x += int( float( self.block_w ) * ratio )
        return x, y
    #-------------------------------------------------------------------------------
    # 移動量のオフセット値を取得する
    #-------------------------------------------------------------------------------
    def get_direction(self):
        return self.direction


