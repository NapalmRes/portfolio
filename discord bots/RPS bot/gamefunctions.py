# Problem Set 2, hangman.py
# Name: 
# Collaborators:
# Time spent:

# Hangman Game
# -----------------------------------
# Helper code
# You don't need to understand this helper code,
# but you will have to know how to use the functions
# (so be sure to read the docstrings!)
import random
import string

WORDLIST_FILENAME = "words.txt"

def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
    print("  ", len(wordlist), "words loaded.")
    return wordlist
wordlist = load_words()

def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)
    
    Returns a word from wordlist at random
    """
    return random.choice(wordlist)


# end of helper code

# -----------------------------------

# Load the list of words into the variable wordlist
# so that it can be accessed from anywhere in the program



def get_chars(input):
    """
     input: string or list (of letters), what user wants to get letters from
     returns: list, list of all unique letters in the input
    """
    letters = []
    for char in input:
        if char not in letters:
            letters.append(char)
            letters.sort()
    return letters

def is_word_guessed(secret_word, letters_guessed):
    """
    secret_word: string, the word the user is guessing; assumes all letters are
      lowercase
    letters_guessed: list (of letters), which letters have been guessed so far;
      assumes that all letters are lowercase
    returns: boolean, True if all the letters of secret_word are in letters_guessed;
      False otherwise
    """
    swc = get_chars(secret_word)
    swc_copy = swc[:]
    lgc = get_chars(letters_guessed)
    for char in swc_copy:
        if char in lgc:
            swc.remove(char)
        if swc == []:
            return True
    return False


def get_guessed_word(secret_word, letters_guessed):
    """
    secret_word: string, the word the user is guessing
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string, comprised of letters, underscores (_), and spaces that represents
      which letters in secret_word have been guessed so far.
    """
    string = ''
    for char in secret_word:
        if char in letters_guessed:
            string += char
        else:
            string += ' - '
    return string


def get_available_letters(letters_guessed):
    """
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string (of letters), comprised of letters that represents which letters have not
      yet been guessed.
    """
    alphabet = list(string.ascii_lowercase)
    for char in letters_guessed:
        if char in alphabet:
            alphabet.remove(char)
    return ''.join(alphabet)


def hangman(secret_word):
    """
    secret_word: string, the secret word to guess.

    Starts up an interactive game of Hangman.

    * At the start of the game, let the user know how many
      letters the secret_word contains and how many guesses s/he starts with.

    * The user should start with 6 guesses

    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.

    * Ask the user to supply one guess per round. Remember to make
      sure that the user puts in a letter!

    * The user should receive feedback immediately after each guess
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the
      partially guessed word so far.

    Follows the other limitations detailed in the problem write-up.
    """
    guessed_letters = []
    alphabet = string.ascii_lowercase
    i = 0
    warnings = 3
    print('Welcome to hangman!\nThe word you are guessing contains', len(secret_word), 'letters!\nYou have', warnings,
          'warnings left!')
    while i <= 5:
        print('You have', (6 - i), 'guess(es)!\n___________________')
        print('Available letters are:', get_available_letters(guessed_letters))
        guess = input('Please guess a lower case letter:')
        if len(guess) != 1 or guess not in alphabet:
            print('That was not a valid letter!')
            if warnings > 0:
                warnings -= 1
                i -= 1
                print('You have', warnings, 'warnings left!')
            else:
                print('You have lost a guess!')
        if guess in guessed_letters:
            print('You have already guessed this letter!')
            if warnings > 0:
                warnings -= 1
                i -= 1
                print('You have', warnings, 'warnings left!')
            else:
                print('You have lost a guess!')
        if guess in secret_word and guess not in guessed_letters:
            print(guess, 'was in the word!')
            i -= 1
        elif guess not in secret_word and guess in alphabet:
            print(guess, 'was not in the word...')
        if len(guess) == 1 and guess in alphabet:
            guessed_letters += guess
        print('Current word is:', get_guessed_word(secret_word, guessed_letters))
        print('___________________')
        if is_word_guessed(secret_word, guessed_letters) is True:
            print('Congratulations you have won!')
            print('Your score was', (6-i)*len(get_chars(secret_word)))
            return
        i += 1
    print('You have lost...\nThe word was:', secret_word)


# When you've completed your hangman function, scroll down to the bottom
# of the file and uncomment the first two lines to test
# (hint: you might want to pick your own
# secret_word while you're doing your own testing)


# -----------------------------------


def match_with_gaps(my_word, other_word):
    """
    my_word: string with _ characters, current guess of secret word
    other_word: string, regular English word
    returns: boolean, True if all the actual letters of my_word match the
        corresponding letters of other_word, or the letter is the special symbol
        _ , and my_word and other_word are of the same length;
        False otherwise:
    """
    chars_my_word = get_chars(my_word)
    other_guessed_word = get_guessed_word(other_word,chars_my_word)
    if other_guessed_word == my_word:
        return True
    return False


    
#print(match_with_gaps(input('Please enter your word:'),input('Please enter the other word:')))

def show_possible_matches(my_word):
    """
    my_word: string with _ characters, current guess of secret word
    returns: nothing, but should print out every word in wordlist that matches my_word
             Keep in mind that in hangman when a letter is guessed, all the positions
             at which that letter occurs in the secret word are revealed.
             Therefore, the hidden letter(_ ) cannot be one of the letters in the word
             that has already been revealed.

    """
    matches = 0
    match_string = ''
    for word in wordlist:
        if match_with_gaps(my_word, word) is True:
            print(word)
            matches += 1
            match_string += word
    print(matches)
    if matches == 0:
        print('No matches found!')
    return match_string
        
def how_many_possible_matches(word):
    """
    """
    counter = 0
    for word in show_possible_matches(word):
        counter += 1
    return counter

def hangman_with_hints(secret_word):
    """
    secret_word: string, the secret word to guess.

    Starts up an interactive game of Hangman.

    * At the start of the game, let the user know how many
      letters the secret_word contains and how many guesses s/he starts with.

    * The user should start with 6 guesses

    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.

    * Ask the user to supply one guess per round. Make sure to check that the user guesses a letter

    * The user should receive feedback immediately after each guess
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the
      partially guessed word so far.

    * If the guess is the symbol *, print out all words in wordlist that
      matches the current guessed word.

    Follows the other limitations detailed in the problem write-up.
    """
    guessed_letters = []
    alphabet = string.ascii_lowercase
    i = 0
    hints = 1
    warnings = 3
    print('Welcome to hangman!\nThe word you are guessing contains', len(secret_word), 'letters!\nYou have', warnings,
          'warnings left!')
    while i <= 5:
        print('You have', (6 - i), 'guess(es)', 'and', hints, 'hint(s)!\n___________________')
        print('Available letters are:', get_available_letters(guessed_letters))
        guess = input('Please guess a lower case letter:')
        if guess == '*' and hints > 0:
            show_possible_matches(get_guessed_word(secret_word, guessed_letters))
            hints -= 1
            i -= 1
        elif guess == '*':
            print('Sorry you have no hints left!')
            i -= 1
        if (len(guess) != 1 or guess not in alphabet) and guess != '*':
            print('That was not a valid letter!')
            if warnings > 0:
                warnings -= 1
                i -= 1
                print('You have', warnings, 'warnings left!')
            else:
                print('You have lost a guess!')
        if guess in guessed_letters:
            print('You have already guessed this letter!')
            if warnings > 0:
                warnings -= 1
                i -= 1
                print('You have', warnings, 'warnings left!')
            else:
                print('You have lost a guess!')
        if guess in secret_word and guess not in guessed_letters:
            print(guess, 'was in the word!')
            i -= 1
        elif guess not in secret_word and guess in alphabet:
            print(guess, 'was not in the word...')
        if len(guess) == 1 and guess in alphabet:
            guessed_letters += guess
        print('Current word is:', get_guessed_word(secret_word, guessed_letters))
        print('___________________')
        if is_word_guessed(secret_word, guessed_letters) is True:
            print('Congratulations you have won!')
            print('Your score was', ((6-i)*len(get_chars(secret_word))) )
            if hints == 0:
                print('But you used a hint...')
            return
        i += 1
    print('You have lost...\nThe word was:', secret_word)


# When you've completed your hangman_with_hint function, comment the two similar
# lines above that were used to run the hangman function, and then uncomment
# these two lines and run this file to test!
# Hint: You might want to pick your own secret_word while you're testing.


if __name__ == "__main__":
    pass

    # To test part 2, comment out the pass line above and
    # uncomment the following two lines.

    #secret_word = choose_word(wordlist)
    #hangman(secret_word)

###############

# To test part 3 re-comment out the above lines and
# uncomment the following two lines.



# 6.0001 Problem Set 3
#
# The 6.0001 Word Game
# Created by: Kevin Luu <luuk> and Jenna Wiens <jwiens>
#
# Name          : <your name>
# Collaborators : <your collaborators>
# Time spent    : <total time>

import math
import random
import string

VOWELS = 'aeiou'
CONSONANTS = 'bcdfghjklmnpqrstvwxyz'
HAND_SIZE = 7

SCRABBLE_LETTER_VALUES = {
    'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 'i': 1, 'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1, 'o': 1, 'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10
}

# -----------------------------------
# Helper code
# (you don't need to understand this helper code)



def get_frequency_dict(sequence):
    """
    Returns a dictionary where the keys are elements of the sequence
    and the values are integer counts, for the number of times that
    an element is repeated in the sequence.

    sequence: string or list
    return: dictionary
    """
    
    # freqs: dictionary (element_type -> int)
    freq = {}
    for x in sequence:
        freq[x] = freq.get(x,0) + 1
    return freq
	

# (end of helper code)
# -----------------------------------

#
# Problem #1: Scoring a word
#
def get_word_score(word, n):
    """
    Returns the score for a word. Assumes the word is a
    valid word.

    You may assume that the input word is always either a string of letters, 
    or the empty string "". You may not assume that the string will only contain 
    lowercase letters, so you will have to handle uppercase and mixed case strings 
    appropriately. 

	The score for a word is the product of two components:

	The first component is the sum of the points for letters in the word.
	The second component is the larger of:
            1, or
            7*wordlen - 3*(n-wordlen), where wordlen is the length of the word
            and n is the hand length when the word was played

	Letters are scored as in Scrabble; A is worth 1, B is
	worth 3, C is worth 3, D is worth 2, E is worth 1, and so on.

    word: string
    n: int >= 0
    returns: int >= 0
    """
    score = 0
    sum = 0
    word_lower = str(word.lower())
    for char in word_lower:
        if char in string.ascii_lowercase:
            sum += SCRABBLE_LETTER_VALUES[char]
    multiplier = (7*len(word_lower) - 3*(n-len(word_lower)))
    if  multiplier > 1:
        score = sum*multiplier
        return score
    else:
        return sum

#
# Make sure you understand how this function works and what it does!
#
def display_hand(hand):
    """
    Displays the letters currently in the hand.

    For example:
       display_hand({'a':1, 'x':2, 'l':3, 'e':1})
    Should print out something like:
       a x x l l l e
    The order of the letters is unimportant.

    hand: dictionary (string -> int)
    """
    displayed_hand = ''
    for letter in hand.keys():
        for j in range(hand[letter]):
             displayed_hand += letter + ' '      # print all on the same line
    return displayed_hand                             # print an empty line

#
# Make sure you understand how this function works and what it does!
# You will need to modify this for Problem #4.
#
def deal_hand(n):
    """
    Returns a random hand containing n lowercase letters.
    ceil(n/3) letters in the hand should be VOWELS (note,
    ceil(n/3) means the smallest integer not less than n/3).

    Hands are represented as dictionaries. The keys are
    letters and the values are the number of times the
    particular letter is repeated in that hand.

    n: int >= 0
    returns: dictionary (string -> int)
    """
    
    hand={}
    num_vowels = int(math.ceil(n / 3) - 1)

    for i in range(num_vowels):
        x = random.choice(VOWELS)
        hand[x] = hand.get(x, 0) + 1
    
    for i in range(num_vowels, n):    
        x = random.choice(CONSONANTS)
        hand[x] = hand.get(x, 0) + 1

    hand['*'] = 1
    return hand


# Problem #2: Update a hand by removing letters
#
def update_hand(hand, word):
    """
    Does NOT assume that hand contains every letter in word at least as
    many times as the letter appears in word. Letters in word that don't
    appear in hand should be ignored. Letters that appear in word more times
    than in hand should never result in a negative count; instead, set the
    count in the returned hand to 0 (or remove the letter from the
    dictionary, depending on how your code is structured). 

    Updates the hand: uses up the letters in the given word
    and returns the new hand, without those letters in it.

    Has no side effects: does not modify hand.

    word: string
    hand: dictionary (string -> int)    
    returns: dictionary (string -> int)
    """
    updated_hand = hand.copy()
    word_lower = word.lower()
    word_dict = get_frequency_dict(word_lower)
    for letter in word_dict.keys():
        updated_hand[letter] = hand.get(letter, 0) - word_dict[letter]
        if updated_hand[letter] <= 0:
            del(updated_hand[letter])
    return updated_hand

#
# Problem #3: Test word validity
#
def is_valid_word(word, hand, word_list):
    """
    Returns True if word is in the word_list and is entirely
    composed of letters in the hand. Otherwise, returns False.
    Does not mutate hand or word_list.
   
    word: string
    hand: dictionary (string -> int)
    word_list: list of lowercase strings
    returns: boolean
    """

    word_lower = word.lower()
    word_dict = get_frequency_dict(word_lower)
    copied_hand = hand.copy()
    wildcard_index = word_lower.find('*')
    if wildcard_index > 0:
        word_lower_list = list(word_lower)
        for vowel in VOWELS:
            word_lower_list[wildcard_index] = vowel
            word_lower_new = ''.join(word_lower_list)
            if word_lower_new in word_list:
                word_lower = word_lower_new


    if word_lower in word_list:
        for letter in word_dict:
            for i in range(word_dict[letter]):
                copied_hand[letter] = copied_hand.get(letter, 0) - 1
                if copied_hand[letter] < 0:
                    return False
    else:
        return False
    return True

#
# Problem #5: Playing a hand
#
def calculate_handlen(hand):
    """ 
    Returns the length (number of letters) in the current hand.
    
    hand: dictionary (string-> int)
    returns: integer
    """
    
    pass  # TO DO... Remove this line when you implement this function

def play_hand(hand, word_list):

    """
    Allows the user to play the given hand, as follows:

    * The hand is displayed.
    
    * The user may input a word.

    * When any word is entered (valid or invalid), it uses up letters
      from the hand.

    * An invalid word is rejected, and a message is displayed asking
      the user to choose another word.

    * After every valid word: the score for that word is displayed,
      the remaining letters in the hand are displayed, and the user
      is asked to input another word.

    * The sum of the word scores is displayed when the hand finishes.

    * The hand finishes when there are no more unused letters.
      The user can also finish playing the hand by inputing two 
      exclamation points (the string '!!') instead of a word.

      hand: dictionary (string -> int)
      word_list: list of lowercase strings
      returns: the total score for the hand
      
    """
    score = 0
    while len(hand) > 0:
        print('Current hand:', display_hand(hand))
        word = input('Enter word, or "!!" when you are finished playing your hand:')
        if word == '!!':
            print('Total score for this hand:', score)
            return score
        if is_valid_word(word, hand, word_list) == True:
            word_score = get_word_score(word, len(hand))
            print(word, 'earned', word_score, 'points.')
            score += word_score
            print('Total score:', score)
        else:
            print('That is not a valid word. Please choose another word.')
        hand = update_hand(hand, word)
    print('Total score for this hand:', score)
    return score





#
# Problem #6: Playing a game
# 


#
# procedure you will use to substitute a letter in a hand
#

def substitute_hand(hand, letter):
    """ 
    Allow the user to replace all copies of one letter in the hand (chosen by user)
    with a new letter chosen from the VOWELS and CONSONANTS at random. The new letter
    should be different from user's choice, and should not be any of the letters
    already in the hand.

    If user provide a letter not in the hand, the hand should be the same.

    Has no side effects: does not mutate hand.

    For example:
        substitute_hand({'h':1, 'e':1, 'l':2, 'o':1}, 'l')
    might return:
        {'h':1, 'e':1, 'o':1, 'x':2} -> if the new letter is 'x'
    The new letter should not be 'h', 'e', 'l', or 'o' since those letters were
    already in the hand.
    
    hand: dictionary (string -> int)
    letter: string
    returns: dictionary (string -> int)
    """
    lower_letter = letter.lower()
    num_letter = hand[lower_letter]
    copied_hand = hand.copy()
    alphabet = list(string.ascii_lowercase)
    for letters in copied_hand:
        if letters in alphabet:
            alphabet.remove(letters)
    del(copied_hand[lower_letter])
    for i in range(num_letter):
        random_letter = random.choice(alphabet)
        copied_hand[random_letter] = copied_hand.get(random_letter, 0) + 1
    return copied_hand



       
    
def play_game(word_list):
    """
    Allow the user to play a series of hands

    * Asks the user to input a total number of hands

    * Accumulates the score for each hand into a total score for the 
      entire series
 
    * For each hand, before playing, ask the user if they want to substitute
      one letter for another. If the user inputs 'yes', prompt them for their
      desired letter. This can only be done once during the game. Once the
      substitue option is used, the user should not be asked if they want to
      substitute letters in the future.

    * For each hand, ask the user if they would like to replay the hand.
      If the user inputs 'yes', they will replay the hand and keep 
      the better of the two scores for that hand.  This can only be done once 
      during the game. Once the replay option is used, the user should not
      be asked if they want to replay future hands. Replaying the hand does
      not count as one of the total number of hands the user initially
      wanted to play.

            * Note: if you replay a hand, you do not get the option to substitute
                    a letter - you must play whatever hand you just had.
      
    * Returns the total score for the series of hands

    word_list: list of lowercase strings
    """
    score = 0
    substiute = 1
    replay = 1
    no_hands = input('Enter total number of hands:')

    try :
        int(no_hands)
    except:
        print('That was not an integer, exiting game...')
        return

    for i in range(int(no_hands)):
        hand = deal_hand(HAND_SIZE)
        if substiute > 0:
            print('Current hand:', display_hand(hand))
            asks = input('Would you like to substitute a letter?').lower()
            if asks == 'yes':
                substiute -= 1
                hand = substitute_hand(hand, input('Enter the letter to replace:'))
        initial_score = score
        score += play_hand(hand, word_list)
        if replay > 0:
            askr = input('Would you like to replay that hand?').lower()
            if askr == 'yes':
                replay -= 1
                score = initial_score
                score += play_hand(hand, word_list)
    print('The total score for all', no_hands, 'hands:', score)
    return score


    


#
# Build data structures used for entire session and play game
# Do not remove the "if __name__ == '__main__':" line - this code is executed
# when the program is run directly, instead of through an import statement
#
if __name__ == '__main__':
    word_list = load_words()
    play_game(word_list)
