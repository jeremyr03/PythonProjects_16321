from tkinter import *
import tkinter.scrolledtext as tkscroll
import tkinter.messagebox as message
import time
import random
import os
import webbrowser
import os.path
# 1920x1080


def update(ind):
    global character_status, update_i
    # Animation if character is running
    if character_status == CHARACTER_STATUS[1]:
        ind += 1
        if not (ind < 7):
            ind = 0
        canvas.itemconfig(character, image=user_run[ind])

    # Animation if character is idle
    elif character_status == CHARACTER_STATUS[0]:
        ind += 1
        if ind == 11:
            ind = 0
        canvas.itemconfig(character, image=user_idle[ind])

    # Animation if character is jumping
    elif character_status == CHARACTER_STATUS[2]:
        # If cheat code 2 is active, character will be paused in the air
        if not cheat_code2_active:
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

    # If character paused, character is stationary
    elif character_status == CHARACTER_STATUS[4]:
        pass

    root.after(70, update, ind)


def save():
    global character_status, file, line
    # if there exists a file of saved data, make sure not to overwrite it
    if os.path.isfile("SaveData.txt"):
        answ = message.askyesno(title="Save File exists",
                                message="A saved file already exists. Do you wish to overwrite file?")
        if answ:
            file = open("SaveData.txt", "w")
            line = f"{score}"
            file.writelines(line)
            file.close()
            character_status = CHARACTER_STATUS[5]
            message.showinfo(title="return to title", message="Returning to title screen")
            root.after(100, setup_canvas)

    # If there is no save data, save score to .txt then send back to main menu
    else:
        file = open("SaveData.txt", "w")
        line = f"{score}"
        file.writelines(line)
        file.close()
        character_status = CHARACTER_STATUS[5]
        message.showinfo(title="return to title", message="Returning to title screen")
        root.after(100, setup_canvas)


def go():
    global character_status, txt, pause_button, bosskey
    # Destroy menu
    for i in menu:
        i.destroy()
    character_status = CHARACTER_STATUS[1]
    pos = canvas.coords(character)
    # Run character to the centre of the screen
    if pos[0] < 900:
        canvas.move(character, 10, 0)
        root.after(30, go)
        pos = canvas.coords(character)
    bg()
    floor_move()
    start()
    # Implement pause button
    pause_button = Button(canvas, text="| |", command=pause_command, bg="#db9160", foreground="#fbff19",
                          font=("Times New Roman", 36, "bold"))
    pause = canvas.create_window(1870, 50, window=pause_button, height=100, width=100, tag="pause_canvas")
    canvas.tag_raise(pause)

    root.after(2500, obstacles)


def pause_command():
    global character_status, prev_status, pause_button, save_game
    prev_status = character_status
    character_status = CHARACTER_STATUS[4]
    pause_button['text'] = "▶"
    pause_button['command'] = play
    save_game_button = Button(canvas, text="Save Game", command=save)
    save_game = canvas.create_window(1620, 50, window=save_game_button, height=100, width=400)


def play():
    global character_status
    character_status = prev_status
    pause_button['text'] = "| |"
    pause_button['command'] = pause_command
    canvas.delete(save_game)


def start():
    global score, old, txt
    if (character_status != CHARACTER_STATUS[4]) and (character_status != CHARACTER_STATUS[5]):
        # Calculate new time to avoid the score being updated to frequently
        new = time.time()
        if (new - old) >= 1:
            try:
                canvas.delete(txt)
            except:
                pass
            score += 1
            old = new
            # Update score on screen
            txt = canvas.create_text(1000, 100, text=f"{score} seconds", fill="#fbff19",
                                     font=("Times New Roman", 36, "bold"))

    if character_status != CHARACTER_STATUS[5]:
        root.after(500, start)


def save_key(k):
    global space
    # Update jump key
    canvas.unbind_all(f"<{space}>")
    space = k
    canvas.bind_all(f"<{space}>", jump)


