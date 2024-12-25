# view smb.json in TheVGLC
SOLIDS = set()
SOLIDS.add('X')
SOLIDS.add('S')
SOLIDS.add('?')
SOLIDS.add('Q')
SOLIDS.add('<')
SOLIDS.add('>')
SOLIDS.add('[')
SOLIDS.add(']')
SOLIDS.add('B')
SOLIDS.add('b')

ENEMIES = set()
ENEMIES.add('E')
ENEMIES.add('B')
ENEMIES.add('b')

# modified from past work by seth cooper
JUMPS = [
    [
        [0,-1],
        [0,-2],
        [0,-3],
        [1,-3],
        [1,-4]
    ],
    [
        [0,-1],
        [0,-2],
        [0,-3],
        [0,-4],
        [1,-4]
    ],
    [
        [0,-1],
        [1,-1],
        [1,-2],
        [1,-3],
        [1,-4],
        [2,-4]
    ],
    [
        [0,-1],
        [1,-1],
        [1,-2],
        [2,-2],
        [2,-3],
        [3,-3],
        [3,-4],
        [4,-4],
        [5,-4],
        [5,-3],
        [6,-3],
        [7,-3],
        [7,-2],
        [8,-2],
        [8,-1]
    ],
    [
        [0,-1],
        [1,-1],
        [1,-2],
        [2,-2],
        [2,-3],
        [3,-3],
        [3,-4],
        [4,-4],
        [5,-4],
        [6,-4],
        [6,-3],
        [7,-3],
        [7,-2],
        [8,-2],
        [8,-1]
    ]
]