import os
import discord
from dotenv import load_dotenv
from discord.utils import get
from discord.ext import commands
from discord import FFmpegPCMAudio
from gamefunctions import *
import random
import time
import pandas as pd
import string

WORDLIST_FILENAME = "words.txt"

word_list = load_words()


     
# Creates dictionary of outcomes where 0 is a draw, 1 is a win for P1 (row), and 2 is a win for P2 (column)
rps = {
    "rock": ["0", "1", "2"],
    "paper": ["2", "0", "1"],
    "scissors": ["1", "2", "0"]
}

# Changes dictionary into dataframe and uses P1 to index the rows
game = pd.DataFrame(rps, index=["rock", "paper", "scissors"])
print(game)

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()
bot = commands.Bot(command_prefix="&")

# Checks if a user is part of the scores.csv file if not creates a row for that user
def user_check(u):
    global scoresg
    scoresg = pd.read_csv("scores.csv", index_col="user")
    try:
        scoresg.loc[u]
    except KeyError:
        print('That user does not exist yet, creating user now.')
        scoresg.loc[u, :] = [0,0,0]

# Prints out message once bot connects to discord        
@client.event   
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    
# Whenever there is a message sent in chat this code is run, it checks the message content for any commands sent by a user
@client.event
async def on_message(message):
    # Checks if the author of a message is not a bot if it is runs the code if not ends the code 
    user = message.author
    if message.author == client.user:
        return
    
    # If a user sends &solorps in chat the user plays a game of rps against the bot
    if message.content == '&solorps':
        # A list of choices which the bot randomly selects as their choice against the player
        choices = ['rock','paper','scissors']

        # Sends a series of messages which prompt the user to send rock, paper, or scissors
        await message.channel.send('Send rock, paper or scissors on shoot!')
        time.sleep(1)
        await message.channel.send('3')
        time.sleep(1)
        await message.channel.send('2')
        time.sleep(1)
        await message.channel.send('1')
        time.sleep(1)
        await message.channel.send('Shoot!')

        # Checks the author of the message to see if they are in the scores.csv if not creates a row for that user
        U1 = await client.wait_for('message',timeout=60.0)
        U1a = str(U1.author)
        print(U1a)
        user_check(U1a)
        
        # Checks the content of the message and assigns it to C1
        C1 = U1.content
        print(C1)

        # Randomly chooses rock, paper, or scissors and sends its choice to the user
        C2 = random.choice(choices)
        await message.channel.send(C2)

        # Tests if the user sent a valid response by attempting to index the dataframe if they didn't prompt them to retype their message
        while True:
            try:
                game.loc[C1, C2]
            except KeyError:
                
                await message.channel.send('You did not send rock, paper or scissors! It must be all lowercase!')
                
                await message.channel.send('Send rock, paper or scissors on shoot!')
                time.sleep(1)
                await message.channel.send('3')
                time.sleep(1)
                await message.channel.send('2')
                time.sleep(1)
                await message.channel.send('1')
                time.sleep(1)
                await message.channel.send('Shoot!')
                
                U1 = await client.wait_for('message',timeout=60.0)
                U1a = str(U1.author)
                print(U1a)
                C1 = U1.content
                print(C1)
                
                C2 = random.choice(choices)
                await message.channel.send(C2)

                   
            else:
                break
        result = int(game.loc[C1, C2])
        # Prints integer value of result, sends the user the outcome, and updates the scores.csv file based on the outcome
        print(result)
        if result == 1:
            await message.channel.send(U1a + ' wins!')
            scoresg.loc[U1a, 'wins'] = scoresg.loc[U1a, 'wins'] + 1
            await message.channel.send(U1a + ' has ' + str(scoresg.loc[U1a, 'wins']) + ' wins.')
            scoresg.to_csv("scores.csv")
        if result == 2:
            await message.channel.send('RPS bot wins!')
            scoresg.loc[U1a, 'losses'] = scoresg.loc[U1a, 'losses'] + 1
            await message.channel.send(U1a + ' has ' + str(scoresg.loc[U1a, 'losses']) + ' losses.')
            scoresg.to_csv("scores.csv")
        if result == 0:
            await message.channel.send('Draw.')
            scoresg.loc[U1a, 'draws'] = scoresg.loc[U1a, 'draws'] + 1
            await message.channel.send(U1a + ' has ' + str(scoresg.loc[U1a, 'draws']) + ' draws.')
            scoresg.to_csv("scores.csv")

    # If a user sends &rps starts a game of rps between two users
    if message.content == '&rps':
        
        await message.channel.send('Send rock, paper or scissors on shoot!')
        time.sleep(1)
        await message.channel.send('3')
        time.sleep(1)
        await message.channel.send('2')
        time.sleep(1)
        await message.channel.send('1')
        time.sleep(1)
        await message.channel.send('Shoot!')

        # Same as above, but this time runs a check for both users who send in a choice and checks if someone tries to play against themselves
        U1 = await client.wait_for('message',timeout=60.0)
        U1a = str(U1.author)
        print(U1a)
        user_check(U1a)
        U2 = await client.wait_for('message',timeout=3.0)
        U2a = str(U2.author)
        # If someone tries to play against themselves ends the game
        if U1a == U2a:
            await message.channel.send("You can't play against yourself!")
            await message.channel.send("Ending game!")
            await client.wait_for('message',timeout=0.2)
        user_check(U2a)
        print(scoresg)

        # Assigns choice of player 1 to C1 and choice of player 2 to C2
        C1 = U1.content
        print(C1)
        C2 = U2.content
        print(C2)
        
        while True:
            try:
                game.loc[C1, C2]
            except KeyError:
                
                await message.channel.send('One of you did not send rock, paper or scissors!')
                
                await message.channel.send('Send rock, paper or scissors on shoot!')
                time.sleep(1)
                await message.channel.send('3')
                time.sleep(1)
                await message.channel.send('2')
                time.sleep(1)
                await message.channel.send('1')
                time.sleep(1)
                await message.channel.send('Shoot!')
                
                U1 = await client.wait_for('message',timeout=10.0)
                U1a = str(U1.author)
                print(U1a)
                U2 = await client.wait_for('message',timeout=10.0)
                U2a = str(U2.author)
                
                if U1a == U2a:
                    await message.channel.send("You can't play against yourself!")
                    await message.channel.send("Ending game!")
                    await client.wait_for('message',timeout=0.2)
                
                C1 = U1.content
                print(C1)
                C2 = U2.content
                print(C2)                    
            else:
                break
        
        result = int(game.loc[C1, C2])
        # Prints integer value of result, outcome, and writes to the file based on the outcome of the game
        print(result)
        if result == 1:
            await message.channel.send(U1a + ' wins!')
            scoresg.loc[U1a, 'wins'] = scoresg.loc[U1a, 'wins'] + 1
            await message.channel.send(U1a + ' has ' + str(scoresg.loc[U1a, 'wins']) + ' wins.')
            scoresg.loc[U2a, 'losses'] = scoresg.loc[U2a, 'losses'] + 1
            await message.channel.send(U2a + ' has ' + str(scoresg.loc[U2a, 'losses']) + ' losses.')
            scoresg.to_csv("scores.csv")
        if result == 2:
            await message.channel.send(U2a + ' wins!')
            scoresg.loc[U2a, 'wins'] = scoresg.loc[U2a,'wins'] + 1
            await message.channel.send(U2a + ' has ' + str(scoresg.loc[U2a, 'wins']) + ' wins.')
            scoresg.loc[U1a, 'losses'] = scoresg.loc[U1a, 'losses'] + 1
            await message.channel.send(U1a + ' has ' + str(scoresg.loc[U1a, 'losses']) + ' losses.')
            scoresg.to_csv("scores.csv")
        if result == 0:
            await message.channel.send('Draw.')
            scoresg.loc[U1a, 'draws'] = scoresg.loc[U1a, 'draws'] + 1
            await message.channel.send(U1a + ' has ' + str(scoresg.loc[U1a, 'draws']) + ' draws.')
            scoresg.loc[U2a, 'draws'] = scoresg.loc[U2a, 'draws'] + 1
            await message.channel.send(U2a + ' has ' + str(scoresg.loc[U2a, 'draws']) + ' draws.')
            scoresg.to_csv("scores.csv")

    # If a user sends &statsall sends the entire data frame line by line in chat
    if message.content == '&statsall':

        # Reads in the scores from the scores.csv file
        scoresl = pd.read_csv("scores.csv", index_col="user")
        print(scoresl)
        print(scoresl)
        
        for i in range(len(scoresl)):
            await message.channel.send(scoresl.index[i])
            await message.channel.send('Wins:')
            await message.channel.send(scoresl.iloc[i,0])
            await message.channel.send('Draws:')
            await message.channel.send(scoresl.iloc[i,1])
            await message.channel.send('Losses:')
            await message.channel.send(scoresl.iloc[i,2])

    # If a user sends &statswins sends the wins column of the data frame with the corresponding names line by line in chat
    if message.content == '&statswins':
        
        scoresl = pd.read_csv("scores.csv", index_col="user")
        print(scoresl)
        
        for i in range(len(scoresl)):
            await message.channel.send(scoresl.index[i])
            await message.channel.send('Wins:')
            await message.channel.send(scoresl.iloc[i,0])

    # If a user sends &statsdraws sends the draws column of the data frame with the corresponding names line by line in chat
    if message.content == '&statsdraws':
        
        scoresl = pd.read_csv("scores.csv", index_col="user")
        print(scoresl)
        
        for i in range(len(scoresl)):
            await message.channel.send(scoresl.index[i])
            await message.channel.send('Draws:')
            await message.channel.send(scoresl.iloc[i,1])
    # If a user sends &statslosses sends the losses column of the data frame with the corresponding names line by line in chat        
    if message.content == '&statslosses':
        
        scoresl = pd.read_csv("scores.csv", index_col="user")
        print(scoresl)
        
        for i in range(len(scoresl)):
            await message.channel.send(scoresl.index[i])
            await message.channel.send('Losses:')
            await message.channel.send(scoresl.iloc[i,2])

    # If a user sends &win% calculates the message authors win% and send it in chat
    if message.content == '&win%':

        scoresl = pd.read_csv("scores.csv", index_col="user")
        a = str(message.author)
        print(a)

        # If a user has no scores in the scores.csv file sends a message in chat telling them they haven't played a game yet
        try:
            scoresl.loc[a,'wins']
        except KeyError:
            await message.channel.send("You haven't played yet!")
        else:
            aw = scoresl.loc[a,'wins']
            ad = scoresl.loc[a,'draws']
            al = scoresl.loc[a,'losses']
            win = str(((aw)/(aw+ad+al))*100)
            await message.channel.send(a + ' has a win percentage of:')
            await message.channel.send(win+"%")
             
    if message.content == '&hangman':
            wf = 0
            hints = 1
            secret_word = choose_word(wordlist)
            guessed_letters = []
            alphabet = string.ascii_lowercase
            i = 0
            warnings = 3
            t1 = str('Welcome to hangman! The word you are guessing contains ' + str(len(secret_word)) +  ' letters! You have 3 warnings left!')
            await message.channel.send(t1)
            while i <= 5:
                t2 = str('You have ' + str(6 - i) + ' guess(es) left and ' + str(hints) +' hint(s) left!')
                await message.channel.send(t2)
                U1 = await client.wait_for('message',timeout=60.0)
                guess = U1.content
                print(secret_word)
                if guess == '*' and hints > 0 and how_many_possible_matches(get_guessed_word(secret_word, guessed_letters)) <= 100:          
                    await message.channel.send('Here are some words which match the gaps that are currently filled')
                    await message.channel.send(show_possible_matches(get_guessed_word(secret_word, guessed_letters)))
                    hints -= 1
                    i -= 1
                elif guess == '*' and hints == 0:
                    await message.channel.send('You have no hints left!')
                    i -= 1
                elif guess == '*' and how_many_possible_matches(get_guessed_word(secret_word, guessed_letters)) > 100:
                    await message.channel.send('There are over 100 possible words which fit in those gaps try harder!')
                    i -= 1
                t7 = str('Available letters are: ' + get_available_letters(guessed_letters))
                await message.channel.send(t7)
                if (len(guess) != 1 or guess not in alphabet) and guess != '*':
                    await message.channel.send('That was not a valid letter!')
                    if warnings > 0:
                        warnings -= 1
                        i -= 1
                        t3 = str('You have ' + str(warnings) + ' warnings left!')
                        await message.channel.send(t3)
                    else:
                        await message.channel.send('You have lost a guess!')
                if guess in guessed_letters:
                    await message.channel.send('You have already guessed this letter!')
                    if warnings > 0:
                        warnings -= 1
                        i -= 1
                        t3 = str('You have ' + str(warnings) + ' warnings left!')
                        await message.channel.send(t3)
                    else:
                        await message.channel.send('You have lost a guess!')
                if guess in secret_word and guess not in guessed_letters:
                    t4 =str(guess + ' was in the word!')
                    await message.channel.send(t4)
                    i -= 1
                elif guess not in secret_word and guess in alphabet:
                    t5 =str(guess + ' was not in the word...')
                    await message.channel.send(t5)
                if len(guess) == 1 and guess in alphabet:
                    guessed_letters += guess
                t6 = str('Current word is: '+ get_guessed_word(secret_word, guessed_letters))
                print(t6)
                await message.channel.send(t6)
                if is_word_guessed(secret_word, guessed_letters) is True:
                    await message.channel.send('Congratulations you have won!')
                    t8 = str('Your score was: ' + str((6-i)*len(get_chars(secret_word))))
                    await message.channel.send(t8)
                    wf = 1
                    if hints == 0:
                        await message.channel.send('But you used a hint...')
                    break
                i += 1
            if wf == 0:
                await message.channel.send('You have lost the word was: '+secret_word)
                 
    if message.content == '&scrabblecomp':
        HAND_SIZE = 7
        total_score = 0
        substitute = 3
        no_hands = 1
        await message.channel.send('This is competitive so ' + str(no_hands) + ' hands will be played and your high score will be recorded.')
        await message.channel.send('You have ' + str(substitute) + ' substitute(s).')
        for i in range(int(no_hands)):
            hand = deal_hand(HAND_SIZE)
            await message.channel.send('Current hand: ' + display_hand(hand))
            if substitute > 0:
                await message.channel.send('Would you like to substiute a letter?')
                asksi = await client.wait_for('message',timeout=120.0)
                asks = asksi.content.lower()
                if asks == 'yes':
                    substitute -= 1
                    await message.channel.send('Enter the letter to replace')
                    handi = await client.wait_for('message',timeout=120.0)
                    handl = handi.content.lower()
                    hand = substitute_hand(hand, handl)
            score = 0
            while len(hand) > 0:
                await message.channel.send('Current hand: ' + display_hand(hand))
                await message.channel.send('Enter word, or "!!" when you are finished playing your hand:')
                wordi = await client.wait_for('message',timeout=120.0)
                word = wordi.content.lower()
                if word == '!!':
                    break
                if is_valid_word(word, hand, word_list) == True:
                    word_score = get_word_score(word, len(hand))
                    await message.channel.send(word + ' earned ' + str(word_score) + ' points.')
                    score += word_score
                    await message.channel.send('Total score for this hand: ' + str(score))
                else:
                    await message.channel.send('That is not a valid word. Please choose another word.')
                hand = update_hand(hand, word)
            await message.channel.send('Total score for this hand: ' + str(score))
            total_score += score
        await message.channel.send('The total score for all ' + str(no_hands) + ' hands: ' + str(total_score))
        Ua = str(message.author)
        print(Ua)
        highscores = pd.read_csv("highscores.csv", index_col="user")
        print(highscores.loc[Ua])
        try:
            print(highscores.loc[Ua])
            highscores.loc[Ua]
        except KeyError:
            print('That user does not exist yet, creating user now.')
            highscores.loc[Ua, :] = [0]
            print(highscores.loc[Ua])
        u_highscore = highscores.loc[Ua, 'highscore']
        print(u_highscore)
        print(total_score)
        if total_score > u_highscore:
            highscores.loc[Ua, 'highscore'] = total_score
            highscores.to_csv("highscores.csv")
            print(highscores.loc[Ua])
            await message.channel.send('You have achieved a new personal highscore!')
             
    if message.content == '&highscores':
        
        scoresl = pd.read_csv("highscores.csv", index_col="user")
        print(scoresl)
        
        for i in range(len(scoresl)):
            await message.channel.send(scoresl.index[i])
            await message.channel.send('Highscore:')
            await message.channel.send(scoresl.iloc[i,0])
      
        

client.run(TOKEN)