def config(event=None):
    global space, option
    for i in menu:
        i.destroy()

    canvas1 = Canvas(canvas)
    canvas.create_window(1000, 500, window=canvas1)
    spaces = StringVar(canvas1)
    spaces.set(extra_keys[0])
    label1 = Label(canvas1, text="Jump:", font=("Times New Roman", 20, "bold"))
    label1.grid(row=0, column=0)
    emptylabel = Label(canvas1)
    emptylabel.grid(row=1)
    # Drop down menu to change the button for jumping
    option = OptionMenu(canvas1, spaces, *(keyboard + extra_keys))
    option.config(font=("Times New Roman", 20, "italic"))
    option.grid(row=0, column=1)
    # Button to save key choice
    save_change = Button(canvas1, text="save", command=lambda: save_key(spaces.get()), font=("Times New Roman", 20))
    save_change.grid(row=2, column=0)
    # Go back to main menu
    menu_button = Button(canvas1, text="Menu", command=lambda: setup_canvas(), font=("Times New Roman", 20))
    menu_button.grid(row=2, column=1)


def bg():
    global background
    # Move background
    if character_status != CHARACTER_STATUS[4]:
        for i in background:
            for j in i:
                canvas.move(j, -0.75, 0)
                if canvas.coords(j)[0] <= (960 - 1920):
                    canvas.coords(j, (960 + int(1920 / 2)), 400)

    if character_status != CHARACTER_STATUS[5]:
        root.after(500, bg)


def floor_move():
    global floor
    # Move floor
    if character_status != CHARACTER_STATUS[4]:
        for i in floor:
            canvas.move(i, -2, 0)
            if canvas.coords(i)[0] <= (100 - 640):
                canvas.coords(i, (100 + ((640 / 2) * 7)), 900)

    if character_status != CHARACTER_STATUS[5]:
        root.after(500, floor_move)


def jump(event=None):
    global character_status
    if character_status == CHARACTER_STATUS[1]:
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
    global character_status, animals_i

    if character_status != CHARACTER_STATUS[4]:
        # For non-animated obstacles
        for i in obstacle:
            canvas.move(i, -1.5, 0)
            # If cheat code is active, the arrow will pass through the user (not for bird though)
            if not cheat_code1_active:
                # Checks overlapping when close to the character
                if 500 < canvas.coords(i)[0] < 1500:
                    if (overlapping(character, i)) and (character_status != CHARACTER_STATUS[5]):
                        character_status = CHARACTER_STATUS[5]
                        end()
                        break
            # If too left, move far right to head back onto the stage
            if canvas.coords(i)[0] < -400:
                canvas.move(i, 100000, 0)

        # For animated obstacles
        for i in animals:
            canvas.move(i, -1.5, 0)
            canvas.itemconfig(i, image=bird[(int(animals_i) % 2)])
            animals_i += 0.005
            # Checks overlapping when close to the character
            if 500 < canvas.coords(i)[0] < 1500:
                if (overlapping(character, i)) and (character_status != CHARACTER_STATUS[5]):
                    character_status = CHARACTER_STATUS[5]
                    end()
                    break
            # If too left, move far right to head back onto the stage
            if canvas.coords(i)[0] < -400:
                canvas.move(i, 100000, 0)

    # Loops if character not dead
    if character_status != CHARACTER_STATUS[5]:
        root.after(200, obstacles)


