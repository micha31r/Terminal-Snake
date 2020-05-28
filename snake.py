# Snake game

import curses, random, time, sys

SCREEN = curses.initscr()

# Returning special values
SCREEN.keypad(True)

# Clear SCREEN
SCREEN.clear()

# Keypress timeout
SCREEN.timeout(120)

HEIGHT, WIDTH = SCREEN.getmaxyx()

# No echo keys
curses.noecho()

# No pressing enter
curses.cbreak()

# Start color
curses.start_color()

# Grey
curses.init_pair(1, 120, curses.COLOR_BLACK)

class Game:

    def __init__(self):
        self.snake = Snake()
        self.food = Food()

    def score(self):
        SCREEN.addstr(0, 2, f"SCORE: {str(self.snake.length)}", curses.color_pair(1))

    def update(self):
        # Update snake movement
        self.snake.update()

        # Spawn new food if snake ate it
        eat = self.snake.eat(self.food.y, self.food.x)
        if eat:
            self.food = eat

        # Collision with body and border
        if self.snake.hit_body() or self.snake.hit_border():
            global running
            running = False

    def render(self):
        self.snake.render()
        self.food.render()
        self.score()

class Snake:

    def __init__(self):
        self.y = int(HEIGHT/2)
        self.x = int(WIDTH/2)
        self.direction = 0 # 0=up 1=down 2=right 3=left
        self.tail = []
        self.length = 0
    
    def control(self):
        key_p = SCREEN.getch()
        if key_p == ord('w'):
            if self.direction != 1:
                self.direction = 0
        elif key_p == ord('a'):
            if self.direction != 2:
                self.direction = 3
        elif key_p == ord('s'):
            if self.direction != 0:
                self.direction = 1
        elif key_p == ord('d'):
            if self.direction != 3:
                self.direction = 2

    def add_body(self):
        self.tail.append([self.y, self.x])

    def shift(self):
        self.add_body()
        self.tail.pop(0)

    def eat(self,foody,foodx):
        if self.y == foody and self.x == foodx:
            self.add_body()
            self.length += 1
            return Food() # Generate new food

    def hit_body(self):
        if [self.y, self.x] in self.tail[:-1]:
            return True

    def hit_border(self):
        if (self.y > HEIGHT-2 or self.y < 2) or (self.x > WIDTH-2 or self.x < 2):
            return True

    def update(self):
        self.control()

        # Move body
        self.shift()

        # Move head
        if self.direction == 0:
            self.y -= 1
        elif self.direction == 1:
            self.y += 1
        elif self.direction == 2:
            self.x += 1
        elif self.direction == 3:
            self.x -= 1

    def render(self):
        color = curses.color_pair(1)
        # Render head
        SCREEN.addstr(self.y, self.x, "@", color)
        # Render tail
        for body in self.tail:
            SCREEN.addstr(body[0], body[1], "o", color)

class Food:

    def __init__(self):
        self.y = random.randint(2,HEIGHT-2)
        self.x = random.randint(2,WIDTH-2)

    def render(self):
        SCREEN.addstr(self.y, self.x, "c", curses.color_pair(1))

game = Game()

# Loop
running = True
while running:
    game.update()
    SCREEN.refresh()
    SCREEN.erase()
    SCREEN.border(0)
    game.render()

# End Program
curses.endwin()

print(f"Game Score: {game.snake.length}")
sys.exit()
