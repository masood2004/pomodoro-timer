import math
from tkinter import *

# ---------------------------- CONSTANTS ------------------------------- #
DARK_GREEN = "#2A9D8F"
LIGHT_GREEN = "#9bdeac"
RED = "#E76F51"
YELLOW = "#E9C46A"
DARK_BLUE = "#264653"
FONT_NAME = "Helvetica"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
reps = 0
timer = None
timer_running = False  # To track if timer is active

# ---------------------------- TIMER RESET ------------------------------- #
def reset_timer():
    global reps, timer, timer_running
    if timer is not None:
        window.after_cancel(timer)
        timer = None
    canvas.itemconfig(timer_text, text="00:00")
    timer_label.config(text="Timer", fg=DARK_GREEN)
    check_label.config(text="")
    reps = 0
    timer_running = False
    start_button.config(state=NORMAL)
    reset_button.config(state=NORMAL)

# ---------------------------- TIMER MECHANISM ------------------------------- #
def start_timer():
    global reps, timer_running
    if timer_running:
        return
    timer_running = True
    start_button.config(state=DISABLED)
    reset_button.config(state=NORMAL)
    reps += 1

    work_sec = WORK_MIN * 60
    short_break_sec = SHORT_BREAK_MIN * 60
    long_break_sec = LONG_BREAK_MIN * 60

    if reps % 8 == 0:
        count_down(long_break_sec)
        timer_label.config(text="Break", fg=RED)
    elif reps % 2 == 0:
        count_down(short_break_sec)
        timer_label.config(text="Break", fg=YELLOW)
    else:
        count_down(work_sec)
        timer_label.config(text="Work", fg=DARK_GREEN)

# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #
def count_down(count):
    global timer, timer_running
    count_min = math.floor(count / 60)
    count_sec = count % 60
    count_sec = f"0{count_sec}" if count_sec < 10 else count_sec

    canvas.itemconfig(timer_text, text=f"{count_min}:{count_sec}")
    if count > 0:
        timer = window.after(1000, count_down, count - 1)
    else:
        timer_running = False
        start_timer()
        marks = "✔" * (reps // 2)
        check_label.config(text=marks, fg=DARK_BLUE)

# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Pomodoro Timer")
window.config(padx=40, pady=30, bg=LIGHT_GREEN)

# Timer Label
timer_label = Label(text="Timer", fg=DARK_GREEN, bg=LIGHT_GREEN,
                    font=(FONT_NAME, 35, "bold"))
timer_label.grid(column=1, row=0, pady=20)

# Canvas
canvas = Canvas(width=220, height=224, bg=LIGHT_GREEN, highlightthickness=0)
tomato_img = PhotoImage(file="images/tomato.png")
canvas.create_image(110, 112, image=tomato_img)
timer_text = canvas.create_text(110, 135, text="00:00", fill="white",
                   font=(FONT_NAME, 30, "bold"))
canvas.grid(column=1, row=1, pady=20)

# Buttons
button_style = {
    "font": (FONT_NAME, 14, "bold"),
    "borderwidth": 0,
    "highlightthickness": 0,
    "padx": 20,
    "pady": 10
}

start_button = Button(text="Start", command=start_timer,
                     bg=DARK_GREEN, fg="white", activebackground=DARK_GREEN,
                     **button_style)
start_button.grid(column=0, row=2, padx=10)

reset_button = Button(text="Reset", command=reset_timer,
                     bg=RED, fg="white", activebackground=RED,
                     **button_style)
reset_button.grid(column=2, row=2, padx=10)

# Check Marks
check_label = Label(bg=LIGHT_GREEN, fg=DARK_BLUE,
                   font=(FONT_NAME, 18, "bold"))
check_label.grid(column=1, row=3, pady=20)

window.mainloop()