def end():
    global character_status, user_score, leaderboard_prompt
    # Initiate dead sequence for other loops
    character_status = CHARACTER_STATUS[5]

    user_score = pause_button['text'][0]
    canvas.delete('pause_canvas')
    canvas.delete(txt)
    # 1920x1080
    root.unbind_all(f"<{space}>")
    # Ask for prompt to enter the user's username (OS Login entered as default)
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

    # Try to close menu, if menu not created, try...except... will catch the error
    try:
        for i in menu:
            i.destroy()
    except:
        pass
    # If leaderboard was not displayed, try...except... will catch the error
    try:
        leaderboard_prompt.destroy()
    except:
        pass

    # Display leaderboard with Scroll bar
    leaderboard_display = tkscroll.ScrolledText(bg="#db9160", foreground="#fbff19", font=("Times New Roman", 36, "bold"))
    leaderboard_display.pack()
    canvas.create_window(960, 480, window=leaderboard_display, height=700, width=500)
    leaderboard = sort(leaderboard)
    leaderboard_count = 1
    leaderboard_display.insert(INSERT, "LEADERBOARD\n\n")
    leaderboard_display.tag_configure('tag-center', justify='center')
    leaderboard_display.tag_configure('tag-left', justify='left')
    leaderboard_display.tag_configure('tag-right', justify='right')

    for i in leaderboard:
        leaderboard_display.insert(INSERT, f'{leaderboard_count}: {i[0]}\n', 'tag-left')
        leaderboard_display.insert(INSERT, f' {i[1]}\n', 'tag-right')
        leaderboard_count += 1
    # Disable user from editing text in the leaderboard
    leaderboard_display.config(state=DISABLED)
    main_menu_button = Button(canvas, text="Main Menu", command=lambda: setup_canvas())
    canvas.create_window(1160, 119, window=main_menu_button)


def sort(dictionary):
    temp_array = []
    # Sorts leaderboard by score best to worst
    dictionary = sorted(dictionary, key=lambda elem: elem[1], reverse=True)

    return dictionary


def submit_username(u=''):
    global leaderboard
    # Validation for Username
    if u != '':
        leaderboard.append([u, score])
        on_quit()
    else:
        message.showwarning("Not Entered", "Please enter a valid username")


def save_leaderboard():
    # When program is about to be closed \
    # (with red window button) this procedure is called to save everything to the leaderboard
    close_label = Label(canvas, text="Jungle Run", bg="#b36029", foreground="#fbff19",
                        font=("Times New Roman", 36, "bold"))
    canvas.create_window(1000, 500, window=close_label, height=100, width=400)

    # Searches for duplicate entries and ensures only 1 is saved to the .txt
    temp_array = []
    for idx in leaderboard:
        temp_array.append(f"{idx[0]}#{idx[1]}")
    for i in temp_array:
        # finds duplicates
        if i in temp_array:
            num = temp_array.count(i)
            for j in range(num-1):
                temp_array.pop(temp_array.index(i))

    # Save to .txt
    file = open(leaderboardfile, "w")
    for line in temp_array:
        file.write(line)
        file.write("\n")
    file.close()
    root.destroy()


def main_menu(to_del):
    # Creates main menu
    canvas.delete(to_del)
    i = 100
    for k in menu:
        k.pack()
        canvas.create_window(1000, i, window=k, height=100, width=400)
        i += 150


def load():
    global score
    # Loads previously saved data if there is any
    if os.path.isfile("SaveData.txt"):
        file = open("SaveData.txt", "r")
        line = file.readline()
        score = int(line.strip())
        file.close()
        go()
    # Otherwise it will produce an error box telling the user that there is no Save Data found
    else:
        message.showwarning(title="FileNotFound", message="Save Data not found")


