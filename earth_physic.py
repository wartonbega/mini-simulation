

import random
import block_ids as id
import water_physic

def erosion(n):
    north = n[0][1]
    south = n[2][1]
    east = n[1][2]
    ouest = n[1][0]

    faces = []

    if id.WATER_ID in [north, south, east, ouest]:
        if random.randint(0,1000) == 50:
            return True
    
    return False
    