import block_ids as id


def check_neighbour(n):
    north = n[0][1]
    south = n[2][1]
    east = n[1][2]
    ouest = n[1][0]

    faces = []

    if north == id.NOTHING_ID:
        faces.append("N")

    if south == id.NOTHING_ID:
        faces.append("S")
    
    if east == id.NOTHING_ID:
        faces.append("E")

    if ouest == id.NOTHING_ID:
        faces.append("O")

    return faces

def is_type_water(t):
    if t == id.WATER_ID or t == id.STATIC_WATER_ID:
        return True
    return False