def setup_canvas():
    global character, character_status, canvas, floor, obstacle, space, menu, score, animals, update_i

    # Reset jump value
    update_i = 0

    # Start canvas from scratch
    canvas.destroy()
    canvas = Canvas(width='9000', height='1080')
    canvas.pack()

    # Setup background
    background[0].append(canvas.create_image(960, 400, image=bg1))
    background[0].append(canvas.create_image(960, 400, image=bg2))
    background[0].append(canvas.create_image(960, 400, image=bg3))
    background[0].append(canvas.create_image(960, 400, image=bg4))
    background[1].append(canvas.create_image(canvas.coords(background[0][0])[0] + bg1.width()-1, 400, image=bg1))
    background[1].append(canvas.create_image(canvas.coords(background[0][1])[0] + bg2.width()-1, 400, image=bg2))
    background[1].append(canvas.create_image(canvas.coords(background[0][2])[0] + bg3.width()-1, 400, image=bg3))
    background[1].append(canvas.create_image(canvas.coords(background[0][3])[0] + bg4.width()-1, 400, image=bg4))
    background[2].append(canvas.create_image(canvas.coords(background[1][0])[0] + bg1.width()-1, 400, image=bg1))
    background[2].append(canvas.create_image(canvas.coords(background[1][1])[0] + bg2.width()-1, 400, image=bg2))
    background[2].append(canvas.create_image(canvas.coords(background[1][2])[0] + bg3.width()-1, 400, image=bg3))
    background[2].append(canvas.create_image(canvas.coords(background[1][3])[0] + bg4.width()-1, 400, image=bg4))
    background[3].append(canvas.create_image(canvas.coords(background[2][0])[0] + bg1.width()-1, 400, image=bg1))
    background[3].append(canvas.create_image(canvas.coords(background[2][1])[0] + bg2.width()-1, 400, image=bg2))
    background[3].append(canvas.create_image(canvas.coords(background[2][2])[0] + bg3.width()-1, 400, image=bg3))
    background[3].append(canvas.create_image(canvas.coords(background[2][3])[0] + bg4.width()-1, 400, image=bg4))

    # Setup menu
    menu = [Label(canvas, text="Jungle Run", bg="#b36029", foreground="#fbff19",
                  font=("Times New Roman", 36, "bold")),
            Button(canvas, text="start", bg="#b36029", foreground="#fbff19", command=go,
                   font=("helvetica", 25)),
            Button(canvas, text="load", bg="#b36029", foreground="#fbff19", command=load,
                   font=("helvetica", 25)),
            Button(canvas, text="leaderboard", bg="#b36029", foreground="#fbff19", command=on_quit,
                   font=("helvetica", 25)),
            Button(canvas, text="configure", bg="#b36029", foreground="#fbff19", command=config,
                   font=("helvetica", 25))]
    i = 150
    for k in menu:
        k.pack()
        canvas.create_window(1000, i, window=k, height=100, width=400)
        i += 120

    # Setup floor
    floor = [canvas.create_image((100 + (flr[k].width() * k)), 900, image=flr[k]) for k in range(7)]

    # Setup character
    character = canvas.create_image(CHAR_POS[0], CHAR_POS[1], image=user_idle[0])
    character_status = CHARACTER_STATUS[0]
    canvas.itemconfig(character, image=user_idle[0])

    # Setup obstacles
    obstacle = []
    animals = []
    temp = 2000

    # Choose between arrow and bird, with arrow weighted to be more common
    for k in random.choices(obstacle_items, [9, 4], k=50):
        if k == bird:
            animals.append(canvas.create_image(temp, 700, image=bird[0]))
        else:
            obstacle.append(canvas.create_image(temp, 700, image=k))
        temp += random.randint(1000, 2000)

    # Setting up controls
    canvas.bind_all(f"<{space}>", jump)

    # Setting up score
    score = 0


# If Shift-L is pressed, cheat code 1 is activated
def cheat1(event=None):
    global cheat_code1_active
    if not cheat_code1_active:
        cheat_code1_active = True
    else:
        cheat_code1_active = False
    print(f"Cheat code {cheat_code1_active}")


# If Caps-Lock is pressed, cheat code 2 is activated
def cheat2(event=None):
    global cheat_code2_active
    if cheat_code2_active:
        cheat_code2_active = False
    else:
        cheat_code2_active = True
    print(f"Cheat code {cheat_code2_active}")


# If Backspace is pressed, 10 points added to score
def cheat3(event=None):
    global score
    print("10 points added")
    score += 10


# Opens a webpage to hide the game
def boss_key(event=None):
    global character_status, prev_status, bosskey_label
    print("boss key activated")

    if character_status == CHARACTER_STATUS[4]:
        try:
            canvas.delete(bosskey_label)
        except:
            pass
        character_status = prev_status
    else:
        prev_status = character_status
        close_label = Label(canvas, text="Boss Key Activated", bg="#000000", foreground="#ffffff",
                            font=("Times New Roman", 36, "bold"))
        bosskey_label = canvas.create_window(1000, 500, window=close_label, height=100, width=400)
        character_status = CHARACTER_STATUS[4]
        root.after(1000, lambda: webbrowser.open('https://www.cs.manchester.ac.uk/'))


