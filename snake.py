# Snake game

# Import libraries
import curses
import random
import time
import sys

screen = curses.initscr()

# Variables
###################################
HEIGHT, WIDTH = screen.getmaxyx()

###################################

# SetUps
###################################
# No echo keys
curses.noecho()

# No pressing enter
curses.cbreak()

# Returning special values
screen.keypad(True)

#clear screen
screen.clear()

# Start color
curses.start_color()
# Grey
curses.init_pair(1, 120, curses.COLOR_BLACK)

screen.timeout(100)
#################################

# Program codes
###################################

class Game:

    def __init__(self):
        self.snake = Snake()
        self.food = Food()

    def score(self):
        screen.addstr(0, 2, "SCORE: "+str(m_snake.length), curses.color_pair(1))

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

class Snake:

    def __init__(self):
        self.y = int(HEIGHT/2)
        self.x = int(WIDTH/2)
        self.direction = 0 # 0=up 1=down 2=right 3=left
        self.tail = []
        self.length = 0
    
    def control(self):
        key_p = screen.getch()
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
        self.length += 1

    def shift(self):
        for i in range(self.length-1):
            self.tail[i] = self.tail[i+1]
        self.add_body()

    def eat(self,foody,foodx):
        if self.y == foody and self.x == foodx:
            self.length += 1
            self.add_body()
            return Food() # Generate new food

    def hit_body(self):
        if [self.y, self.x] in self.tail:
            return False

    def hit_border(self):
        if (self.y > HEIGHT-1 or self.y < 1) or (self.x > WIDTH-1 or self.x < 1):
            return False

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
        screen.addstr(3,3, str(self.y)+" "+str(self.x), color)
        # screen.addstr(self.y, self.x, "@", color)
        # Render tail
        # for body in self.tail:
            # screen.addstr(body[0], body[1], "o", color)

class Food:

    def __init__(self):
        self.y = random.randint(0,HEIGHT-1)
        self.x = random.randint(0,WIDTH-1)

    def render(self):
        screen.addstr(self.y, self.x, "c", curses.color_pair(1))

game = Game()

# Loop
running = True
while running:
    try:
        screen.border(0)
        game.update()
        game.render()
        screen.refresh()
        screen.erase()
        screen.addstr(3,3,"2")
    except KeyboardInterrupt:
        break

#End Program
curses.endwin()
sys.exit()
