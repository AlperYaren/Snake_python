from uib_inf100_graphics.helpers import load_image, image_in_box

def draw_board(canvas, x1, y1, x2, y2, board, debug_mode):
    rows = len(board)
    cols = len(board[0])
    switch = True

    cell_width = (x2 - x1) / cols
    cell_height = (y2 - y1) / rows

    image = load_image('apple.png')

    for row in range(rows):
        for col in range(cols):
            switch = not switch
            cell_left = x1 + col * cell_width
            cell_top = y1 + row * cell_height
            cell_right = cell_left + cell_width
            cell_bottom = cell_top + cell_height
            color = get_color(board[row][col], switch)
            if color == 'red':
                color = get_color(0,switch)
                canvas.create_rectangle(
                    cell_left, cell_top, cell_right, cell_bottom,
                    fill=color, outline=""
                )
                image_in_box(canvas, cell_left, cell_top, cell_right, cell_bottom, image)
            else:
                canvas.create_rectangle(
                    cell_left, cell_top, cell_right, cell_bottom,
                    fill=color, outline=""
                )
            if debug_mode:
                canvas.create_text(
                    (cell_right+cell_left)/2,
                    (cell_bottom+cell_top)/2,
                    text= f'{row},{col}\n{board[row][col]}'
                )



def get_color(value, switch):
    if value > 0:
        color = 'orange'
    elif value < 0:
        color = 'red'
    elif value == 0:
        if switch:
            color = 'green'
        else:
            color = 'lightgreen'
    return color






