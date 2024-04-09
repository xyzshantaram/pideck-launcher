import ttkbootstrap as ttk
from ttkbootstrap.constants import INFO, OUTLINE
import subprocess
from tkinter import Frame

root = ttk.Window(size=(480, 320))
root.style.configure(".", font=("Liberation Mono", 24))

btn_frame = ttk.Frame(root)

btn_frame.rowconfigure(0, weight=1)
btn_frame.columnconfigure(0, weight=1)
btn_frame.rowconfigure(1, weight=1)
btn_frame.columnconfigure(1, weight=1)

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)


class LauncherItem:
    def __init__(self, root, label, icon, pos, command):
        self.icon = icon
        self.pos = pos
        self.label = label
        self.btn = ttk.Button(root, text=f"{icon} {label}", bootstyle=(INFO))
        self.btn.grid(row=pos[0], column=pos[1], padx=5, pady=5, sticky="wens")
        self.command = command


btns = [
    [
        LauncherItem(btn_frame, "Code", "📝", (0, 0), "launch-python3"),
        LauncherItem(btn_frame, "Quizzes", "💯", (0, 1), "launch-quizapp"),
        LauncherItem(btn_frame, "Chat", "💬", (0, 2), "launch-irc"),
    ],
    [
        LauncherItem(btn_frame, "Calc", "🖩", (1, 0), "launch-octave"),
        LauncherItem(btn_frame, "Music", "🎵", (1, 1), "launch-music"),
        LauncherItem(btn_frame, "Exit", "❌", (1, 2), "exit"),
    ],
]

in_menu = False


def show_menu():
    global in_menu
    in_menu = True
    btn_frame.grid(row=0, column=0, sticky="wens")
    btn_frame.focus_set()


def hide_menu():
    global in_menu
    in_menu = False
    btn_frame.grid_forget()


show_menu()

last_tframe = None


def launch_app(cmd):
    global root, last_tframe
    termf = Frame(root, height=200, width=480)
    last_tframe = termf
    hide_menu()
    termf.grid(row=0, column=0, sticky="wens")
    termf.focus_set()
    args = cmd if isinstance(cmd, list) else [cmd]
    subprocess.run(["xterm", "-geometry", "80x24", "-e", *args])
    termf.grid_forget()
    show_menu()


def handle(item):
    print("handle() called with item", item)
    match item.command:
        case "launch-python3":
            launch_app("python3")
        case "launch-quizapp":
            pass
        case "launch-irc":
            launch_app("weechat")
        case "launch-octave":
            launch_app("octave")
        case "launch-music":
            launch_app(["kew", "all"])
        case "exit":
            exit(0)


def clamp(val, min, max):
    if val <= min:
        return min

    if val >= max:
        return max

    return val


cursor_row = 0
cursor_col = 0


def on_key_release(evt):
    print(evt)
    global cursor_row, cursor_col
    if evt.keysym in ["Up", "Left", "Down", "Right"]:
        if not in_menu:
            return
        btns[cursor_row][cursor_col].btn.configure(bootstyle=(INFO))
        if evt.keysym == "Down":
            cursor_row += 1
        elif evt.keysym == "Up":
            cursor_row -= 1
        elif evt.keysym == "Right":
            if cursor_col == 2:
                cursor_col = 0
                if cursor_row == 1:
                    cursor_row = 0
                else:
                    cursor_row += 1
            else:
                cursor_col += 1
        elif evt.keysym == "Left":
            if cursor_col == 0:
                cursor_col = 2
                if cursor_row == 0:
                    cursor_row = 1
                else:
                    cursor_row -= 1
            else:
                cursor_col -= 1

        cursor_row = clamp(cursor_row, 0, 1)
        cursor_col = clamp(cursor_col, 0, 2)
        btns[cursor_row][cursor_col].btn.configure(bootstyle=(INFO, OUTLINE))
    elif evt.keysym in ["space"]:
        if not in_menu:
            return
        else:
            handle(btns[cursor_row][cursor_col])
    elif evt.keysym == "Escape":
        print("esc")
    else:
        print(evt.keysym)


root.bind("<KeyRelease>", on_key_release)
# root.bind("<KeyPress>", on_key_press)

root.mainloop()
