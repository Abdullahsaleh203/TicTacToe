import tkinter as tk
from tkinter import messagebox
import os
import time

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

# Player
class Player:
    def __init__(self):
        self.name = ""
        self.symbol = ""

    def choose_name(self):
        while True:
            name = input("Enter your name (only letters) :- ")
            if name.isalpha():
                self.name = name
                break
            print("Only letters allowed")

    def choose_symbol(self):
        self.your_choice = ["X", "O"]
        while True:
            symbol = input(f"{self.name.capitalize()} Enter your symbol ({self.your_choice}): ").upper()
            if symbol.isalpha() and len(symbol) == 1 and symbol in self.your_choice:
                self.symbol = symbol.upper()
                break
            else:
                print("Only one letter allowed")

# Menu
class Menu:
    def validate_choice(self):
        while True:
            choice = input("Enter your choice (1 or 2): ")
            if choice.isnumeric() and int(choice) in [1, 2]:
                return int(choice)
            else:
                print("Invalid input. Please enter 1 or 2.")

    def display_main_menu(self):
        print("Welcome to my X-O game")
        print("1. Start the game")
        print("2. Quit Game")
        return self.validate_choice()

    def display_endgame_menu(self):
        menu_text = """
        Game Over!
        1. Play again
        2. Quit Game
        Enter your choice (1 or 2): """
        print(menu_text)
        return self.validate_choice()

# Board
class Board:
    def __init__(self):
        self.board = [str(i) for i in range(1, 10)]

    def display_board(self):
        for i in range(0, 9, 3):
            print("|".join(self.board[i:i+3]))
            if i < 6:
                print("------")

    def update_board(self, choice, symbol):
        if self.is_valid_move(choice):
            self.board[choice - 1] = symbol
            return True
        return False

    def is_valid_move(self, choice):
        return self.board[choice - 1].isdigit()

    def reset_board(self):
        self.board = [str(i) for i in range(1, 10)]

class Game:
    def __init__(self):
        self.players = [Player(), Player()]
        self.board = Board()
        self.menu = Menu()
        self.current_player_position = 0

    def start_game(self):
        choice = self.menu.display_main_menu()
        if choice == 1:
            self.setup_players()
            self.play_game()
        else:
            self.quit_game()

    def setup_players(self):
        for number, player in enumerate(self.players, start=1):
            print(f"Player {number}, Enter your details :- ")
            player.choose_name()
            player.choose_symbol()
            print("=" * 20)
            clear_screen()

    def quit_game(self):
        print("Game closed")
        time.sleep(2)
        clear_screen()

    def play_game(self):
        while True:
            choice = self.play_turn()

            # Get the current player's symbol
            symbol = self.players[self.current_player_position].symbol

            # Update the board with the player's choice and symbol
            self.board.update_board(choice, symbol)
            player = self.players[self.current_player_position]

            if self.check_win() :
                self.congratulate_winner()
                choice = self.menu.display_endgame_menu()
                if choice == 1:
                    self.restart_game()
                else:
                    self.quit_game()
                    break
            elif self.check_draw():
                choice = self.menu.display_endgame_menu()
                if choice == 1:
                    self.restart_game()
                else:
                    self.quit_game()
                    break
            self.switch_player()

    def play_turn(self):
        player = self.players[self.current_player_position]
        self.board.display_board()
        print(f"{player.name}'s turn {player.symbol}")
        while True:
            try:
                cell_choice = int(input("Choose a cell to display on the board from [1-9] "))
                if 1 <= cell_choice <= 9 and self.board.update_board(cell_choice, player.symbol):
                    return cell_choice
                else:
                    print("Invalid move, try again.")
            except ValueError:
                print("Please enter a number between 1 and 9")
            self.switch_player()

    def switch_player(self):
        self.current_player_position = 1 - self.current_player_position

    def check_win(self):
        win_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],
            [0, 3, 6], [1, 4, 7], [2, 5, 8],
            [0, 4, 8], [2, 4, 6]
        ]
        for combo in win_combinations:
            if self.board.board[combo[0]] == self.board.board[combo[1]] == self.board.board[combo[2]]:
                return True
        return False
    def congratulate_winner(self):
        winner = self.players[self.current_player_position]
        print(f"Congratulations, {winner.name}! You won!")

    def check_draw(self):
        return all(not cell.isdigit() for cell in self.board.board)

    def restart_game(self):
        print("Restarting the game...")
        self.board.reset_board()
        self.current_player_position = 0
        self.play_game()

game = Game()
game.start_game()
