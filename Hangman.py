import random
import tkinter as tk
from tkinter import messagebox


class HangmanGame:
    # - Initialize the HangmanGame class.
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("--HANG MAN--")
        self.run = True

        # Get screen dimensions
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()

        # Set window size to a percentage of screen dimensions
        self.window_width = int(self.screen_width * 0.5)
        self.window_height = int(self.screen_height * 0.5)

        # Calculate position x and y coordinates
        self.position_right = int(self.screen_width / 2 - self.window_width / 2)
        self.position_down = int(self.screen_height / 2 - self.window_height / 2)

        self.root.geometry(
            f"{self.window_width}x{self.window_height}+{self.position_right}+{self.position_down}"
        )

        self.setup_game()
        self.root.mainloop()

    # - Initialize game state variables and load the list of words. Set up the game's background and reset the UI.
    def setup_game(self):
        self.score = 0
        self.check_count = 0
        self.win_count = 0
        self.background_color = "#000000"
        self.alpha = list("abcdefghijklmnopqrstuvwxyz")
        self.buttons = []
        self.selected_word = ""

        with open("words.txt", "r") as f:
            self.words_list = f.readlines()

        self.root.config(bg=self.background_color)
        self.reset_ui()

    # - Reset the user interface for a new game. Clear existing widgets and set up new widgets (dashes, buttons, hangman images, exit button, score label).
    def reset_ui(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.selected_word = random.choice(self.words_list).strip()
        self.dashes = [
            tk.Label(
                self.root,
                text="_",
                fg="#ffffff",
                bg="#000000",
                font=("arial", int(self.window_height * 0.05)),
            )
            for _ in self.selected_word
        ]
        for i, dash in enumerate(self.dashes):
            dash.place(
                x=self.window_width * 0.27 + i * self.window_width * 0.05,
                y=self.window_height * 0.65,
            )

        self.btn_images = [tk.PhotoImage(file=f"images/{i}.png") for i in range(26)]
        self.hangman_images = [
            tk.PhotoImage(file=f"images/h{i+1}.png") for i in range(7)
        ]
        self.hangman_labels = [
            tk.Label(self.root, bg="#000000", image=img) for img in self.hangman_images
        ]

        for i in range(26):
            btn = tk.Button(
                self.root,
                bd=0,
                command=lambda i=i: self.check(self.alpha[i], i),
                bg="#000000",
                activebackground="#000000",
                font=10,
                image=self.btn_images[i],
            )
            x = self.window_width * 0.05 * (i % 13)
            y = self.window_height * 0.8 if i < 13 else self.window_height * 0.9
            btn.place(x=x, y=y)
            self.buttons.append(btn)

        self.exit_img = tk.PhotoImage(file="images/exit.png")
        self.exit_label = tk.Button(
            self.root,
            bd=0,
            command=self.close,
            bg="#999999",
            activebackground="#999999",
            font=0,
            image=self.exit_img,
            borderwidth=5,
        )
        self.exit_label.place(x=self.window_width * 0.84, y=self.window_height * 0.02)

        self.score_label = tk.Label(
            self.root,
            text=f"SCORE: {self.score}",
            fg="#ffffff",
            bg="#000000",
            font=("arial", int(self.window_height * 0.035)),
        )
        self.score_label.place(x=self.window_width * 0.01, y=self.window_height * 0.02)

    # - Tell the user to confirm if they want to exit the game. If confirmed, stop the game and close the window.
    def close(self):
        answer = messagebox.askyesno("EXIT", "DO YOU WANT TO EXIT THE GAME ?")
        if answer:
            self.run = False
            self.root.destroy()

    def check(self, letter, button_index):
        button = self.buttons[button_index]
        button.destroy()

        if letter in self.selected_word:
            for i, char in enumerate(self.selected_word):
                if char == letter:
                    self.win_count += 1
                    self.dashes[i].config(text=letter.upper())
            if self.win_count == len(self.selected_word):
                self.score += 2
                answer = messagebox.askyesno(
                    "GAME OVER", "YOU WON!\nWANT TO PLAY AGAIN?"
                )
                self.replay(answer)
        else:
            self.check_count += 1
            if self.check_count < len(self.hangman_labels):
                self.hangman_labels[self.check_count].place(
                    x=self.window_width * 0.33, y=self.window_height * 0.14
                )
            if self.check_count == 6:
                answer = messagebox.askyesno(
                    "GAME OVER",
                    f"ANSWER: {self.selected_word.upper()}\nYOU LOST! WANT TO PLAY AGAIN?",
                )
                self.replay(answer)

    # - Resets the game state and user interface if the user wants to play again. Otherwise, stops the game and closes the window.
    def replay(self, answer):
        if answer:
            self.reset_game_state()
            self.reset_ui()
        else:
            self.run = False
            self.root.destroy()

    # - Resets game state variables for a new game session.
    def reset_game_state(self):
        self.check_count = 0
        self.win_count = 0
        self.buttons = []
        self.hangman_labels = []


if __name__ == "__main__":
    HangmanGame()
