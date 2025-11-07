import tkinter as tk
from tkinter import font
import random

# -----------------------------
# PROFESSIONAL LIGHT COLOR THEME
# -----------------------------
THEME = {
    "bg": "#E8F6F3",       # light teal background
    "button_bg": "#A2D9CE", # light greenish buttons
    "hover": "#76D7C4",
    "text": "#1C2833"
}

# -----------------------------
# AI LOGIC (Unbeatable)
# -----------------------------
def check_winner(board, symbol):
    wins = [
        [0,1,2],[3,4,5],[6,7,8],
        [0,3,6],[1,4,7],[2,5,8],
        [0,4,8],[2,4,6]
    ]
    return any(all(board[i] == symbol for i in w) for w in wins)

def minimax(board, is_max, ai_symbol, player_symbol, depth=0):
    if check_winner(board, ai_symbol):
        return 10 - depth
    if check_winner(board, player_symbol):
        return depth - 10
    if "" not in board:
        return 0

    empty = [i for i, x in enumerate(board) if x == ""]

    if is_max:
        best = -float('inf')
        for i in empty:
            board[i] = ai_symbol
            score = minimax(board, False, ai_symbol, player_symbol, depth + 1)
            board[i] = ""
            best = max(best, score)
        return best
    else:
        best = float('inf')
        for i in empty:
            board[i] = player_symbol
            score = minimax(board, True, ai_symbol, player_symbol, depth + 1)
            board[i] = ""
            best = min(best, score)
        return best

def ai_move(board, ai_symbol, player_symbol):
    empty = [i for i, x in enumerate(board) if x == ""]
    best_score, move = -float('inf'), None
    for i in empty:
        board[i] = ai_symbol
        score = minimax(board, False, ai_symbol, player_symbol)
        board[i] = ""
        if score > best_score:
            best_score = score
            move = i
    return move

# -----------------------------
# CUSTOM POPUP FUNCTION
# -----------------------------
def show_popup(root, title, message, emoji=""):
    popup = tk.Toplevel(root)
    popup.title(title)
    popup.configure(bg="#D1F2EB")  # light background
    popup.geometry("400x200")
    popup.resizable(False, False)

    # center popup
    popup.update_idletasks()
    x = (popup.winfo_screenwidth() - popup.winfo_width()) // 2
    y = (popup.winfo_screenheight() - popup.winfo_height()) // 2
    popup.geometry(f"+{x}+{y}")

    label_font = ("Helvetica", 20, "bold")
    tk.Label(popup, text=message, font=label_font, bg="#D1F2EB", fg="#1C2833").pack(expand=True)

    tk.Button(popup, text="OK", font=("Helvetica", 14, "bold"),
              command=popup.destroy, bg="#A2D9CE", fg="#1C2833", activebackground="#76D7C4").pack(pady=10)

