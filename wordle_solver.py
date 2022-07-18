import ast
import random
import requests
import sys
from seleniumbase import BaseCase
from datetime import datetime


class WordleTests(BaseCase):
    word_list = []

    def initialize_word_list(self):
        txt_file = "https://seleniumbase.io/cdn/txt/wordle_words.txt"
        word_string = requests.get(txt_file).text
        tmp_list = ast.literal_eval(word_string)
        ### Adding 3 words that will significantly reduce word space
        tmp_list.append("adieu")
        tmp_list.append("golps")
        tmp_list.append("crwth")
        self.word_list = tmp_list
        
    def modify_word_list(self, word, letter_status):
        new_word_list = []
        correct_letters = set()
        present_letters = set()

        ### Checks if there are any letters in their correct position 
        for i in range(len(word)):
            if letter_status[i] == "correct":
                correct_letters.add(word[i])
                for w in self.word_list:
                    if w[i] == word[i]:
                        new_word_list.append(w)
                self.word_list = new_word_list
                new_word_list = []

        ### Checks if there are any letters in the word but incorrect position
        for i in range(len(word)):
            if letter_status[i] == "present":
                present_letters.add(word[i])
                for w in self.word_list:
                    if word[i] in w and word[i] != w[i]:
                        new_word_list.append(w)
                self.word_list = new_word_list
                new_word_list = []

        ### Updates word list by removing words that contain absent letters
        for i in range(len(word)):
            if (
                letter_status[i] == "absent"
                and word[i] not in correct_letters
                and word[i] not in present_letters
            ):
                for w in self.word_list:
                    if word[i] not in w:
                        new_word_list.append(w)
                self.word_list = new_word_list
                new_word_list = []


    def test_wordle(self):
        ### Opening File Write
        stdoutOrigin=sys.stdout 
        sys.stdout = open("log.txt", "a")

        ### Accessing Website
        self.open("https://www.nytimes.com/games/wordle/index.html")
        ### Closing popup
        self.click('svg[data-testid="icon-close"]')
        self.initialize_word_list()
        num_attempts = 0
        success = False

        ### Loop for the 6 word attempts
        for attempt in range(6):
            num_attempts += 1
            ### Reducing Word Space by Enforcing 3 words
            if(attempt == 0):
                word = "adieu"
            elif(attempt == 1):
                word = "golps"
            elif(attempt == 2):
                word = "crwth"
            else:
                word = random.choice(self.word_list)
            letters = []
            for letter in word:
                letters.append(letter)
                button = 'button[data-key="%s"]' % letter
                self.click(button)
            button = 'button[class*="oneAndAHalf"]'
            self.click(button)
            row = (
                'div[class*="lbzlf"] div[class*="Row-module"]:nth-of-type(%s) '
                % num_attempts
            )
            tile = row + 'div:nth-child(%s) div[class*="module_tile__3ayIZ"]'
            self.wait_for_element(tile % "5" + '[data-state*="e"]')
            letter_status = []
            for i in range(1, 6):
                letter_eval = self.get_attribute(tile % str(i), "data-state")
                letter_status.append(letter_eval)
            if letter_status.count("correct") == 5:
                success = True
                break
            self.modify_word_list(word, letter_status)

        ### Saving Screenshot
        #self.save_screenshot_to_logs()
        #now = datetime.now().strftime("%m/%d/%Y_%H:%M:%S")
        #self.save_screenshot(datetime.now().strftime("%m/%d/%Y_%H:%M:%S"), folder="./screenshots")
        
        ### Print based on Output
        if success:
           self._print('\nWord: "%s"\nAttempts: %s' % (word.upper(), num_attempts))
        else:
            print('Final guess: "%s" (Not the correct word!)' % word.upper())
            self.fail("Unable to solve for the correct word in 6 attempts!")

        ### Closing file write
        sys.stdout.close()
        sys.stdout=stdoutOrigin
        self.sleep(1)