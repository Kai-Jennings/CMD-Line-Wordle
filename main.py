import random
import os

GREEN = "\033[38;2;0;0;0;48;2;106;170;100m"
YELLOW = "\033[38;2;0;0;0;48;2;201;180;88m"
DEFAULT = "\033[0m"
CLEAR = "cls" if os.name == "nt" else "clear"


class Game:
    def __init__(self):
        self.guesses = []
        self.guess_count = 0
        self.max_guesses = 6
        self.valid_words = set()
        self.valid_answers = set()
        self.win = False

        with open("valid_words.txt", "r") as f:
            for line in f:
                self.valid_words.add(line.strip())

        with open("valid_answers.txt", "r") as f:
            for line in f:
                self.valid_answers.add(line.strip())

        self.answer = random.choice(list(self.valid_answers))

        self.game_loop()

    def display(self, display_guess=True):
        if display_guess:
            print(f"Guess {self.guess_count + 1}/{self.max_guesses}")
        for guess in self.guesses:
            print(self.colourize(guess))

    def colourize(self, guess):
        buffer = ""
        chars = list(self.answer)
        for x, y in zip(guess, self.answer):
            if x == y:
                chars.remove(x)
        for x, y in zip(guess, self.answer):
            if x == y:
                buffer += colour(f" {x} ", GREEN)
            elif x not in self.answer:
                buffer += f" {x} "
            else:
                if x in chars:
                    buffer += colour(f" {x} ", YELLOW)
                    chars.remove(x)
                else:
                    buffer += f" {x} "
        return buffer

    def game_loop(self):
        while self.guess_count < self.max_guesses:
            self.display()
            guess = input()
            if guess in self.valid_words:
                self.guesses.append(guess)
                self.guess_count += 1
            if guess == self.answer:
                self.win = True
                os.system(CLEAR)
                break
            os.system(CLEAR)

        self.display(False)
        if self.win:
            print(f"You guessed the word in {self.guess_count} guesses.")
        else:
            print(f"The word was {self.answer}")


def colour(text, c):
    return c + text + DEFAULT


game = Game()