# -----------------------------
# GUI CLASS
# -----------------------------
class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Tic-Tac-Toe (Professional Edition)")
        self.root.geometry("460x600")
        self.root.resizable(False, False)

        # center main window
        self.center_window()

        self.player_symbol = "X"
        self.ai_symbol = "O"
        self.board = [""] * 9
        self.scores = {"Player": 0, "AI": 0, "Draw": 0}

        self.create_ui()
        self.update_theme()

    def center_window(self):
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() - width) // 2
        y = (self.root.winfo_screenheight() - height) // 2
        self.root.geometry(f"+{x}+{y}")

    def create_ui(self):
        self.main_frame = tk.Frame(self.root, padx=12, pady=12)
        self.main_frame.pack(fill="both", expand=True)

        # Symbol Selection
        control_frame = tk.Frame(self.main_frame, bg=THEME["bg"])
        control_frame.pack(pady=10)

        label_font = ("Helvetica", 16, "bold")
        radio_font = ("Helvetica", 14, "bold")

        tk.Label(control_frame, text="Symbol:", font=label_font, bg=THEME["bg"], fg=THEME["text"]).grid(row=0, column=0, padx=10)
        self.symbol_var = tk.StringVar(value="X")
        tk.Radiobutton(control_frame, text="X", variable=self.symbol_var, value="X",
                       font=radio_font, padx=10, pady=5, bg="#A2D9CE", fg="#1C2833",
                       activebackground="#76D7C4", command=self.choose_symbol).grid(row=0, column=1)
        tk.Radiobutton(control_frame, text="O", variable=self.symbol_var, value="O",
                       font=radio_font, padx=10, pady=5, bg="#A2D9CE", fg="#1C2833",
                       activebackground="#76D7C4", command=self.choose_symbol).grid(row=0, column=2)

        # Scoreboard
        self.score_label = tk.Label(self.main_frame, text=self.get_score_text(), font=("Helvetica", 14), bg=THEME["bg"], fg=THEME["text"])
        self.score_label.pack(pady=8)

        # Board Frame
        board_frame = tk.Frame(self.main_frame, height=420, width=380)
        board_frame.pack_propagate(False)
        board_frame.pack(pady=15)

        for r in range(4):
            board_frame.rowconfigure(r, weight=1)
        for c in range(3):
            board_frame.columnconfigure(c, weight=1)

        # Board Buttons
        self.buttons = []
        for i in range(3):
            for j in range(3):
                idx = i * 3 + j
                btn = tk.Button(board_frame, text="", font=("Helvetica", 28),
                                width=4, height=2,
                                command=lambda idx=idx: self.user_click(idx))
                btn.grid(row=i, column=j, padx=5, pady=5, sticky="nsew")
                btn.bind("<Enter>", lambda e, b=btn: b.config(bg=THEME["hover"]))
                btn.bind("<Leave>", lambda e, b=btn: b.config(bg=THEME["button_bg"]))
                self.buttons.append(btn)

        # Restart Button
        self.restart_btn = tk.Button(board_frame, text="Restart Game", font=("Helvetica", 14, "bold"),
                                     width=18, height=1, command=self.restart_game)
        self.restart_btn.grid(row=3, column=0, columnspan=3, pady=10, sticky="nsew")

    def choose_symbol(self):
        self.player_symbol = self.symbol_var.get()
        self.ai_symbol = "O" if self.player_symbol == "X" else "X"

    def update_theme(self):
        self.root.config(bg=THEME["bg"])
        self.main_frame.config(bg=THEME["bg"])
        self.button_bg = THEME["button_bg"]
        self.hover_bg = THEME["hover"]
        self.text_color = THEME["text"]

        self.score_label.config(bg=THEME["bg"], fg=self.text_color)
        self.restart_btn.config(bg=self.button_bg, fg=self.text_color, activebackground=self.hover_bg)
        for btn in self.buttons:
            btn.config(bg=self.button_bg, fg=self.text_color)

    def get_score_text(self):
        return f"Player: {self.scores['Player']}  |  AI: {self.scores['AI']}  |  Draw: {self.scores['Draw']}"

    def user_click(self, idx):
        if self.board[idx] == "":
            self.board[idx] = self.player_symbol
            self.buttons[idx].config(text=self.player_symbol, fg=self.text_color)
            if check_winner(self.board, self.player_symbol):
                show_popup(self.root, "Game Over", "You Win!")
                self.scores["Player"] += 1
                self.update_scores()
                return
            elif "" not in self.board:
                show_popup(self.root, "Game Over", "Draw!")
                self.scores["Draw"] += 1
                self.update_scores()
                return
            self.root.after(300, self.ai_turn)

    def ai_turn(self):
        idx = ai_move(self.board, self.ai_symbol, self.player_symbol)
        self.board[idx] = self.ai_symbol
        self.animate_button(self.buttons[idx], self.ai_symbol)
        if check_winner(self.board, self.ai_symbol):
            show_popup(self.root, "Game Over", "AI Wins!")
            self.scores["AI"] += 1
            self.update_scores()
        elif "" not in self.board:
            show_popup(self.root, "Game Over", "Draw!")
            self.scores["Draw"] += 1
            self.update_scores()

    def animate_button(self, button, symbol):
        colors = ["#76D7C4", "#A2D9CE", "#76D7C4"]
        def step(i=0):
            if i < len(colors):
                button.config(bg=colors[i], text=symbol)
                self.root.after(100, lambda: step(i+1))
        step()

    def update_scores(self):
        self.score_label.config(text=self.get_score_text())
        self.restart_game()

    def restart_game(self):
        self.board = [""] * 9
        for btn in self.buttons:
            btn.config(text="", bg=self.button_bg)

# -----------------------------
# Run Application
# -----------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = TicTacToe(root)
    root.mainloop()
