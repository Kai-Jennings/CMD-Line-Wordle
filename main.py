import random
import os

GREEN = "\033[38;2;0;0;0;48;2;106;170;100m"
YELLOW = "\033[38;2;0;0;0;48;2;201;180;88m"
DEFAULT = "\033[0m"
CLEAR = "cls" if os.name == "nt" else "clear"


class Game:
    def __init__(self):
        self.max_guesses = 6
        self.valid_words = set()
        self.valid_answers = []

        with open("valid_words.txt", "r") as f:
            for line in f:
                self.valid_words.add(line.strip())

        with open("valid_answers.txt", "r") as f:
            for line in f:
                self.valid_answers.append(line.strip())

        self.answer = random.choice(self.valid_answers)
        self.guesses = []
        self.guess_count = 0
        self.win = False

    def display(self, display_guess=True):
        if display_guess:
            print(f"Guess {self.guess_count + 1}/{self.max_guesses}")
        for guess in self.guesses:
            print(self.colourize(guess))

    def colourize(self, guess):
        buffer = ""
        for x, y in self.evaluate(guess):
            if y == 0:
                buffer += colour(f" {x} ", GREEN)
            elif y == 1:
                buffer += f" {x} "
            else:
                buffer += colour(f" {x} ", YELLOW)
        return buffer

    def evaluate(self, guess):
        """
        0 -> GREEN
        1 -> YELLOW
        2 -> DEFAULT
        """
        evaluation = []
        chars = [x for x, y in zip(guess, self.answer) if x != y]
        for x, y in zip(guess, self.answer):
            if x == y:
                evaluation.append((x, 0))
            elif x not in self.answer:
                evaluation.append((x, 1))
            else:
                if x in chars:
                    evaluation.append((x, 2))
                    chars.remove(x)
                else:
                    evaluation.append((x, 0))
        return evaluation

    def guess(self, word):
        if word in self.valid_words:
            self.guesses.append(word)
            self.guess_count += 1
        return word == self.answer

    def game_loop(self):
        while True:
            while self.guess_count < self.max_guesses and not self.win:
                self.display()
                if self.guess(input()):
                    self.win = True
                os.system(CLEAR)

            self.display(False)
            if self.win:
                print(f"You guessed the word in {self.guess_count} guess(es)")
            else:
                print(f"The word was {self.answer}")

            input()
            self.reset()
            os.system(CLEAR)

    def reset(self):
        self.answer = random.choice(self.valid_answers)
        self.guesses = []
        self.guess_count = 0
        self.win = False


def colour(text, c):
    return c + text + DEFAULT


if __name__ == "__main__":
    Game().game_loop()
