def arrow(direction):
    if direction=="dx":
        points = [200,175,300,175,300,125,450,200,300,275,300,225,200,225]
    if direction=="sx":
        points = [200,200,350,125,350,175,450,175,450,225,350,225,350,275]
    if direction=="up":
        points = [225,200,300,50,375,200,325,200,325,300,275,300,275,200]
    if direction=="back":
        points = [275,50,325,50,325,150,375,150,300,300,225,150,275,150]

    return points