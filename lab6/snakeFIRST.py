import random

from uib_inf100_graphics.event_app import run_app
from snake_viewFIRST import draw_board

def app_started(app):
    """ Modellen.
    Denne funksjonen kalles én gang ved programmets oppstart.
    Her skal vi __opprette__ variabler i som behøves i app."""
    app.state = 'active'
    app.debug_mode = False
    app.timer_delay = 50
    app.direction = 'east'
    app.head_pos, app.board = create_board(15, 19)      #Kan endre på antall rows og cols, men kan gå utover spillets performance
    app.snake_size = 3
    app.score_count = 0

def timer_fired(app):
    """En kontroller.
    Denne funksjonen kalles ca 10 ganger per sekund som standard.
    Funksjonen kan __endre på__ eksisterende variabler i app."""
    if not app.debug_mode and app.state =='active':
        move_snake(app)

def move_snake(app):
    app.head_pos = get_next_head_position(app.head_pos, app.direction)
    row, col = app.head_pos
    if not is_legal_move(app.head_pos, app.board):
        app.state = 'gameover'
        return
    else:
        if app.board[row][col] == -1:
            app.snake_size +=1
            app.score_count +=1
            add_apple_at_random_location(app.board)
        else:
            subtract_one_from_all_positives(app.board)

        app.board[row][col] = app.snake_size



def get_next_head_position(head_pos, direction):
    row, col = head_pos
    if direction == 'east':
        col +=1
    elif direction == 'west':
        col -=1
    elif direction == 'north':
        row -=1
    elif direction == 'south':
        row +=1
    next_head_pos = (row, col)
    return next_head_pos

def subtract_one_from_all_positives(grid):
    rows = len(grid)
    cols = len(grid[0])

    for row in range(rows):
        for col in range(cols):
            if grid[row][col] > 0:
                grid[row][col] -= 1

def add_apple_at_random_location(grid):
    possible_apple = []
    rows = len(grid)
    cols = len(grid[0])

    for row in range(rows):
        for col in range(cols):
            if grid[row][col] == 0:
                possible_apple.append((row, col))  # Lagre (row, col) som mulige posisjoner for eplet

    if possible_apple:  # Sjekk om det er noen tomme plasser
        random_row, random_col = random.choice(possible_apple)  # Velg en tilfeldig tom plass
        grid[random_row][random_col] = -1  # Legg til eplet på den tilfeldige plassen

def is_legal_move(pos, board):
    row_pos, col_pos = pos
    row_max = len(board)
    col_max = len(board[0])

    if 0 <= row_pos < row_max:
        if 0 <= col_pos < col_max:
            if board[row_pos][col_pos] <= 0:
                return True
    return False

def create_board(rows, cols):
    board = []
    for row in range(rows):
        r = [0]*cols
        board.append(r)

    board[rows//2][cols//2] = 1
    head_pos = (rows//2, cols//2)
    add_apple_at_random_location(board)
    return head_pos, board



def key_pressed(app, event):
    """ En kontroller.
    Denne funksjonen kalles hver gang brukeren trykker på tastaturet.
    Funksjonen kan __endre på__ eksisterende variabler i app."""
    if event.key == 'd':
        app.debug_mode = not app.debug_mode
    if app.state == 'active':
        if event.key == 'Up' and app.direction != 'south':      #Må ha at tidlgere direction ikke kan være det motsatte fordi ellers å blir det game over hvis man trykker motsatte knappen
            app.direction = 'north'
        elif event.key == 'Down' and app.direction != 'north':
            app.direction = 'south'
        elif event.key == 'Left' and app.direction != 'east':
            app.direction = 'west'
        elif event.key == 'Right' and app.direction != 'west':
            app.direction = 'east'
        elif event.key == 'Space':
            move_snake(app)
    elif app.state == 'gameover':
        return

def redraw_all(app, canvas):
    """ Visningen.
    Denne funksjonen tegner vinduet. Funksjonen kalles hver gang
     modellen har endret seg, eller vinduet har forandret størrelse.
     Funksjonen kan __lese__ variabler fra app, men har ikke lov til
     å endre på dem."""
    if app.debug_mode:
        canvas.create_text(app.width/2, 10, text=f'{app.state=} {app.head_pos=} {app.snake_size=} {app.direction=}')
    if app.state == 'active':
        draw_board(canvas,
                   25,
                   25,
                   app.width-25,
                   app.height-25,
                   app.board,
                   app.debug_mode
                   )
        if not app.debug_mode:
            canvas.create_text(app.width / 2, 10,
                              text=f'score = {app.score_count}')
    elif app.state == 'gameover':
        canvas.create_text(app.width / 2, app.height/2, text=f'Game Over', font='Arial 60')
        canvas.create_text(app.width / 2, (app.height / 2)+50, text=f'Score = {app.score_count}', font='Arial 30')
run_app(width=600, height=500, title="Snake")
