import random
import pygame
import time
from math import floor
from database_builder import retrieve_spotify_data
import pandas
import sys
from spotify_genres import available_genres


def start_game(genre, year, difficulty):
    df = pandas.read_csv('data/songs_database.csv')
    filtered_df = df.loc[(df['genre'] == genre) & (df['year'] == year)]
    songs_to_play = filtered_df['title'].values.tolist()
    random.shuffle(songs_to_play)
    score = 0
    exit = False
    for i, song in enumerate(songs_to_play):
        print(f'Now playing song {i}/{len(songs_to_play)}.\n')
        play_song(song)
        if difficulty == 'Easy':
            print(f"Hint: {song[0:4]}...")
        title = input("What song is it? 🎶 (Type 'r' if you want to listen to the song again.)\n").lower()
        if title == 'r':
            play_song(song)
            title = input("What song is it? 🎶\n").lower()
        if title == song.lower():
            score += 1
            print('Nice one!\n')
        else:
            print('Sorry, you got that wrong.\n')
        
        if difficulty == 'Easy':
            print(f"Hint: {df[df['title'] == song]['artist'].values[0][0:4]}...")
        artist = input("What's the artist? 🧑‍🎤\n").lower()
        if artist == df[df['title'] == song]['artist'].values[0].lower():
            score += 1
            print('Nice one!\n')
        else:
            print('Sorry, you got that wrong.\n')

        if difficulty == 'Easy':
            print(f"Hint: {df[df['title'] == song]['album'].values[0][0:4]}...")
        album = input("And what's the album? 🎼 (You can type '(exit)' at the end to computate this answer and stop the game)\n").lower()
        if '(exit)' in album:
            album = album[0:album.find(' (exit)')]
            exit = True
        if album == df[df['title'] == song]['album'].values[0].lower():
            score += 1
            print('Nice one!\n')
        else:
            print('Sorry, you got that wrong.\n')
        if exit:
            sys.exit(f'\nThank you for playing the game. Your final score is {score} out of {(i+1)*3}.')
        
        print('________________________')
        print(f'|Total score so far: {score} out of {(i+1)*3}.|')
        print('‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾\n')
        time.sleep(1.5)

    sys.exit(f'\nThank you for playing the game. Your final score is {score} out of {(i+1)*3}.')


def get_difficulty():
    difficulty_options = ['Easy', 'Normal', "Hard"]
    difficulty = input("_______________________________________________________________________________________________________\n"
                       "|Please select the difficulty you would like to play:                                                 |\n"
                       "|Easy: You select the genre and the decade, and the first 4 letters of each guess will be revealed.   |\n"
                       "|Normal: You select the genre and the decade, and you won't get any hints.                            |\n"
                       "|Hard: You can select only the genre, the decade will be random, ranging from the 90s to 2020.        |\n"
                       "¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯\n"
                       "Choice: ").title().strip()
    if difficulty not in difficulty_options:
        print('Invalid input, please try again.')
        get_difficulty()
    else:
        return difficulty


def main():
    difficulty = get_difficulty()
    genre = get_genre()
    if difficulty != 'Hard':
        decade = get_decade()
    else:
        decade = random.choice([1990, 2000, 2010, 2020])
    retrieve_spotify_data(genre, decade)
    
    print('\n')
    print('-'*30)
    print('Thank you for waiting')
    confirmation = input('Do you want to start the game? (y/n)? ')
    if confirmation == 'y':
        start_game(genre, decade, difficulty)
    else:
        sys.exit('The program has been shut down.')




main()



