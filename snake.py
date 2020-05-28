# Snake game

# Import libraries
import curses
import random
import time
import sys

screen = curses.initscr()

# Variables
###################################
height, width = screen.getmaxyx()

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

def score():
    screen.addstr(0, 2, "SCORE: "+str(m_snake.length), curses.color_pair(1))

class make_snake:
    snake_pos = []
    head_y, head_x = int(height/2), int(width/2)
    direction = "right"
    length = 0
    
    def key(self):
        key_p = screen.getch()
        if key_p == ord('w'):
            if self.direction != "down":
                self.direction = "up"
        elif key_p == ord('a'):
            if self.direction != "right":
                self.direction = "left"
        elif key_p == ord('s'):
            if self.direction != "up":
                self.direction = "down"
        elif key_p == ord('d'):
            if self.direction != "left":
                self.direction = "right"

    def add_body(self):
        self.snake_pos.append([self.head_y, self.head_x])
    
    def display_snake(self):
        screen.addstr(self.head_y, self.head_x, "@", curses.color_pair(1))
        for body in make_snake.snake_pos:
            screen.addstr(body[0], body[1], "o", curses.color_pair(1))

    def move_snake(self):
        if self.direction == "up":
            self.head_y -= 1
        elif self.direction == "left":
            self.head_x -= 1
        elif self.direction == "down":
            self.head_y += 1
        elif self.direction == "right":
            self.head_x += 1

    def del_body(self):
        if len(self.snake_pos) > self.length:
            del self.snake_pos[:1]
            if len(self.snake_pos) > self.length:
                m_snake.del_body()

    def collide_with_food(self):
        try:
            if self.head_y == make_food.food_list[0][0] and self.head_x == make_food.food_list[0][1]:
                make_food.food_list = []
                self.length += 1
        except:
            pass

    def collide_with_body(self):
        if [self.head_y, self.head_x] in self.snake_pos:
            curses.endwin()
            sys.exit()

    def collide_with_border(self):
        if self.head_y >= height-1 or self.head_y <= 1:
            curses.endwin()
            sys.exit()
        if self.head_x >= width-1 or self.head_x <= 1:
            curses.endwin()
            sys.exit()


class make_food:
    food_list = []
    def spawn(self):
        self.food_list.append([random.randint(3,height-3), random.randint(3,width-3)])

    def display_food(self):
        try:
            screen.addstr(self.food_list[0][0], self.food_list[0][1], "c", curses.color_pair(1))
        except:
            pass

    def new_food(self):
        if self.food_list == []:
            m_food.spawn()

###################################
# Create snake and food
m_snake = make_snake()
m_food = make_food()

m_food.spawn()

# Loop
while True:
    try:
        screen.border(0)
        m_food.display_food()
        m_food.new_food()
        m_snake.add_body()
        m_snake.move_snake()
        m_snake.display_snake()
        m_snake.collide_with_food()
        m_snake.collide_with_body()
        m_snake.collide_with_border()
        m_snake.del_body()
        score()
        m_snake.key()
        screen.refresh()
        screen.erase()
    except KeyboardInterrupt:
        #End Program
        curses.endwin()
        sys.exit()
