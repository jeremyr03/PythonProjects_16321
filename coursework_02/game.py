from tkinter import *
import time
import random
from datetime import datetime
import os

geometry = '1920x1080'


def update(ind):
    global character_status, i
    if character_status == CHARACTER_STATUS[1]:
        ind += 1
        if not (ind < 7):
            ind = 0
        # print(ind)
        canvas.itemconfig(character, image=user_run[ind])

    elif character_status == CHARACTER_STATUS[0]:
        ind += 1
        if ind == 11:
            ind = 0
        canvas.itemconfig(character, image=user_idle[ind])

    elif character_status == CHARACTER_STATUS[2]:
        # print(i)
        if i <= 9:
            canvas.itemconfig(character, image=user_jump[0])
            canvas.move(character, 0, -30)
            i += 1
        elif i <= 11:
            canvas.itemconfig(character, image=user_jump[i % 2])
            i += 1
        elif i <= 21:
            canvas.itemconfig(character, image=user_jump[3])
            canvas.move(character, 0, 30)
            i += 1
        else:
            character_status = CHARACTER_STATUS[1]
            i = 0
            canvas.itemconfig(character, image=user_run[0])
    elif character_status == CHARACTER_STATUS[4]:
        ind += 1
        if ind == 11:
            ind = 0
        canvas.itemconfig(character, image=user_idle[ind])


    # print("number of overlaps", overlapping(character))
    root.after(70, update, ind)


def go():
    global character_status, txt
    for k in menu:
        k.destroy()
    character_status = CHARACTER_STATUS[1]
    pos = canvas.coords(character)
    if pos[0] < 900:
        canvas.move(character, 10, 0)
        root.after(30, go)
        pos = canvas.coords(character)
        # print(pos)
    bg()
    Floor()
    # scoreboard = Label(text=f"{score} seconds",  bg="#b36029", foreground="#fbff19", font=("Times New Roman", 36, "bold"))
    # canvas.create_window(1000, 100, window=scoreboard, height=100, width=400, )
    start()

    root.after(2500, obstacles)


def start():
    global score, old, txt
    if character_status != CHARACTER_STATUS[4]:
        new = time.time()
        print(new)
        print(f"new {new} | old {old}")
        if (new - old) >= 1:
            try:
                canvas.delete(txt)
            except:
                pass
            score += 1
            old = new
            txt = canvas.create_text(1000, 100, text=f"{score} seconds", fill="#fbff19", font=("Times New Roman", 36, "bold"))

    root.after(5000, start)


def config(event=None):
    global w
    for k in menu:
        k.destroy()
    w = LabelFrame(text=f"Jump: {space}")
    canvas.create_window(1000, 500, window=w, height=100, width=400)
    canvas.unbind_all("<space>")
    canvas.bind_all("<Key>", new_pressed)


def new_pressed(e):
    global space
    space = e.char
    print(e.char)
    w['text'] = f"Jump: {space}"
    canvas.unbind_all("<Key>")
    canvas.bind_all(f"<{space}>", jump)
    w.destroy()
    go()


def bg():
    global background
    if character_status != CHARACTER_STATUS[4]:
        for k in background:
            for j in k:
                canvas.move(j, -0.25, 0)
                if canvas.coords(j)[0] <= (960 - 1920):
                    canvas.coords(j, (960 + int(1920 / 2)), 400)

    root.after(500, bg)


def Floor():
    global floor
    if character_status != CHARACTER_STATUS[4]:
        for k in floor:
            canvas.move(k, -2, 0)
            if canvas.coords(k)[0] <= (100 - 640):
                canvas.coords(k, (100 + ((640 / 2) * 7)), 900)

    root.after(500, Floor)


def jump(event=None):
    global character_status
    if character_status != (CHARACTER_STATUS[0] or CHARACTER_STATUS[4]):
        character_status = CHARACTER_STATUS[2]


def overlapping(item1, item2=None):
    # print(canvas.bbox(character))
    # overlap = canvas.find_overlapping(canvas.bbox(item1)[0],
    #                                   canvas.bbox(item1)[1],
    #                                   canvas.bbox(item1)[2],
    #                                   canvas.bbox(item1)[3])
    # try:
    #     return overlap[1]
    #
    # except:
    #     return 0
    coords_1 = canvas.bbox(item1)
    coords_2 = canvas.coords(item2)

    # Checks if max&min(x,y) of item 2 is within the max&min(x,y) of item 1
    if ((coords_1[1] <= coords_2[1] <= coords_1[3]) or (coords_1[1] <= coords_2[1] <= coords_1[3])) \
            and ((coords_1[0] <= coords_2[0] <= coords_1[2]) or (coords_1[0] <= coords_2[0] <= coords_1[2])):
        return 1

    print(f"item1 {coords_1} | item2 {coords_2}")
    return 0


def obstacles():
    # root.after(random.randint(50, 100))
    # obstacle.append(canvas.create_image(1000, 700, image=random.choices(obstacle_items, weights=[1], k=1)[0]))
    if character_status != CHARACTER_STATUS[4]:
        for k in obstacle:
            canvas.move(k, -1.5, 0)
            if 500 < canvas.coords(k)[0] < 1500:
                if overlapping(character, k):
                    end()
                    break
            if canvas.coords(k)[0] < -400:
                print(canvas.coords(k))
                canvas.move(k, 100000, 0)
                print(canvas.coords(k))
    root.after(200, obstacles)


