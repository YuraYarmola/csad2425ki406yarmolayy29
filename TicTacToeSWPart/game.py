import tkinter as tk
from tkinter import messagebox

root = tk.Tk()
root.title("Tic-Tac-Toe")

current_player = "X"
buttons = []


def check_win():
    winning_combinations = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),  # Rows
        (0, 3, 6), (1, 4, 7), (2, 5, 8),  # Columns
        (0, 4, 8), (2, 4, 6)  # Diagonals
    ]

    for a, b, c in winning_combinations:
        if buttons[a]["text"] == buttons[b]["text"] == buttons[c]["text"] != " ":
            return True
    return False


def check_draw():
    for button in buttons:
        if button["text"] == " ":
            return False
    return True


def on_button_click(index):
    global current_player

    if buttons[index]["text"] == " ":
        buttons[index]["text"] = current_player
        if check_win():
            messagebox.showinfo("Tic-Tac-Toe", f"Player {current_player} wins!")
            reset_game()
        elif check_draw():
            messagebox.showinfo("Tic-Tac-Toe", "It's a draw!")
            reset_game()
        else:
            current_player = "O" if current_player == "X" else "X"
    else:
        messagebox.showwarning("Tic-Tac-Toe", "Invalid move! Try again.")


def reset_game():
    global current_player
    current_player = "X"
    for button in buttons:
        button["text"] = " "


for i in range(9):
    button = tk.Button(root, text=" ", font=("Arial", 20), width=5, height=2,
                       command=lambda i=i: on_button_click(i))
    button.grid(row=i // 3, column=i % 3)
    buttons.append(button)

root.mainloop()
