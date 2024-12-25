'''
modified directly from:
    1. https://github.com/TheVGLC/TheVGLC/blob/master/PlatformerPathfinding/pathfinding.py
    2. https://github.com/TheVGLC/TheVGLC/blob/master/PlatformerPathfinding/test_level.py
'''

from heapq import heappush, heappop
from config import JUMPS, SOLIDS

DEBUG_DISPLAY = False

def isSolid(tile):
    return tile in SOLIDS

def makeGetNeighbors(jumps,levelStr,visited,isSolid):
    maxX = len(levelStr[0])-1
    maxY = len(levelStr)-1
    jumpDiffs = []
    for jump in jumps:
        jumpDiff = [jump[0]]
        for ii in range(1,len(jump)):
            jumpDiff.append((jump[ii][0]-jump[ii-1][0],jump[ii][1]-jump[ii-1][1]))
        jumpDiffs.append(jumpDiff)
    jumps = jumpDiffs

    def getNeighbors(pos):
        dist = pos[0]-pos[2]
        pos = pos[1]
        visited.add((pos[0],pos[1]))
        below = (pos[0],pos[1]+1)
        neighbors = []
        if below[1] > maxY:
            return []
        if pos[2] != -1:
            ii = pos[3] +1
            jump = pos[2]
            if ii < len(jumps[jump]):
                if not (pos[0]+pos[4]*jumps[jump][ii][0] > maxX or pos[0]+pos[4]*jumps[jump][ii][0] < 0 or pos[1]+jumps[jump][ii][1] < 0) and not isSolid(levelStr[pos[1]+jumps[jump][ii][1]][pos[0]+pos[4]*jumps[jump][ii][0]]):
                    neighbors.append([dist+1,(pos[0]+pos[4]*jumps[jump][ii][0],pos[1]+jumps[jump][ii][1],jump,ii,pos[4])])
                if pos[1]+jumps[jump][ii][1] < 0 and not isSolid(levelStr[pos[1]+jumps[jump][ii][1]][pos[0]+pos[4]*jumps[jump][ii][0]]):
                    neighbors.append([dist+1,(pos[0]+pos[4]*jumps[jump][ii][0],0,jump,ii,pos[4])])

        if isSolid(levelStr[below[1]][below[0]]):
            if pos[0]+1 <= maxX and not isSolid(levelStr[pos[1]][pos[0]+1]):
                neighbors.append([dist+1,(pos[0]+1,pos[1],-1)])
            if pos[0]-1 >= 0 and not isSolid(levelStr[pos[1]][pos[0]-1]):
                neighbors.append([dist+1,(pos[0]-1,pos[1],-1)])

            for jump in range(len(jumps)):
                ii = 0
                if not (pos[0]+jumps[jump][ii][0] > maxX or pos[1] < 0) and not isSolid(levelStr[pos[1]+jumps[jump][ii][1]][pos[0]+jumps[jump][ii][0]]):
                    neighbors.append([dist+ii+1,(pos[0]+jumps[jump][ii][0],pos[1]+jumps[jump][ii][1],jump,ii,1)])

                if not (pos[0]-jumps[jump][ii][0] < 0 or pos[1] < 0) and not isSolid(levelStr[pos[1]+jumps[jump][ii][1]][pos[0]-jumps[jump][ii][0]]):
                    neighbors.append([dist+ii+1,(pos[0]-jumps[jump][ii][0],pos[1]+jumps[jump][ii][1],jump,ii,-1)])

        else:
            neighbors.append([dist+1,(pos[0],pos[1]+1,-1)])
            if pos[1]+1 <= maxY:
                if pos[0] + 1 < maxX and not isSolid(levelStr[pos[1]+1][pos[0]+1]):
                    neighbors.append([dist+1.4,(pos[0]+1,pos[1]+1,-1)])
                if pos[0] - 1 >= 0 and not isSolid(levelStr[pos[1]+1][pos[0]-1]):
                    neighbors.append([dist+1.4,(pos[0]-1,pos[1]+1,-1)])

            if pos[1]+2 <= maxY:
                if pos[0] + 1 < maxX and not isSolid(levelStr[pos[1]+2][pos[0]+1]):
                    neighbors.append([dist+2,(pos[0]+1,pos[1]+2,-1)])
                if pos[0] - 1 >= 0 and not isSolid(levelStr[pos[1]+2][pos[0]-1]):
                    neighbors.append([dist+2,(pos[0]-1,pos[1]+2,-1)])
        return neighbors
    return getNeighbors

def get_percent_completable(src, levelStr):
    visited = set()
    getNeighbors = makeGetNeighbors(JUMPS,levelStr,visited,isSolid)
    maxX = len(levelStr[0])-1
    heuristic = lambda pos: abs(maxX-pos[0])

    dist = {}
    prev = {}
    dist[src] = 0
    prev[src] = None
    heap = [(dist[src], src,0)]
    furthest_x = 0

    while heap:
        node = heappop(heap)

        for next_node in getNeighbors(node):
            next_node[0] += heuristic(next_node[1])
            next_node.append(heuristic(next_node[1]))
            if next_node[1] not in dist or next_node[0] < dist[next_node[1]]:
                # current_x = next_node[1][0]
                furthest_x = max(furthest_x, next_node[1][0])

                dist[next_node[1]] = next_node[0]
                prev[next_node[1]] = node[1]
                heappush(heap, next_node)

        if furthest_x == maxX:
            break

    return furthest_x / maxX

def columns_into_rows(columns):
    column_length = len(columns[0])
    rows = ["" for _ in range(column_length)]

    for col in columns:
        i = column_length - 1
        j = 0

        while i >= 0:
            rows[j] = f'{rows[j]}{col[i]}'

            i -= 1
            j += 1

    return rows

def percent_playable(columns):
    length = len('X-------------')
    columns.insert(0, 'X-------------')
    columns.insert(0, 'X-------------')
    columns.append('X-------------')
    columns.append('X-------------')

    lvl = columns_into_rows(columns)
    return get_percent_completable((1, length-2, -1), lvl)