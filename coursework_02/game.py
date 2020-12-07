from tkinter import *
import tkinter.scrolledtext as tkscroll
import tkinter.messagebox as message
import time
import random
import os

# 1920x1080

root = Tk()
geometry = '1920x1080'
root.geometry(geometry)


def update(ind):
    global character_status, update_i
    if character_status == CHARACTER_STATUS[1]:
        ind += 1
        if not (ind < 7):
            ind = 0
        canvas.itemconfig(character, image=user_run[ind])

    elif character_status == CHARACTER_STATUS[0]:
        ind += 1
        if ind == 11:
            ind = 0
        canvas.itemconfig(character, image=user_idle[ind])

    elif character_status == CHARACTER_STATUS[2]:
        if update_i <= 9:
            canvas.itemconfig(character, image=user_jump[0])
            canvas.move(character, 0, -30)
            update_i += 1
        elif update_i <= 11:
            canvas.itemconfig(character, image=user_jump[update_i % 2])
            update_i += 1
        elif update_i <= 21:
            canvas.itemconfig(character, image=user_jump[3])
            canvas.move(character, 0, 30)
            update_i += 1
        else:
            character_status = CHARACTER_STATUS[1]
            update_i = 0
            canvas.itemconfig(character, image=user_run[0])
    elif character_status == CHARACTER_STATUS[4]:
        pass

    root.after(70, update, ind)


def go():
    global character_status, txt, pause_button
    for i in menu:
        i.destroy()
    character_status = CHARACTER_STATUS[1]
    pos = canvas.coords(character)
    if pos[0] < 900:
        canvas.move(character, 10, 0)
        root.after(30, go)
        pos = canvas.coords(character)

    bg()
    Floor()
    start()
    pause_button = Button(canvas, text="| |", command=pause_command, bg="#db9160", foreground="#fbff19", font=("Times New Roman", 36, "bold"))
    pause = canvas.create_window(1870, 50, window=pause_button, height=100, width=100, tag="pause_canvas")
    canvas.tag_raise(pause)

    root.after(2500, obstacles)


def pause_command():
    global character_status, prev_status
    prev_status = character_status
    character_status = CHARACTER_STATUS[4]
    pause_button['text'] = "▶"
    pause_button['command'] = play


def play():
    global character_status
    character_status = prev_status
    pause_button['text'] = "| |"
    pause_button['command'] = pause_command


def start():
    global score, old, txt
    if character_status != CHARACTER_STATUS[4]:
        new = time.time()
        if (new - old) >= 1:
            try:
                canvas.delete(txt)
            finally:
                pass
            score += 1
            old = new
            txt = canvas.create_text(1000, 100, text=f"{score} seconds", fill="#fbff19", font=("Times New Roman", 36, "bold"))

    root.after(5000, start)


def main_menu():
    pass


def config(event=None):
    global space
    for i in menu:
        i.destroy()

    canvas1 = Canvas(canvas)
    canvas.create_window(1000, 500, window=canvas1)
    space = StringVar(canvas1)
    space.set(extra_keys[0])
    label1 = Label(canvas1, text="Jump:", font=("Times New Roman", 20, "bold"))
    label1.grid(row=0, column=0)
    emptylabel = Label(canvas1)
    emptylabel.grid(row=1)
    w = OptionMenu(canvas1, space, *(keyboard + extra_keys))
    w.config(font=("Times New Roman", 20, "italic"))
    w.grid(row=0, column=1)
    menu_button = Button(canvas1, text="Menu", command=lambda: main_menu(), font=("Times New Roman", 20))
    menu_button.grid(row=2, column=0, columnspan=2)

    # w = LabelFrame(text=f"Jump: {space}")

    # canvas.unbind_all("<space>")
    # canvas.bind_all("<Key>", new_pressed)


def new_pressed(e):
    global space
    space = e.char
    w['text'] = f"Jump: {space}"
    canvas.unbind_all("<Key>")
    canvas.bind_all(f"<{space}>", jump)
    w.destroy()
    go()


