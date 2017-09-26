from .exceptions import *
import random

class GuessAttempt(object):
    def __init__(self, letter, hit=None, miss=None):
        self.letter = letter
        self.hit = hit
        self.miss = miss
        
        if hit and miss:
            raise InvalidGuessAttempt
        
    def is_hit(self):
        if self.hit == True:
            return True
        return False
    
    def is_miss(self):
        if self.miss == True:
            return True
        return False
        
class GuessWord(object):
    def __init__(self, word):
        self.answer = word.lower()
        self.masked = '*' * len(word)
        self.new_word = ['*'] * len(word)

        if not word:
            raise InvalidWordException
            
    def perform_attempt(self, letter):
        letter = letter.lower()
        if len(letter) != 1:
            raise InvalidGuessedLetterException
        elif letter in self.answer:
            for character in range(len(self.answer)):
                if letter == self.answer[character]:
                    self.new_word[character] = letter
                elif self.answer[character] != '*':
                    pass
                else:
                    self.new_word[character] = '*'
            self.masked = ''.join(self.new_word)
            return GuessAttempt(letter, hit=True)
        else:
            return GuessAttempt(letter, miss=True)

class HangmanGame(object):
    WORD_LIST = ['rmotr', 'python', 'awesome']
    
    def __init__(self, word_list=None, number_of_guesses=5):
        if not word_list:
            word_list = self.WORD_LIST
        self.remaining_misses = number_of_guesses
        self.previous_guesses = []
        self.word = GuessWord(self.select_random_word(word_list))
    
    @classmethod    
    def select_random_word(cls, word_list):
        if not word_list:
            raise InvalidListOfWordsException()
        return random.choice(word_list)
        
    def guess(self, letter):
        letter = letter.lower()
        if self.is_finished():
            raise GameFinishedException()
        if letter in self.previous_guesses:
            raise InvalidGuessedLetterException()
        self.previous_guesses.append(letter)
        
        if self.word.perform_attempt(letter).is_miss():
            self.remaining_misses -= 1
        if self.is_won():
            raise GameWonException()
        if self.is_lost():
            raise GameLostException()

        return self.word.perform_attempt(letter)
        
    def is_won(self):
        return self.word.masked == self.word.answer
    
    def is_lost(self):
        return self.remaining_misses == 0
        
    def is_finished(self):
        return self.is_won() or self.is_lost()