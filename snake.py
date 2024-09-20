import random
from uib_inf100_graphics.event_app import run_app
from snake_view import draw_board, show_start_screen


def start_new_game(app):        #funksjon som startes nytt game
    app.state = 'active'
    app.direction = 'east'
    app.head_pos, app.board = create_board(15, 19)
    app.snake_size = 3
    app.score_count = 0

def show_top_score(app):        #funksjon som viser top score
    if app.score_count > app.top_score:
        app.top_score = app.score_count

def app_started(app):
    app.state = 'start'  # Start i startskjermmodus
    app.debug_mode = False      # Debug modus false
    app.timer_delay = 100
    app.direction = 'east'
    app.head_pos, app.board = create_board(15, 19)  # Initialiserer board
    app.snake_size = 3
    app.score_count = 0
    app.top_score = 0

    app.text_size = 13
    app.pulse_direction = 1  # Bruk 1 for å øke størrelsen, -1 for å redusere størrelsen



def timer_fired(app):
    """En kontroller.
    Denne funksjonen kalles ca 10 ganger per sekund som standard.
    Funksjonen kan __endre på__ eksisterende variabler i app."""
    if not app.debug_mode and app.state == 'active':
        move_snake(app)
    elif app.state == 'start':      #hvis app.state == 'start', så pulser tekst i startskjermmodus
        app.text_size += app.pulse_direction  # Oppdater tekststørrelsen
        if app.text_size <= 14 or app.text_size >= 15:
            app.pulse_direction *= -1  # Bytt retning når størrelsen når grenseverdier


def move_snake(app):
    app.head_pos = get_next_head_position(app.head_pos, app.direction)
    row, col = app.head_pos
    if not is_legal_move(app.head_pos, app.board):
        app.state = 'gameover'
        show_top_score(app)  # Oppdater toppscoren
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
    board = []                      # oppretter tom liste og lager et brett med antall rows og cols
    for row in range(rows):
        r = [0]*cols
        board.append(r)

    board[rows//2][cols//2] = 1
    head_pos = (rows//2, cols//2)           #poisjon for snake_head
    add_apple_at_random_location(board)     # Legg til eplet på den tilfeldige plassen
    return head_pos, board



def key_pressed(app, event):
    if event.key == 'd':
        app.debug_mode = not app.debug_mode
    if app.state == 'start':
        app.state = 'active'  # Endre tilstand fra startskjerm til aktivt spill når en tast trykkes
    elif app.state == 'active':
        if event.key == 'Up' and app.direction != 'south':
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
        if event.key.lower() == 'r':
            start_new_game(app)  # Start nytt spill hvis brukeren trykker "R" eller "r"






def redraw_all(app, canvas):
    if app.debug_mode:
        canvas.create_text(app.width/2, 10, text=f'{app.state=} {app.head_pos=} {app.snake_size=} {app.direction=}')

    if app.state == 'start':
        show_start_screen(canvas, app.width, app.height, app.text_size)  # Vis startskjermen

    elif app.state == 'active':
        draw_board(canvas,
                   25,
                   25,
                   app.width-25,
                   app.height-25,
                   app.board,
                   app.debug_mode
                   )
        if not app.debug_mode:
            canvas.create_text(app.width / 2, 10, text=f'Score = {app.score_count}')

    elif app.state == 'gameover':
        # Bakgrunn for Game Over-meldingen
        canvas.create_rectangle(0, 0, app.width, app.height, fill="black")
        canvas.create_text(app.width / 2, app.height/2 - 50, text=f'Game Over', font='Arial 60', fill='red')
        canvas.create_text(app.width / 2, (app.height / 2), text=f'Your Score: {app.score_count}', font='Arial 30', fill='white')
        canvas.create_text(app.width / 2, (app.height / 2) + 50, text=f'Top Score: {app.top_score}', font='Arial 30', fill='white')
        canvas.create_text(app.width / 2, (app.height / 2) + 100, text=f'Press "R" to restart', font='Arial 20', fill='white')

run_app(width=600, height=500, title="Snake")