def bg():
    global background
    if character_status != CHARACTER_STATUS[4]:
        for i in background:
            for j in i:
                canvas.move(j, -0.25, 0)
                if canvas.coords(j)[0] <= (960 - 1920):
                    canvas.coords(j, (960 + int(1920 / 2)), 400)

    root.after(500, bg)


def Floor():
    global floor
    if character_status != CHARACTER_STATUS[4]:
        for i in floor:
            canvas.move(i, -2, 0)
            if canvas.coords(i)[0] <= (100 - 640):
                canvas.coords(i, (100 + ((640 / 2) * 7)), 900)

    root.after(500, Floor)


def jump(event=None):
    global character_status
    if character_status != CHARACTER_STATUS[0] or CHARACTER_STATUS[4]:
        character_status = CHARACTER_STATUS[2]


def overlapping(item1, item2=None):
    coords_1 = canvas.bbox(item1)
    coords_2 = canvas.coords(item2)

    # Checks if max&min(x,y) of item 2 is within the max&min(x,y) of item 1
    if ((coords_1[1] <= coords_2[1] <= coords_1[3]) or (coords_1[1] <= coords_2[1] <= coords_1[3])) \
            and ((coords_1[0] <= coords_2[0] <= coords_1[2]) or (coords_1[0] <= coords_2[0] <= coords_1[2])):
        return 1

    return 0


def obstacles():
    # root.after(random.randint(50, 100))
    # obstacle.append(canvas.create_image(1000, 700, image=random.choices(obstacle_items, weights=[1], k=1)[0]))
    if character_status != CHARACTER_STATUS[4]:
        for i in obstacle:
            canvas.move(i, -1.5, 0)
            if 500 < canvas.coords(i)[0] < 1500:
                if overlapping(character, i):
                    end()
                    break
            if canvas.coords(i)[0] < -400:
                canvas.move(i, 100000, 0)
    root.after(200, obstacles)


def end():
    global character_status, user_score, leaderboard_prompt
    character_status = CHARACTER_STATUS[4]

    end_screen = canvas.create_window(960, 540)
    user_score = pause_button['text'][0]
    canvas.delete('pause_canvas')
    canvas.delete(txt)
    # 1920x1080
    time.sleep(0.2)
    root.unbind_all(f"<{space}>")
    leaderboard_prompt = Toplevel(root)
    leaderboard_prompt.geometry("250x200+960+540")
    leaderboard_prompt.title("Leaderboard")
    label_1 = Label(leaderboard_prompt, text="Enter username", font=("Times New Roman", 20, "bold"))
    label_1.pack()
    username_entry = Entry(leaderboard_prompt, width=15, bd=10)
    username_entry.insert(10, os.getlogin())
    username_entry.pack()
    submit = Button(leaderboard_prompt, text="Submit", command=lambda: submit_username(username_entry.get()))
    submit.pack()
    leaderboard_prompt.bind_all("<Return>", lambda: on_quit())

    # When prompt window is closed, leaderboard is displayed
    leaderboard_prompt.protocol("WM_DELETE_WINDOW", on_quit)


# When prompt window is closed, leaderboard is displayed
def on_quit():
    global leaderboard, leaderboard_prompt

    leaderboard_display = tkscroll.ScrolledText(bg="#db9160", foreground="#fbff19", font=("Times New Roman", 36, "bold"))
    leaderboard_display.pack()
    canvas.create_window(960, 480, window=leaderboard_display, height=700, width=500)
    leaderboard = sort(leaderboard)
    leaderboard_count = 1
    leaderboard_display.insert(INSERT, "LEADERBOARD\n\n")
    for i in leaderboard:
        leaderboard_display.insert(INSERT, f'{leaderboard_count}: {i[0]}  |   {i[1]}\n')
        leaderboard_count += 1
    leaderboard_prompt.destroy()


def sort(dictionary):
    temp_array = []
    dictionary = sorted(dictionary, key=lambda elem: elem[1], reverse=True)

    return dictionary


