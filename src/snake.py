# import required modules
import turtle
import time
import random
from operator import truediv
from turtle import Turtle

delay = 0.2
score = 0
high_score = 0
width = 600
height = 600
grid_width =int((width/2)-40)
grid_height = int((height/2)-40)
bomb_num = ((grid_width*2)//40) *((grid_height*2)//40) //5
bombs = []
segments = []
can_move = True


#use final score as fitness

# death callable function
#Tell GA the location of head, tail segments, fruit, and bombs on each frame





# Creating a window screen
wn = turtle.Screen()
wn.title("Snake Game")
wn.bgcolor("blue")
wn.setup(width=width, height=height)
wn.tracer(0)


# head of the snake
head = turtle.Turtle()
head.shapesize(stretch_wid=1, stretch_len=1)
head.shape("square")
head.color("white")
head.penup()
head.goto(0, 0)
head.direction = "Stop"



pen = turtle.Turtle()
pen.speed(0)
pen.shape("square")
pen.color("white")
pen.penup()
pen.hideturtle()
pen.goto(0, (grid_height)-20)
pen.write("Score : 0  High Score : 0", align="center",
          font=("candara", 24, "bold"))



def food_spawn(snakehead,bomblist,tail):
    x = random.randint(-grid_width // 20, grid_width // 20) * 20
    y = random.randint(-grid_height // 20, grid_height // 20) * 20
    for i in range(len(bomblist)):
        if x == bomblist[i].xcor() and y == bomblist[i].ycor():
            x = x + 20
            if x >= grid_width:
                x = x - 40
        if x == snakehead.xcor() and y == snakehead.ycor():
            x = x + 20
            if x >= grid_width:
                x = x - 40
    for i in range(len(tail)):
        if x == tail[i].xcor() and y == tail[i].ycor():
            x = x + 20
            if x >= grid_width:
                x = x - 40
        if x == snakehead.xcor() and y == snakehead.ycor():
            x = x + 20
            if x >= grid_width:
                x = x - 40
    food.goto(x, y)

# food in the game
food = turtle.Turtle()
food.shapesize(stretch_wid=1, stretch_len=1)
colors = random.choice(['red'])
shapes = random.choice(['circle'])
food.speed(0)
food.shape(shapes)
food.color(colors)
food.penup()
food_spawn(head,bombs,segments)

border_size = int((grid_height*4)+(grid_width*4)+4)
border_num = int(border_size/20)

def make_border(num):
    while num != 0:
        border_i = turtle.Turtle()
        border_i.shapesize(stretch_wid=1, stretch_len=1)
        border_i.shape("square")
        border_i.color("green")
        border_i.speed(0)
        border_i.penup()
        if num >= (num/4)*3:
            border_i.goto(0, (num/4)*3)

        num -= 1







def bomb_spawn(bomb, snakehead,bomblist):
    x = random.randint(-grid_width // 20, grid_width // 20) * 20
    y = random.randint(-grid_height // 20, grid_height // 20) * 20
    for i in range(len(bomblist)):
        if x == bomblist[i].xcor() and y == bomblist[i].ycor():
            x = x + 20
            if x >= grid_width:
                x = x - 40
        if x == snakehead.xcor() and y == snakehead.ycor():
            x = x + 20
            if x >= grid_width:
                x = x - 40
    bomb.goto(x, y)
    print(bomb.xcor(),bomb.ycor())

def death():
    time.sleep(1)
    global bombs
    for i in range(len(bombs)):
        bombs[i].goto(grid_width+1000, grid_height+1000)
    head.goto(0, 0)
    bombs.clear
    global segments
    for segment in segments:
        segment.goto(grid_width+1000, grid_height+1000)
    segments.clear()


    head.direction = "stop"
    head.goto(0, 0)

    score = 0
    pen.clear()
    pen.write("Score : {} High Score : {} ".format(
        score, high_score), align="center", font=("candara", 24, "bold"))

    bomb_setup(bomb_num)
    food_spawn(head,bombs,segments)





def bomb_setup(num):
    while num != 0:
        bomb_i = turtle.Turtle()
        bomb_i.shapesize(stretch_wid=1, stretch_len=1)
        bomb_i.shape("square")
        bomb_i.color("black")
        bomb_i.speed(0)
        bomb_i.penup()
        bomb_spawn(bomb_i, head,bombs)
        bombs.append(bomb_i)
        num -= 1

bomb_setup(bomb_num)

# assigning key directions
def goup():
    global can_move
    if can_move and head.direction != "down":
        head.direction = "up"
        can_move = False


def godown():
    global can_move
    if can_move and head.direction != "up":
        head.direction = "down"
        can_move = False


def goleft():
    global can_move
    if can_move and head.direction != "right":
        head.direction = "left"
        can_move = False


def goright():
    global can_move
    if can_move and head.direction != "left":
        head.direction = "right"
        can_move = False


def move():
    global can_move
    if head.direction == "up":
        y = head.ycor()
        head.sety(y+20)

    if head.direction == "down":
        y = head.ycor()
        head.sety(y-20)

    if head.direction == "left":
        x = head.xcor()
        head.setx(x-20)

    if head.direction == "right":
        x = head.xcor()
        head.setx(x+20)
    can_move = True



wn.listen()
wn.onkeypress(goup, "w")
wn.onkeypress(godown, "s")
wn.onkeypress(goleft, "a")
wn.onkeypress(goright, "d")




# Main Gameplay
while True:

    # Logic for portal Walls
    wn.update()
    if head.xcor() > grid_width+20:
        head.goto(-grid_width-20, head.ycor())

    if head.xcor() < -grid_width-20:
        head.goto(grid_width+20, head.ycor())

    if head.ycor() > grid_height+20:
        head.goto(head.xcor(), -grid_height-20)

    if head.ycor() < -grid_height-20:
        head.goto(head.xcor(), grid_height+20)

    #logic for bombs
    for i in range(len(bombs)):
        if bombs[i].distance(head) < 20:
            death()






    if head.distance(food) < 20:
        # Adding segment
        new_segment = turtle.Turtle()
        new_segment.speed(0)
        new_segment.shape("square")
        new_segment.color("orange")  # tail colour
        new_segment.penup()
        segments.append(new_segment)
        delay -= 0.000 #could cause issues if it does reset to 0.001
        score += 10
        if score > high_score:
            high_score = score
        pen.clear()
        pen.write("Score : {} High Score : {} ".format(
            score, high_score), align="center", font=("candara", 24, "bold"))
        food_spawn(head, bombs, segments)


    # Checking for head collisions with body segments
    for index in range(len(segments)-1, 0, -1):
        x = segments[index-1].xcor()
        y = segments[index-1].ycor()
        segments[index].goto(x, y)
    if len(segments) > 0:
        x = head.xcor()
        y = head.ycor()
        segments[0].goto(x, y)
        #print(segments[0].xcor(), segments[0].ycor())
    move()
    time.sleep(delay)

    for segment in segments:
        if segment.distance(head) < 20:
            death()
    time.sleep(delay)

wn.mainloop()


