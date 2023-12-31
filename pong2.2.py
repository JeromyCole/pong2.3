# Pong Remix
# Python 3 Required


import time
import turtle
import keyboard
import random
import pickle
from playsound import playsound
import os
from os import path
from tkinter import *

# Window specs & info
wn = turtle.Screen()
wn.title("Pong Remixed")
wn.bgcolor("black")
wn.setup(width=800, height=600)
wn.tracer(0)

# Scores
score_a = 0
score_b = 0

# Collision count
a_collisions = 0
b_collisions = 0

# Paddle A
paddle_a = turtle.Turtle()
paddle_a.speed(0)
paddle_a.shape("square")
paddle_a.color("red")
paddle_a.shapesize(stretch_wid=5, stretch_len=1)
paddle_a.penup()
paddle_a.goto(-350, 0)

# Paddle B
paddle_b = turtle.Turtle()
paddle_b.speed(0)
paddle_b.shape("square")
paddle_b.color("orange")
paddle_b.shapesize(stretch_wid=5, stretch_len=1)
paddle_b.penup()
paddle_b.goto(350, 0)

# Ball
ball = turtle.Turtle()
ball.speed(0)
ball.shape("circle")
ball.color("white")
ball.penup()
ball.goto(0, 0)
ball.dx = 0.45  # <--zcontrol-a1-- Ball's LEFT/RIGHT, HORIZONTAL, X AXIS speed
ball.dy = -0.35  # <--zcontrol-a2-- Ball's UP/DOWN, VERTICAL, Y AXIS speed
ball_reset_dy = .35  # <--zcontrol-a3-- (Reset) Ball's LEFT/RIGHT, HORIZONTAL, X AXIS speed
ball_reset_dx_player_a = .42  # <--zcontrol-a4-- (Reset Player A) Ball's UP/DOWN, VERTICAL, Y AXIS speed
ball_reset_dx_player_b = -.42  # <--zcontrol-a5-- (Reset Player B) Ball's UP/DOWN, VERTICAL, Y AXIS speed ***Negative so if Player score it goes toward other player's goal

# Pen
pen = turtle.Turtle()
pen.speed(0)
pen.color("white")
pen.penup()
pen.hideturtle()
pen.goto(0, 260)
pen.write("Player A : 0  Player B : 0", align="center", font=("courier", 24, "normal"))

# Center court line
center_court = turtle.Turtle()
center_court.width(2)
center_court.color("white")
center_court.hideturtle()
point1 = (0, 400)
point2 = (0, -400)
center_court.penup()
center_court.goto(point1)
center_court.pendown()
center_court.goto(point2)

# Score reset
def score_reset():
    dir_name = "/Users/GM/pycharmprojects/pong2.2"
    test = os.listdir(dir_name)
    for item in test:
        if item.endswith(".pickle"):
            os.remove(os.path.join(dir_name, item))
            time.sleep(1.1)  # Introduce a short delay
            print("Scores have been reset")

# Paddle A functions
def paddle_a_up():
    y = paddle_a.ycor()
    y += 42.8
    paddle_a.sety(y)


def paddle_a_down():
    y = paddle_a.ycor()
    y += -42.8
    paddle_a.sety(y)


# Paddle A keyboard binding while True:
wn.listen()
wn.onkeypress(paddle_a_up, "w")  # <--zcontrol-a6-- Player A's paddle move UP
wn.onkeypress(paddle_a_up, "W")  # <--zcontrol-a6-- Player A's paddle move UP
wn.onkeypress(paddle_a_down, "s")  # <--zcontrol-a7-- Player A's paddle move DOWN
wn.onkeypress(paddle_a_down, "S")  # <--zcontrol-a7-- Player A's paddle move DOWN


# Paddle B functions
def paddle_b_up():
    y = paddle_b.ycor()
    y += 42.8
    paddle_b.sety(y)