def submit_username(u=''):
    global leaderboard
    if u != '':
        leaderboard.append([u, score])
        on_quit()
    else:
        message.showwarning("Not Entered", "Please enter a valid username")


def save_leaderboard():
    close_label = Label(canvas, text="Jungle Run", bg="#b36029", foreground="#fbff19", font=("Times New Roman", 36, "bold"))
    canvas.create_window(1000, 500, window=close_label, height=100, width=400)

    temp_array = []
    for idx in leaderboard:
        temp_array.append(f"{idx[0]}#{idx[1]}")
    for i in temp_array:
        # finds duplicates
        if i in temp_array:
            num = temp_array.count(i)
            for j in range(num-1):
                temp_array.pop(temp_array.index(i))

    file = open(leaderboardfile, "w")
    for line in temp_array:
        file.write(line)
        file.write("\n")
    file.close()
    root.destroy()


canvas = Canvas(width='9000', height='1080')
canvas.pack()
CHARACTER_STATUS = ("idle", "run", "jump", "fall", "pause")
prev_status = None  # Used for pause
# Used in Update subroutine
update_i = 0

# Setting up background & foreground & menu
background = [[], [], [], []]
bg1 = PhotoImage(file="assets/background/bg1.gif").zoom(5)
bg2 = PhotoImage(file="assets/background/bg2.gif").zoom(5)
bg3 = PhotoImage(file="assets/background/bg3.gif").zoom(5)
bg4 = PhotoImage(file="assets/background/bg3.gif").zoom(5)
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
        Button(canvas, text="leaderboard", bg="#b36029", foreground="#fbff19", command=on_quit, font=("helvetica", 25)),
        Button(canvas, text="configure", bg="#b36029", foreground="#fbff19", command=config, font=("helvetica", 25))]
temp = 100
for k in menu:
    canvas.create_window(1000, temp, window=k, height=100, width=400)
    temp += 150

flr = [PhotoImage(file='assets/foreground/floor1.gif').zoom(4) for k in range(7)]
floor = [canvas.create_image((100 + (flr[k].width() * k)), 900, image=flr[k]) for k in range(7)]

# Setting up Character
char_pos = [200, 677]
user_idle = [PhotoImage(file="assets/sprites/idle.gif", format=f"gif -index {k}").zoom(10) for k in range(11)]
user_run = [PhotoImage(file="assets/sprites/run.gif", format=f"gif -index {k}").zoom(10) for k in range(7)]
user_jump = [PhotoImage(file='assets/sprites/jump.png').zoom(10),
             PhotoImage(file='assets/sprites/landing.png').zoom(10)]
for k in range(2):
    user_jump.append(PhotoImage(file="assets/sprites/mid air.gif", format=f"gif -index {k}").zoom(10))

character = canvas.create_image(char_pos[0], char_pos[1], image=user_idle[0])
character_status = CHARACTER_STATUS[0]

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
pause_button = None
user_score = 0
leaderboard_prompt = None

# All keys
keyboard = [chr(i) for i in range(ord('a'), ord('z')+1)]
extra_keys = ["space", "BackSpace", "Up", "Down", "Left", "right",
              "KP_0", "KP_1", "KP_2", "KP_3", "KP_4", "KP_5", "KP_5", "KP_6", "KP_7", "KP_8", "KP_9",
              "KP_Down", "KP_End", "KP_Enter", "KP_Left", "KP_Right", "KP_Up"]

# Setting up controls
space = "space"
canvas.bind_all(f"<{space}>", jump)

# Setting up leaderboard
leaderboardfile = "leaderboard.txt"
try:
    file = open(leaderboardfile, "r")
    leaderboard = []
    for line in file:
        if line != ("" or "\n"):
            line = line.strip()
            user, val = line.split("#")
            leaderboard.append([user, int(val)])
    file.close()
except FileNotFoundError:
    leaderboard = []

label = Label(root)
label.place()
label.pack()


root.protocol("WM_DELETE_WINDOW", save_leaderboard)
root.after(0, update, 0)
root.mainloop()
