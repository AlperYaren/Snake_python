from uib_inf100_graphics.simple import canvas, display
from snake_viewFIRST import draw_board

test_boards = [
    [
        [0,-1, 0],
        [1, 2, 0]
    ],
    [
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 9,10,11, 0,-1, 0],
        [0, 0, 0, 8, 0, 0, 0, 0, 0],
        [0, 0, 0, 7, 6, 5, 0, 0, 0],
        [0, 0, 0, 0, 0, 4, 0, 0, 0],
        [0, 0, 0, 1, 2, 3, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
    ]
]

debug_mode = True

while True:
    for test_board in test_boards:
        draw_board(canvas, 25, 25, 375, 375, test_board, debug_mode)
        display(canvas, min_duration_sec=2)
    debug_mode = not debug_mode
