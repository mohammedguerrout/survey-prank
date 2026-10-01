"""The "Are you stupid?" survey where the honest answer is impossible to click."""
import random
import tkinter as tk
from tkinter import messagebox

WIDTH, HEIGHT = 600, 600
SAFE_DISTANCE = 120  # the "no" button never lands closer than this to the mouse
TAUNTS = [
    "Too slow!",
    "Nice try.",
    "Missed me!",
    "Over here!",
    "Are you even trying?",
    "Wrong button, genius.",
    "I'm faster than you.",
]


def overlaps(a, b, margin=20):
    """a and b are (x, y, width, height) rectangles."""
    ax, ay, aw, ah = a
    bx, by, bw, bh = b
    return not (ax + aw + margin < bx or bx + bw + margin < ax
                or ay + ah + margin < by or by + bh + margin < ay)


class Survey(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Survey")
        self.geometry(f"{WIDTH}x{HEIGHT}")
        self.resizable(False, False)
        self.configure(bg="white")
        self.dodges = 0

        tk.Label(self, text="Are you stupid?", font=("Arial", 20, "bold"),
                 bg="white").pack(pady=(20, 5))
        self.status = tk.Label(self, text="", font=("Arial", 12), bg="white", fg="gray")
        self.status.pack()

        self.no_button = tk.Button(self, text="no", font=("Arial", 20, "bold"))
        self.no_button.place(x=170, y=150)
        self.yes_button = tk.Button(self, text="yes", font=("Arial", 20, "bold"),
                                    command=self.accept)
        self.yes_button.place(x=350, y=150)

        # Dodge on hover, on click AND on keyboard focus, so Tab + Space cannot cheat.
        for event in ("<Enter>", "<FocusIn>", "<Button-1>"):
            self.no_button.bind(event, self.dodge)

        # Closing the window is not an escape either.
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def dodge(self, _event=None):
        self.update_idletasks()
        width, height = self.no_button.winfo_reqwidth(), self.no_button.winfo_reqheight()
        yes_box = (self.yes_button.winfo_x(), self.yes_button.winfo_y(),
                   self.yes_button.winfo_reqwidth(), self.yes_button.winfo_reqheight())
        mouse_x = self.winfo_pointerx() - self.winfo_rootx()
        mouse_y = self.winfo_pointery() - self.winfo_rooty()

        x, y = 0, 100
        for _ in range(100):  # try random spots until one is far from the mouse and the "yes" button
            x = random.randint(0, WIDTH - width)
            y = random.randint(80, HEIGHT - height)
            far_from_mouse = ((x + width / 2 - mouse_x) ** 2 + (y + height / 2 - mouse_y) ** 2
                              > SAFE_DISTANCE ** 2)
            if far_from_mouse and not overlaps((x, y, width, height), yes_box):
                break
        self.no_button.place(x=x, y=y)

        self.dodges += 1
        self.status.config(text=f"{random.choice(TAUNTS)}   (escapes: {self.dodges})")
        return "break"  # cancel the normal click handling

    def accept(self):
        messagebox.showinfo(" ", f"Thanks bro\n\n(the 'no' button escaped {self.dodges} times)")
        self.destroy()

    def on_close(self):
        messagebox.showinfo("Nice try", "You can't leave without answering the survey!")


if __name__ == "__main__":
    Survey().mainloop()