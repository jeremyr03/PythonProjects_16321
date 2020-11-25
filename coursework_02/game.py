from tkinter import *
import time
geometry = '1920x1080'


def update(ind,):
    if character_status == CHARACTER_STATUS[1]:
        ind += 1
        if not(ind < 7):
            ind = 0
        print(ind)
        canvas.itemconfig(character, image=user_run[ind])

    elif character_status == CHARACTER_STATUS[0]:
        ind += 1
        if ind == 11:
            ind = 0

        canvas.itemconfig(character, image=user_idle[ind])
    print(character_status)
    root.after(80, update, ind)


def go():
    global character_status
    character_status = CHARACTER_STATUS[1]
    pos = canvas.coords(character)
    if pos[0] < 900:
        canvas.move(character, 10, 0)
        root.after(30, go)
        pos = canvas.coords(character)
        print(pos)
    bg()
    Floor()


def bg():
    global background
    for i in background:
        for j in i:
            canvas.move(j, -0.5, 0)
            if canvas.coords(j)[0] <= (960 - 1920):
                canvas.coords(j, (960 + (1920/2)), 400)

    root.after(500, bg)


def Floor():
    global floor
    for i in floor:
        canvas.move(i, -2, 0)
        if canvas.coords(i)[0] <= (100 - 640):
            canvas.coords(i, (100 + ((640/2) * 7)), 900)

    root.after(500, Floor)


def right(event=None):
    print("r key presed")
    if character_status == CHARACTER_STATUS[1]:
        pass


def left(event=None):
    print("l key pressed")
    go()


root = Tk()
root.geometry(geometry)
canvas = Canvas(width='9000', height='1080')
canvas.pack()
CHARACTER_STATUS = ("idle", "run", "jump", "fall", "ledge")

# Setting up background & foreground
background = [[], [], []]
bg1 = PhotoImage(file="assets/background/bg1.gif").zoom(5)
bg2 = PhotoImage(file="assets/background/bg2.gif").zoom(5)
bg3 = PhotoImage(file="assets/background/bg3.gif").zoom(5)
bg4 = PhotoImage(file="assets/background/bg3.gif").zoom(5)
print(bg1.width(), bg1.height())
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

flr = [PhotoImage(file='assets/foreground/floor1.gif').zoom(4) for i in range(7)]
floor = [canvas.create_image((100 + (flr[i].width()*i)), 900, image=flr[i]) for i in range(7)]

# dimensions = "image size: %dx%d" % (flr.width(), flr.height())
print(flr[0].height())

# Setting up Character
char_pos = [100, 700]
user_idle = [PhotoImage(file="assets/sprites/idle.gif", format=f"gif -index {i}").zoom(10) for i in range(11)]
user_run = [PhotoImage(file="assets/sprites/run.gif", format=f"gif -index {i}").zoom(10) for i in range(7)]
character = canvas.create_image(char_pos[0], char_pos[1], image=user_idle[0])
character_status = CHARACTER_STATUS[0]

# Setting up controls
left_key, right_key = "Left", "Right"
canvas.bind_all(f"<{right_key}>", lambda e: right())
canvas.bind_all(f"<{left_key}>", lambda e: left())


label = Label(root)
label.place()
label.pack()

root.after(0, update, 0)
root.mainloop()
