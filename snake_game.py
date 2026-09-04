import turtle
import random

# =========================
# GAME SETTINGS
# =========================

WIDTH = 600
HEIGHT = 600

delay = 120
score = 0
high_score = 0

game_running = True


# =========================
# SCREEN
# =========================

screen = turtle.Screen()
screen.title("Snake Game")
screen.bgcolor("black")
screen.setup(width=WIDTH, height=HEIGHT)
screen.tracer(0)


# =========================
# SNAKE HEAD
# =========================

head = turtle.Turtle()
head.speed(0)
head.shape("square")
head.color("lime")
head.penup()
head.goto(0, 0)

head.direction = "stop"


# =========================
# FOOD
# =========================

food = turtle.Turtle()
food.speed(0)
food.shape("circle")
food.color("yellow")
food.penup()
food.goto(0, 100)


# =========================
# SNAKE BODY
# =========================

body = []


# =========================
# SCORE
# =========================

score_pen = turtle.Turtle()
score_pen.speed(0)
score_pen.color("white")
score_pen.penup()
score_pen.hideturtle()
score_pen.goto(0, 260)


def update_score():
    score_pen.clear()

    score_pen.write(
        "Score: {}    High Score: {}".format(score, high_score),
        align="center",
        font=("Arial", 18, "bold")
    )


update_score()


# =========================
# GAME OVER MESSAGE
# =========================

message_pen = turtle.Turtle()
message_pen.speed(0)
message_pen.color("white")
message_pen.penup()
message_pen.hideturtle()


# =========================
# MOVEMENT FUNCTIONS
# =========================

def go_up():
    if head.direction != "down":
        head.direction = "up"


def go_down():
    if head.direction != "up":
        head.direction = "down"


def go_left():
    if head.direction != "right":
        head.direction = "left"


def go_right():
    if head.direction != "left":
        head.direction = "right"


def move():

    if head.direction == "up":
        head.sety(head.ycor() + 20)

    elif head.direction == "down":
        head.sety(head.ycor() - 20)

    elif head.direction == "left":
        head.setx(head.xcor() - 20)

    elif head.direction == "right":
        head.setx(head.xcor() + 20)


# =========================
# CREATE SNAKE BODY
# =========================

def create_body_part():

    part = turtle.Turtle()

    part.speed(0)
    part.shape("square")
    part.color("green")
    part.penup()

    part.goto(1000, 1000)

    body.append(part)


# =========================
# MOVE FOOD
# =========================

def move_food():

    while True:

        x = random.randint(-14, 14) * 20
        y = random.randint(-11, 12) * 20

        # Don't put food on head
        if abs(x - head.xcor()) < 20 and abs(y - head.ycor()) < 20:
            continue

        # Don't put food on body
        occupied = False

        for part in body:

            if abs(x - part.xcor()) < 20 and abs(y - part.ycor()) < 20:
                occupied = True
                break

        if not occupied:
            food.goto(x, y)
            break


# =========================
# GAME OVER
# =========================

def game_over():

    global game_running

    game_running = False

    message_pen.clear()

    message_pen.goto(0, 30)

    message_pen.write(
        "GAME OVER",
        align="center",
        font=("Arial", 32, "bold")
    )

    message_pen.goto(0, -20)

    message_pen.write(
        "Press R to Restart",
        align="center",
        font=("Arial", 18, "normal")
    )

    screen.update()


# =========================
# RESTART GAME
# =========================

def restart_game():

    global score
    global delay
    global game_running

    # Remove old body
    for part in body:
        part.goto(1000, 1000)

    body.clear()

    # Reset values
    score = 0
    delay = 120
    game_running = True

    # Reset snake
    head.goto(0, 0)
    head.direction = "stop"

    # Reset food
    food.goto(0, 100)

    # Remove Game Over message
    message_pen.clear()

    # Reset score
    update_score()

    screen.update()

    # Start game loop again
    game_loop()


# =========================
# MAIN GAME LOOP
# =========================

def game_loop():

    global score
    global high_score
    global delay

    # If game is over, don't continue moving
    if not game_running:
        return

    # -------------------------
    # MOVE BODY
    # -------------------------

    for i in range(len(body) - 1, 0, -1):

        x = body[i - 1].xcor()
        y = body[i - 1].ycor()

        body[i].goto(x, y)

    # First body part follows head
    if len(body) > 0:

        body[0].goto(
            head.xcor(),
            head.ycor()
        )

    # -------------------------
    # MOVE HEAD
    # -------------------------

    move()

    # -------------------------
    # WALL COLLISION
    # -------------------------

    if (
        head.xcor() > 290
        or head.xcor() < -290
        or head.ycor() > 290
        or head.ycor() < -290
    ):

        game_over()
        return

    # -------------------------
    # FOOD COLLISION
    # -------------------------

    if head.distance(food) < 20:

        # Grow snake
        create_body_part()

        # Increase score
        score += 10

        # High score
        if score > high_score:
            high_score = score

        # Increase speed
        if delay > 45:
            delay -= 5

        # Update score
        update_score()

        # Move food
        move_food()

    # -------------------------
    # BODY COLLISION
    # -------------------------

    for part in body:

        if part.distance(head) < 10:

            game_over()
            return

    # Update screen
    screen.update()

    # Run game loop again
    screen.ontimer(game_loop, delay)


# =========================
# KEYBOARD CONTROLS
# =========================

screen.listen()

screen.onkey(go_up, "Up")
screen.onkey(go_down, "Down")
screen.onkey(go_left, "Left")
screen.onkey(go_right, "Right")

# Restart
screen.onkey(restart_game, "r")
screen.onkey(restart_game, "R")

# Force keyboard focus
screen.getcanvas().focus_force()


# =========================
# START GAME
# =========================

game_loop()

screen.mainloop()