def end():
    global character_status
    character_status = CHARACTER_STATUS[4]


root = Tk()
root.geometry(geometry)
canvas = Canvas(width='9000', height='1080')
canvas.pack()
CHARACTER_STATUS = ("idle", "run", "jump", "fall", "game-over")
# Used in Update subroutine
i = 0

# Setting up background & foreground
background = [[], [], [], []]
bg1 = PhotoImage(file="assets/background/bg1.gif").zoom(5)
bg2 = PhotoImage(file="assets/background/bg2.gif").zoom(5)
bg3 = PhotoImage(file="assets/background/bg3.gif").zoom(5)
bg4 = PhotoImage(file="assets/background/bg3.gif").zoom(5)
# print(bg1.width(), bg1.height())
background[0].append(canvas.create_image(960, 400, image=bg1))
background[0].append(canvas.create_image(960, 400, image=bg2))
background[0].append(canvas.create_image(960, 400, image=bg3))
background[0].append(canvas.create_image(960, 400, image=bg4))
background[1].append(canvas.create_image(canvas.coords(background[0][0])[0] + bg1.width(), 400, image=bg1))
background[1].append(canvas.create_image(canvas.coords(background[0][1])[0] + bg2.width(), 400, image=bg2))
background[1].append(canvas.create_image(canvas.coords(background[0][2])[0] + bg3.width(), 400, image=bg3))
background[1].append(canvas.create_image(canvas.coords(background[0][3])[0] + bg4.width(), 400, image=bg4))
background[2].append(canvas.create_image(canvas.coords(background[1][0])[0] + bg1.width(), 400, image=bg1))
background[2].append(canvas.create_image(canvas.coords(background[1][1])[0] + bg2.width(), 400, image=bg2))
background[2].append(canvas.create_image(canvas.coords(background[1][2])[0] + bg3.width(), 400, image=bg3))
background[2].append(canvas.create_image(canvas.coords(background[1][3])[0] + bg4.width(), 400, image=bg4))
background[3].append(canvas.create_image(canvas.coords(background[2][0])[0] + bg1.width(), 400, image=bg1))
background[3].append(canvas.create_image(canvas.coords(background[2][1])[0] + bg2.width(), 400, image=bg2))
background[3].append(canvas.create_image(canvas.coords(background[2][2])[0] + bg3.width(), 400, image=bg3))
background[3].append(canvas.create_image(canvas.coords(background[2][3])[0] + bg4.width(), 400, image=bg4))

menu = [Label(canvas, text="Jungle Run", bg="#b36029", foreground="#fbff19", font=("Times New Roman", 36, "bold")),
        Button(canvas, text="start", bg="#b36029", foreground="#fbff19", command=go, font=("helvetica", 25)),
        Button(canvas, text="leaderboard", bg="#b36029", foreground="#fbff19", command=go, font=("helvetica", 25)),
        Button(canvas, text="configure", bg="#b36029", foreground="#fbff19", command=config, font=("helvetica", 25))]
temp = 100
for k in menu:
    canvas.create_window(1000, temp, window=k, height=100, width=400)
    temp += 150

flr = [PhotoImage(file='assets/foreground/floor1.gif').zoom(4) for k in range(7)]
floor = [canvas.create_image((100 + (flr[k].width() * k)), 900, image=flr[k]) for k in range(7)]

# dimensions = "image size: %dx%d" % (flr.width(), flr.height())
# print(flr[0].height())

# Setting up Character
char_pos = [200, 700]
user_idle = [PhotoImage(file="assets/sprites/idle.gif", format=f"gif -index {k}").zoom(10) for k in range(11)]
user_run = [PhotoImage(file="assets/sprites/run.gif", format=f"gif -index {k}").zoom(10) for k in range(7)]
user_jump = [PhotoImage(file='assets/sprites/jump.png').zoom(10),
             PhotoImage(file='assets/sprites/landing.png').zoom(10)]
for k in range(2):
    user_jump.append(PhotoImage(file="assets/sprites/mid air.gif", format=f"gif -index {k}").zoom(10))

character = canvas.create_image(char_pos[0], char_pos[1], image=user_idle[0])
character_status = CHARACTER_STATUS[0]
# print(overlapping(character))

# Setting up obstacles
obstacle_items = [PhotoImage(file="assets/arrow.gif")]
# Used in subroutine
obstacle = []
temp = 2000
for k in random.choices(obstacle_items, [1], k=50):
    obstacle.append(canvas.create_image(temp, 700, image=k))
    temp += random.randint(1000, 2000)

# Setting up Score
score = 0
old = time.time()
txt = None

# Setting up controls
left_key, right_key, space = "Left", "Right", "space"
# canvas.bind_all(f"<{right_key}>", lambda e: right())
canvas.bind_all(f"<{space}>", jump)
# canvas.bind_all(f"<{left_key}>", lambda e: left())


label = Label(root)
label.place()
label.pack()

root.after(0, update, 0)
root.mainloop()