# Declaring variables that will be used in future subroutines
character_status = None
floor = None
menu = None
character = None  # Will be used in main_menu
prev_status = None  # Used for pause
update_i = 0  # Used in Update subroutine
animals_i = 0  # Used to animate birds
option = None
cheat_code1_active = False  # Arrows pass through you with no problem (not birds though)
cheat_code2_active = False  # Pauses the jump (allowing character to float in midair); resumes once key pressed again
bosskey = True  # When bosskey is False, it cannot be used ( first 5 seconds of the game being started, it is False)

# Setting up Main Window (root)
root = Tk()
geometry = '1920x1080'
root.geometry(geometry)
# Setting up canvas
canvas = Canvas(width='9000', height='1080')
canvas.pack()

# Setup Character
# https://jesse-m.itch.io/jungle-pack
# CHARACTER_STATUS is used to define statuses of the character that breaks loops, run empty loops etc.
CHARACTER_STATUS = ("idle", "run", "jump", "fall", "pause", "dead")
CHAR_POS = [200, 677]
user_idle = [PhotoImage(file="assets/sprites/idle.gif", format=f"gif -index {k}").zoom(10) for k in range(11)]
user_run = [PhotoImage(file="assets/sprites/run.gif", format=f"gif -index {k}").zoom(10) for k in range(7)]
user_jump = [PhotoImage(file='assets/sprites/jump.png').zoom(10),
             PhotoImage(file='assets/sprites/landing.png').zoom(10)]

# Setting up background & foreground & menu
# https://jesse-m.itch.io/jungle-pack
background = [[], [], [], []]
bg1 = PhotoImage(file="assets/background/bg1.gif").zoom(5)
bg2 = PhotoImage(file="assets/background/bg2.gif").zoom(5)
bg3 = PhotoImage(file="assets/background/bg3.gif").zoom(5)
bg4 = PhotoImage(file="assets/background/bg3.gif").zoom(5)
flr = [PhotoImage(file='assets/foreground/floor1.gif').zoom(4) for k in range(7)]
for x in range(2):
    user_jump.append(PhotoImage(file="assets/sprites/mid air.gif", format=f"gif -index {x}").zoom(10))

# Setting up obstacles
# https://opengameart.org/content/pixel-art-colorful-flying-2-frames
bird = [PhotoImage(file="assets/bird.gif", format=f"gif -index {k}").zoom(2) for k in range(2)]
# https://kenam0.itch.io/arrows-pack
obstacle_items = [PhotoImage(file="assets/arrow.gif"), bird]
obstacle = []  # Used in subroutine
animals = []
# temp = 2000
# for k in random.choices(obstacle_items, [1], k=50):
#     obstacle.append(canvas.create_image(temp, 700, image=k))
#     temp += random.randint(1000, 2000)

# Setting up Score
score = 0
old = time.time()
txt = None
pause_button = None
user_score = 0
leaderboard_prompt = None

# Define keys
keyboard = [chr(i) for i in range(ord('a'), ord('z')+1)]
extra_keys = ["space", "Up", "Down", "Left", "right",
              "KP_0", "KP_1", "KP_2", "KP_3", "KP_4", "KP_5", "KP_5", "KP_6", "KP_7", "KP_8", "KP_9",
              "KP_Down", "KP_End", "KP_Enter", "KP_Left", "KP_Right", "KP_Up"]
# Setting up original control
space = "space"
# cheat_codes
canvas.bind_all("<Shift_L>", cheat1)
canvas.bind_all("<Caps_Lock>", cheat2)
canvas.bind_all("<BackSpace>", cheat3)
canvas.bind_all("<Alt-b>", boss_key)

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

# Initiate setting up of canvas
setup_canvas()

# When root is closed (with red button on window), instead of shutting dow, save_leaderboard() is called
root.protocol("WM_DELETE_WINDOW", save_leaderboard)
root.after(0, update, 0)
root.mainloop()
