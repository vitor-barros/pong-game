import turtle
import sqlite3

wn = turtle.Screen()
wn.title("Jogo de Pong")
wn.bgcolor("black")
wn.setup(width=800, height=600)
wn.tracer(0)

# pontos
score_a = 0
score_b = 0
placarA = score_a + score_a
placarB = score_b + score_b


# barrinha 1

paddle_a = turtle.Turtle()
paddle_a.speed(0)
paddle_a.shape("square")
paddle_a.color("white")
paddle_a.shapesize(stretch_wid=5, stretch_len=1)
paddle_a.penup()
paddle_a.goto(-350, 0)

# barrinha 2

paddle_b = turtle.Turtle()
paddle_b.speed(0)
paddle_b.shape("square")
paddle_b.color("white")
paddle_b.shapesize(stretch_wid=5, stretch_len=1)
paddle_b.penup()
paddle_b.goto(350, 0)

# bola

ball = turtle.Turtle()
ball.speed(0)
ball.shape("square")
ball.color("white")
ball.penup()
ball.goto(0, 0)
ball.dx = 0.6  # sempre que a bola mexer, ela mexe em 2 pixels
ball.dy = -0.6  # sempre que a bola mexer, ela mexe em 2 pixels


# pen
pen = turtle.Turtle()
pen.speed(0)
pen.color("white")
pen.penup()
pen.hideturtle()
pen.goto(0, 260)
pen.write("MAX:  Player A: 0  Player B: 0  MAX:", align="center", font=("Courier", 20, "normal"))

'''

conn = sqlite3.connect('pong.db')
c = conn.cursor()
c.execute("""CREATE TABLE IF NOT EXISTS placar (
    id integer primary key,\
    placarA integer,\
    placarB integer
    )""")

c.execute("""INSERT into placar values (1,0,0)""")
conn.commit()
conn.close()
'''

# Funções

def insertA():
    conn = sqlite3.connect('pong.db')
    c = conn.cursor()

    for row in c.execute('''SELECT placarA from placar where id = 1 '''):
        placarA = row[0]
    if placarA < score_a:
        c.execute(f"UPDATE placar set placarA = {score_a} where id =1")
        conn.commit()
    
    return placarA

def insertB():
    conn = sqlite3.connect('pong.db')
    c = conn.cursor()

    for row in c.execute('''SELECT placarB from placar where id =1 '''):
        placarB = row[0]
    
    if placarB < score_b:
        c.execute(f"UPDATE placar set placarB = {score_b} where id =1")
        conn.commit()
    return placarB



def paddle_a_up():
    y = paddle_a.ycor()  # retorna a cordenada y
    y += 20
    paddle_a.sety(y)


def paddle_a_down():
    y = paddle_a.ycor()  # retorna a cordenada y
    y -= 20
    paddle_a.sety(y)


def paddle_b_up():
    y = paddle_b.ycor()  # retorna a cordenada y
    y += 20
    paddle_b.sety(y)


def paddle_b_down():
    y = paddle_b.ycor()  # retorna a cordenada y
    y -= 20
    paddle_b.sety(y)


# Ações do teclado!
wn.listen()
wn.onkeypress(paddle_a_up, "w")
wn.onkeypress(paddle_a_down, "s")
wn.onkeypress(paddle_b_up, "Up")
wn.onkeypress(paddle_b_down, "Down")


# Main game

while True:
    wn.update()

    # movendo a bola
    ball.setx(ball.xcor() + ball.dx)
    ball.sety(ball.ycor() + ball.dy)

    # controle das bordas
    if ball.ycor() > 290:
        ball.sety(290)
        ball.dy *= -1  # recocheteia a bola, pq vai dar um número igual negativo

    if ball.ycor() < -290:
        ball.sety(-290)
        ball.dy *= -1  # recocheteia a bola, pq vai dar um número igual negativo

    if ball.xcor() > 390:
        ball.goto(0, 0)
        ball.dx *= -1
        score_a += 1
    pen.clear()  
    pen.write("MAX: {} Player A: {}  Player B: {}  MAX: {}".format(insertA(),score_a, score_b, insertB()), align="center", font=("Courier", 20, "normal"))
        

    if ball.xcor() < -390:
        ball.goto(0, 0)
        ball.dx *= -1
        score_b += 1
        #pen.clear()
        #pen.write("MAX: {} Player A: {}  Player B: {}  MAX: {} ".format(insertA(), score_a, score_b,insertB()), align="center", font=("Courier", 20, "normal"))

    # colisões!

    if 340 < ball.xcor() < 350 and paddle_b.ycor() + 40 > ball.ycor() > paddle_b.ycor() - 40:
        ball.setx(340)
        ball.dx *= -1

    if -340 > ball.xcor() > -350 and paddle_a.ycor() + 40 > ball.ycor() > paddle_a.ycor() - 40:
        ball.setx(-340)
        ball.dx *= -1