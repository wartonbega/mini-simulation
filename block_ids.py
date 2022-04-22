

from mmap import MADV_WILLNEED
from tkinter.tix import MAX


count = 0

def iota():
    global count
    count += 1
    return count - 1


NOTHING_ID  = iota()
WATER_ID    = iota()
EARTH_ID    = iota()
GRASS_ID    = iota()
SAND_ID     = iota()
STONE_ID    = iota()

_STATIC_MIDDLE = iota()

STATIC_WATER_ID    = iota()
STATIC_EARTH_ID    = iota()
STATIC_GRASS_ID    = iota()
STATIC_SAND_ID     = iota()
STATIC_STONE_ID    = iota()


MAX_ID = iota()



def static_block(block):
    if block > _STATIC_MIDDLE:
        return block
    return (block+_STATIC_MIDDLE)%MAX_ID

def is_static(block):
    if block > _STATIC_MIDDLE:
        return True
    return False

def unstatic_block(block):
    if block < _STATIC_MIDDLE:
        return block
    return (block-_STATIC_MIDDLE)%MAX_ID
