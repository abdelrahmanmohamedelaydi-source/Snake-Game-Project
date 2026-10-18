# import necessary modules for the game
import curses
import random

# Initialize the curses library to create our screen
screen = curses.initscr()

# hide the mouse cursor
curses.curs_set(0)

# getmax screen height and width
screen_height, screen_width = screen.getmaxyx()

# create a new window
window = curses.newwin(screen_height, screen_width, 0, 0)

# allow window to receive input from the keyboard
window.keypad(1)

# set the delay for updating the screen
window.timeout(100)

# set initial coordinates (y, x) -> y is height, x is width
snk_y = int(screen_height / 2)
snk_x = int(screen_width / 4)

# define the initial position of the snake body (y, x)
snake = [[snk_y, snk_x], [snk_y, snk_x - 1], [snk_y, snk_x - 2]]

# create the food in the middle of window (y, x)
food = [int(screen_height / 2), int(screen_width / 2)]

# add the food to screen
window.addch(food[0], food[1], curses.ACS_PI)

# set initial movement direction to right
key = curses.KEY_RIGHT

# create game loop
while True:
    next_key = window.getch()
    key = key if next_key == -1 else next_key

    # 1. check if snake collided with walls or itself
    head = snake[0]
    if (
        head[0] <= 0
        or head[0] >= screen_height - 1
        or head[1] <= 0
        or head[1] >= screen_width - 1
        or head in snake[1:]
    ):
        break  # exit loop safely

    # 2. calculate new head position (y, x)
    new_head = [snake[0][0], snake[0][1]]

    if key == curses.KEY_DOWN:
        new_head[0] += 1
    elif key == curses.KEY_UP:
        new_head[0] -= 1
    elif key == curses.KEY_RIGHT:
        new_head[1] += 1
    elif key == curses.KEY_LEFT:
        new_head[1] -= 1

    # insert the new head to snake
    snake.insert(0, new_head)

    # 3. check if snake ate the food
    if snake[0] == food:
        food = None
        while food is None:
            new_food = [
                random.randint(1, screen_height - 2),
                random.randint(1, screen_width - 2),
            ]
            food = new_food if new_food not in snake else None
        window.addch(food[0], food[1], curses.ACS_PI)
    else:
        tail = snake.pop()
        window.addch(tail[0], tail[1], " ")

    # update position of the snake head on screen
    window.addch(snake[0][0], snake[0][1], curses.ACS_CKBOARD)

# Clean up screen when game ends
curses.endwin()
print("Game Over!")
