import turtle
turtle.color('blue', 'green')
turtle.speed(0)
for step in range(6):
    turtle.forward(100)
    turtle.right(60)
    turtle.begin_fill()
    for step_1 in range(3):
        turtle.forward(100)
        turtle.left(120)
    turtle.end_fill()
turtle.forward(50)
turtle.circle(-86)
turtle.hideturtle()
turtle.penup()
turtle.sety(-120)
turtle.pendown()
turtle.write('A', align='center', font=('Arial', 48, 'bold'))
turtle.done()