def paddle_b_down():
    y = paddle_b.ycor()
    y += -42.8
    paddle_b.sety(y)


# Paddle B keyboard binding while True:
wn.listen()
wn.onkeypress(paddle_b_up, "Up")  # <--zcontrol-a8-- Player B's paddle move UP
wn.onkeypress(paddle_b_down, "Down")  # <--zcontrol-a9-- Player B's paddle move DOWN

while True:
    # Startup screen -- Countdown and gameplay window prep
    if ball.ycor() == 0:  # <---- Probably not best but hasn't broke yet (if additional colision physics are added, could cause bug from the coordinates)
        pen.goto(0, 0)
        pen.clear()
        pen.write("3", align="center", font=("lato", 95, "normal"))
        pen.clear()
        time.sleep(1)
        pen.write("2", align="center", font=("lato", 95, "normal"))
        pen.clear()
        time.sleep(1)
        pen.write("1", align="center", font=("lato", 95, "normal"))
        pen.clear()
        time.sleep(1)
        pen.color('green')
        pen.write("START", align="center", font=("lato", 100, "normal"))
        pen.clear()
        time.sleep(.4)
        pen.color('white')
        pen.goto(0, 260)
        pen.write("Player A: 0  Player B: 0", align="center", font=("courier", 24, "normal"))
        # Random ball direction at startup
        rand = random.randrange(0, 2)
        if rand < 2:
            ball.dy = 0.45
            ball.dx = 0.45
        if rand < 1:
            ball.dy = -0.45
            ball.dx = -0.45

    # Move the ball
    ball.setx(ball.xcor() + ball.dx)
    ball.sety(ball.ycor() + ball.dy)
    wn.update()
    # INSIDE OF THE GAME LOOP
    #########- gameDisplay.blit(bg, (0, 0))

    if ball.ycor() > -500 or ball.y < 500:
        point1 = (0, 400)
        point2 = (0, -400)

    # Border checking
    # Stop ball from going off screen vertically
    # Top border for ball
    if ball.ycor() > 290:
        ball.sety(290)
        ball.dy *= -1

    # Bottom border for ball
    if ball.ycor() < -290:
        ball.sety(-290)
        ball.dy *= -1

        # Stop paddles from going off screen
        # Player A's paddle border
    if (paddle_a.ycor() > 245):
        paddle_a.sety(245)
    if (paddle_a.ycor() < -242):
        paddle_a.sety(-242)

        # Player B's paddle border
    if (paddle_b.ycor() > 245):
        paddle_b.sety(245)
    if (paddle_b.ycor() < -242):
        paddle_b.sety(-242)

    # Scoring and events triggered by a score
    # Ball passes paddle on right - Player A scored, ball changes to their color, point added, speed adjusted, screen flash (IF scored 3 times then winner screen is shown)
    if ball.xcor() > 395:
        ball.setx(0)
        ball.dx *= -1
        score_a += 1
        ball.color("red")
        ball.shape("circle")
        wn.bgcolor("red")
        pen.clear()
        ball.shapesize(stretch_wid=1, stretch_len=1)
        # Reset ball speed if Player A scores
        ball.dy = ball_reset_dy
        ball.dx = ball_reset_dx_player_a  # <--zcontrol-a4-- Ball's LEFT/RIGHT, HORIZONTAL, X AXIS speed
        pen.write("Player A: {}  Player B: {}".format(score_a, score_b), align="center", font=("courier", 24, "normal"))
        time.sleep(.1)
        wn.bgcolor("black")
        # Finish game after X rounds and output Player A as winner
        if score_a > 2:  # <--zcontrol-b1-- Finish game after X rounds and output Player A as winner ***Default --- score_b > 2:
            pen.clear()
            wn.clear()
            wn.bgcolor("red")
            playsound('sounds/game_finish.mp3', block=False)
            pen.goto(0, 220)
            pen.write("Player A Wins!".format(score_a, a_collisions), align="center", font=("lato", 32, "normal"))
            pen.goto(0, 120)
            pen.write("With {} hits ".format(a_collisions), align="center", font=("lato", 32, "normal"))
            print("Player A Wins with {} points and {} collisions".format(score_a, a_collisions))
            # Keep count of games won via pickling
            player_a_scores_exists = path.exists("player_a_scores.pickle")
            if not player_a_scores_exists:
                pickle_out_a = open("player_a_scores.pickle", "wb")
                player_a_scores = 0
                pickle.dump(player_a_scores, pickle_out_a)
                pickle_out_a.close()
            player_b_scores_exists = path.exists("player_b_scores.pickle")
            if not player_b_scores_exists:
                pickle_out_b = open("player_b_scores.pickle", "wb")
                player_b_scores = 0
                pickle.dump(player_b_scores, pickle_out_b)
                pickle_out_b.close()
            # Bring in Player B's score for final game stats
            pickle_in_b = open("player_b_scores.pickle", "rb")
            player_b_scores = pickle.load(pickle_in_b)
            # Increment++ game wins by 1 for Player A
            pickle_in_a = open("player_a_scores.pickle", "rb")
            player_a_scores = pickle.load(pickle_in_a)
            player_a_scores += 1
            pickle_out_a = open("player_a_scores.pickle", "wb")
            pickle.dump(player_a_scores, pickle_out_a)
            pickle_out_a.close()
            print(player_a_scores)
            pen.goto(0, -20)
            pen.write("Player A total wins: {}".format(player_a_scores), align="center", font=("lato", 32, "normal"))
            pen.goto(0, -80)
            pen.write("Player B total wins: {}".format(player_b_scores), align="center", font=("lato", 32, "normal"))
            time.sleep(3)
            break

    # Ball passes paddle on left - Player B scored, ball changes to their color, point added, speed adjusted. If score 3 times then winner screen is shown, and winner point sent to player's PICKLE file to keep lifetime count.
    if ball.xcor() < -395:
        ball.setx(0)
        ball.dx *= -1
        score_b += 1
        wn.bgcolor("orange")
        ball.shape("circle")
        ball.color("orange")
        pen.clear()
        ball.shapesize(stretch_wid=1, stretch_len=1)
        # Reset ball speed if Player B scores
        ball.dy = ball_reset_dy
        ball.dx = ball_reset_dx_player_b
        pen.write("Player A: {}  Player B: {}".format(score_a, score_b), align="center", font=("courier", 24, "normal"))
        time.sleep(.1)
        wn.bgcolor("black")
        # Finish game after X rounds and output Player B as winner
        if score_b > 2:  # <--zcontrol-b2-- Finish game after X rounds and output Player B as winner ***Default --- score_b > 2:
            time.sleep(.14)
            pen.clear()
            wn.clear()
            wn.bgcolor("orange")
            playsound('sounds/game_finish.mp3', block=False)
            pen.goto(0, 220)
            pen.write("Player B Wins!".format(score_b, b_collisions), align="center", font=("lato", 32, "normal"))
            pen.goto(0, 120)
            pen.write("With {} hit(s) ".format(b_collisions), align="center", font=("lato", 32, "normal"))
            print("Player B Wins with {} points and {} collisions".format(score_b, b_collisions))
            # Keep count of games won via Pickling
            player_a_scores_exists = path.exists("player_a_scores.pickle")
            if not player_a_scores_exists:
                pickle_out_a = open("player_a_scores.pickle", "wb")
                player_a_scores = 0
                pickle.dump(player_a_scores, pickle_out_a)
                pickle_out_a.close()
            player_b_scores_exists = path.exists("player_b_scores.pickle")
            if not player_b_scores_exists:
                pickle_out_b = open("player_b_scores.pickle", "wb")
                player_b_scores = 0
                pickle.dump(player_b_scores, pickle_out_b)
                pickle_out_b.close()
            # Bring in Player A's score for final game stats
            pickle_in_a = open("player_a_scores.pickle", "rb")
            player_a_scores = pickle.load(pickle_in_a)
            # Increment++ game wins by 1 for Player B


            pickle_in_b = open("player_b_scores.pickle", "rb")
            player_b_scores = pickle.load(pickle_in_b)
            player_b_scores += 1
            pickle_out_b = open("player_b_scores.pickle", "wb")
            pickle.dump(player_b_scores, pickle_out_b)
            pickle_out_b.close()
            print(player_b_scores)
            pen.goto(0, -20)
            pen.write("Player A total wins: {}".format(player_a_scores), align="center", font=("lato", 32, "normal"))
            pen.goto(0, -80)
            pen.write("Player B total wins: {}".format(player_b_scores), align="center", font=("lato", 32, "normal"))
            
            wn.listen()
            wn.onkeypress(score_reset, "r") # <--zcontrol-a?-- Reset scores
            wn.onkeypress(score_reset, "R") # <--zcontrol-a? -- Reset scores

            pen.goto(0, -140)
            pen.write("Press R to reset scores", align="center", font=("lato", 32, "normal"))

            ###TODO: Finish deletion code

            turtle.mainloop()

            time.sleep(3)
            break

    # Reset ball bounce effects
    # Add bounce and speed effects to ball
    # Thinnest shape 1/10
    if (ball.shape() == "circle" and ball.xcor() < 300 and ball.xcor() > -300):
        ball.shapesize(stretch_wid=.8, stretch_len=.9)
    if (ball.shape() == "triangle" and ball.xcor() < 210 and ball.xcor() > -210):
        ball.shapesize(stretch_wid=4, stretch_len=2)
        # Regaining shape 2/10
    if (ball.shape() == "circle" and ball.xcor() < 200 and ball.xcor() > -200):
        ball.shapesize(stretch_wid=.56, stretch_len=1)
        # Regaining shape 3/10
    if (ball.shape() == "circle" and ball.xcor() < 190 and ball.xcor() > -200):
        ball.shapesize(stretch_wid=.60, stretch_len=1)
        # Regaining shape 4/10
    if (ball.shape() == "circle" and ball.xcor() < 190 and ball.xcor() > -200):
        ball.shapesize(stretch_wid=.64, stretch_len=1)
        # Regaining shape 5/10
    if (ball.shape() == "circle" and ball.xcor() < 180 and ball.xcor() > -200):
        ball.shapesize(stretch_wid=.67, stretch_len=1)
        # Regaining shape 6/10
    if (ball.shape() == "circle" and ball.xcor() < 160 and ball.xcor() > -160):
        ball.shapesize(stretch_wid=.70, stretch_len=1)
        # Regaining shape 7/10
    if (ball.shape() == "circle" and ball.xcor() < 125 and ball.xcor() > -125):
        ball.shapesize(stretch_wid=.73, stretch_len=1)
        # Regaining shape 8/10
    if (ball.shape() == "circle" and ball.xcor() < 125 and ball.xcor() > -125):
        ball.shapesize(stretch_wid=.86, stretch_len=1)
        # Regaining shape 9/10
    if (ball.shape() == "circle" and ball.xcor() < 80 and ball.xcor() > -80):
        ball.shapesize(stretch_wid=1, stretch_len=1)
        # Back to full size and shape 10/10
    if (ball.shape() == "triangle" and ball.xcor() < 210 and ball.xcor() > -210):  # Nuclear attack ball bounce finish
        ball.shapesize(stretch_wid=4, stretch_len=4)

    # Paddles and ball collisions
    # Player A
    if (ball.xcor() < -330 and ball.xcor() > -340) and (
            ball.ycor() < paddle_a.ycor() + 59 and ball.ycor() > paddle_a.ycor() - 59):
        ball.dx *= -1
        ball.dx *= 1.19
        ball.dy *= -1.3
        ball.sety(ball.ycor() + ball.dy + 5)
        a_collisions += 1
        playsound('sounds/player_a_hit.mp3', block=False)
        ball.shapesize(stretch_wid=1, stretch_len=.5)  # Squish ball/Bounce effect when hits paddle
        # Random "Super attack"
        rand = random.randrange(0, 15)  # 1/15 chance - Update both player's rand variables for fair gameplay.
        if rand < 2:
            wn.bgcolor("white")
            time.sleep(.1)
            wn.bgcolor("red")
            time.sleep(.1)
            wn.bgcolor("white")
            time.sleep(.1)
            ball.dy = 0.12
            ball.dx = 0.11
            ball.dy *= 6.1
            ball.dx *= 9.2
            wn.bgcolor("black")
            ball.color("red")
        # Nuclear Super attack
        if keyboard.is_pressed('Space'):
            playsound('sounds/pre_attack.mp3', block=False)
            playsound('sounds/nuclear_attack.mp3', block=False)
            ball.dy = ball_reset_dy
            ball.dy = 20
            ball.dx = 3.9
            ball.setheading(0)
            ball.color("red")
            ball.shape("triangle")
            ball.shapesize(stretch_wid=2, stretch_len=4)  # Squish ball/Bounce effect when hits paddle
            wn.bgcolor("white")
            time.sleep(.1)
            wn.bgcolor("red")
            time.sleep(.1)
            wn.bgcolor("white")
            time.sleep(.2)
            wn.bgcolor("red")
            time.sleep(.2)
            wn.bgcolor("black")
            time.sleep(.1)
        # When ball collides with paddle, ball's y axis is random
        rand = random.randrange(0, 2)
        if rand < 2:
            ball.dy = 0.45
        if rand < 1:
            ball.dy = 0.45

    # Player B
    if (ball.xcor() > 330 and ball.xcor() < 340) and (
            ball.ycor() < paddle_b.ycor() + 59 and ball.ycor() > paddle_b.ycor() - 59):
        ball.setx(330)
        ball.dx *= -1
        ball.dx *= 1.19
        ball.sety(ball.ycor() + ball.dy + 5)
        b_collisions += 1
        playsound('sounds/player_b_hit.mp3', block=False)
        ball.shapesize(stretch_wid=1, stretch_len=.5)  # Squish ball/Bounce effect when hits paddle
        # Auto Super attack
        rand = random.randrange(0,
                                15)  # 1/15 chance - Update both player's rand variables for fair gameplay. (or don't)
        if rand < 2:
            wn.bgcolor("white")
            time.sleep(.1)
            wn.bgcolor("orange")
            time.sleep(.1)
            wn.bgcolor("white")
            time.sleep(.1)
            ball.dy = 0.12
            ball.dx = -0.11
            ball.dy *= 6.1
            ball.dx *= 9.2
            wn.bgcolor("black")
            ball.color("red")
        # Nuclear Super attack
        if keyboard.is_pressed('0'):
            playsound('sounds/pre_attack.mp3', block=False)
            playsound('sounds/nuclear_attack.mp3', block=False)
            ball.dy = 3.9
            ball.dx = -3.3
            ball.setheading(180)
            ball.shape("triangle")
            ball.color("orange")
            ball.shape("triangle")
            ball.shapesize(stretch_wid=2, stretch_len=4)  # Squish ball/Bounce effect when hits paddle
            wn.bgcolor("white")
            time.sleep(.1)
            wn.bgcolor("orange")
            time.sleep(.1)
            wn.bgcolor("yellow")
            time.sleep(.1)
            wn.bgcolor("white")
            time.sleep(.2)
            wn.bgcolor("black")
            time.sleep(.1)

        # When ball collides with paddle, ball's y axis is random
        rand = random.randrange(0, 3)
        if rand < 2:
            ball.dy *= 0.45
        if rand > 2:
            ball.dy *= -0.45
