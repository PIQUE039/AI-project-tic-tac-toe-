import tkinter as tk
from tkinter import messagebox
import numpy as np

class TicTacToe:
    def __init__(self, master):
        self.master = master
        self.master.title("Tic Tac Toe")
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        self.create_board()
        self.choose_first_move()

    def create_board(self):
        for i in range(3):
            for j in range(3):
                self.buttons[i][j] = tk.Button(self.master, text='', font=('Roboto', 20), width=7, height=5,
                                                command=lambda row=i, col=j: self.on_button_click(row, col))
                self.buttons[i][j].grid(row=i, column=j)

    def on_button_click(self, row, col):
        if self.board[row][col] == ' ':
            self.board[row][col] = self.current_player
            self.buttons[row][col].config(text=self.current_player)
            if self.check_winner(self.current_player):
                messagebox.showinfo("Winner", f"{self.current_player} wins!")
                self.reset_board()
            elif self.check_draw():
                messagebox.showinfo("Draw", "The game is a draw!")
                self.reset_board()
            else:
                self.current_player = 'O' if self.current_player == 'X' else 'X'
                if self.current_player == 'O':
                    self.ai_move()

    def choose_first_move(self):
        response = messagebox.askyesno("First Move", "Do you want to play first?")
        if not response:
            self.current_player = 'O'
            self.ai_move()

    def check_winner(self, player):
        # Checking rows, columns, and diagonals
        for i in range(3):
            if all(self.board[i][j] == player for j in range(3)) or \
               all(self.board[j][i] == player for j in range(3)):
                return True
        if all(self.board[i][i] == player for i in range(3)) or \
           all(self.board[i][2 - i] == player for i in range(3)):
            return True
        return False

    def check_draw(self):
        return all(self.board[i][j] != ' ' for i in range(3) for j in range(3))

    def reset_board(self):
        for i in range(3):
            for j in range(3):
                self.board[i][j] = ' '
                self.buttons[i][j].config(text='')
        self.choose_first_move()

    def ai_move(self):
        best_score = -np.inf
        best_move = None
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == ' ':
                    self.board[i][j] = 'O'
                    score = self.minimax(False)
                    self.board[i][j] = ' '
                    if score > best_score:
                        best_score = score
                        best_move = (i, j)
        row, col = best_move
        self.board[row][col] = 'O'
        self.buttons[row][col].config(text='O')
        if self.check_winner('O'):
            messagebox.showinfo("Winner", "AI wins!")
            self.reset_board()
        elif self.check_draw():
            messagebox.showinfo("Draw", "The game is a draw!")
            self.reset_board()
        else:
            self.current_player = 'X'

    def minimax(self, is_maximizing):
        if self.check_winner('O'):
            return 1
        elif self.check_winner('X'):
            return -1
        elif self.check_draw():
            return 0

        if is_maximizing:
            best_score = -np.inf
            for i in range(3):
                for j in range(3):
                    if self.board[i][j] == ' ':
                        self.board[i][j] = 'O'
                        score = self.minimax(False)
                        self.board[i][j] = ' '
                        best_score = max(score, best_score)
            return best_score
        else:
            best_score = np.inf
            for i in range(3):
                for j in range(3):
                    if self.board[i][j] == ' ':
                        self.board[i][j] = 'X'
                        score = self.minimax(True)
                        self.board[i][j] = ' '
                        best_score = min(score, best_score)
            return best_score

def main():
    root = tk.Tk()
    game = TicTacToe(root)
    root.mainloop()

if __name__ == "__main__":
    main()
