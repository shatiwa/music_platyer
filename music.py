import os
import threading
import time
from tkinter import *
import tkinter.messagebox
from tkinter import filedialog, ttk

import pygame
from mutagen.mp3 import MP3
from pygame import mixer

root = Tk()
root.title('shashank player')

sta = Label(root, text="Playing file", relief=SUNKEN, anchor=W, font='Times 15 bold italic')
sta.pack(side='bottom', fill=X)

# Create the menubar
menubar = Menu(root)
root.config(menu=menubar)
pygame.mixer.init()
play = PhotoImage(file='play.png')
stop = PhotoImage(file='stop.png')
pause = PhotoImage(file='pause.png')
rewind = PhotoImage(file='rewind.png')
mute = PhotoImage(file='mute.png')
volume = PhotoImage(file='volume.png')

# Create the submenu
subMenu = Menu(menubar, tearoff=0)

index = 0
playlist = []


def browse_file():
    global filename_path
    filename_path = filedialog.askopenfilename()
    add_to_playlist(filename_path)


def add_to_playlist(f):
    global index
    f = os.path.basename(f)
    playlistbox.insert(index, f)
    playlist.insert(index, filename_path)
    index += 1


def delete_file():
    select_song = playlistbox.curselection()
    select_song = int(select_song[0])
    playlistbox.delete(select_song)
    playlist.pop(select_song)


menubar.add_cascade(label="File", menu=subMenu)
subMenu.add_command(label="Open", command=browse_file)
subMenu.add_command(label="Exit", command=root.destroy)


def about_us():
    tkinter.messagebox.showinfo('Our Title', 'This music player is developed by shashank tiwari')


subMenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Help", menu=subMenu)
subMenu.add_command(label="About Us", command=about_us)

leftframe = Frame(root)
leftframe.pack(side=LEFT, padx=30)

playlistbox = Listbox(leftframe)
playlistbox.pack()

addBtn = ttk.Button(leftframe, text="+ Add", command=browse_file)
addBtn.pack(side=LEFT)

delBtn = ttk.Button(leftframe, text="- Del", command=delete_file)
delBtn.pack(side=LEFT)

rightframe = Frame(root)
rightframe.pack()

topframe = Frame(rightframe)
topframe.pack()

filetext = ttk.Label(topframe, text="This is my player made by using python")
filetext.pack(pady=10)

name_song = ttk.Label(topframe, text="Displays name of played song")
name_song.pack(pady=10)

total_time = ttk.Label(topframe, text="Total length - 00:00")
total_time.pack(pady=10)

current_time = ttk.Label(topframe, text="Current Time - 00:00")
current_time.pack(pady=10)

middleframe = Frame(rightframe)
middleframe.pack(padx=10, pady=10)


def show_time(play):
    name_song['text'] = "Playing music" + ' - ' + os.path.basename(play)
    file_data = os.path.splitext(play)
    if file_data[1] == '.mp3':
        audio = MP3(play)
        total_length = audio.info.length()
    else:
        a = pygame.mixer.Sound(play)
        total_length = a.get_length()
    mins, secs = divmod(total_length, 60)
    mins = round(mins)
    secs = round(secs)
    time_format = '{:02d}:{:02d}'.format(mins, secs)
    total_time['text'] = "Total length - " + time_format

    t1 = threading.Thread(target=start_count, args=(total_length,))
    t1.start()


def start_count(total_length):
    global paused, c
    k = total_length
    while total_length and pygame.mixer.music.get_busy():
        if paused:
            continue
        else:
            mins, secs = divmod(total_length, 60)
            mins = round(mins)
            secs = round(secs)
            time_format = '{:02d}:{:02d}'.format(mins, secs)
            current_time['text'] = "Total length - " + time_format
            time.sleep(1)
            total_length -= 1


def play_song():
    global paused, c
    if paused:  # check whether pause function is called or
        pygame.mixer_music.unpause()
        sta['text'] = "Music Resumed"
        paused = FALSE
    else:
        try:
            c = 1
            pygame.mixer_music.stop()
            time.sleep(1)
            select_song = playlistbox.curselection()
            select_song = int(select_song[0])
            play = playlist[select_song]
            print(play)
            pygame.mixer.music.load(play)
            pygame.mixer.music.play()
            sta['text'] = "Playing music"
            show_time(play)
        except:
            tkinter.messagebox.showerror('Message Dialog box', 'File not selected')


def stop_song():
    pygame.mixer.music.stop()
    sta['text'] = "Music Stopped"


paused = FALSE


def pause_song():
    global paused
    paused = TRUE
    pygame.mixer.music.pause()
    sta['text'] = "Music Paused"


def set_v(val):
    x = float(val) / 100  # divide by 100 is done be
    pygame.mixer.music.set_volume(x)


c = 0


def rewind_song():
    play_song()
    sta['text'] = "Music Rewinded"


n = 0


def mute_song():
    global n
    if n == 0:
        playV.config(image=mute)
        pygame.mixer.music.set_volume(0)
        scale.set(0)
        sta['text'] = "Music Muted"
        n = 1
    elif n == 1:
        playV.config(image=volume)
        scale.set(50)
        pygame.mixer.music.set_volume(0.5)
        sta['text'] = "Music Playing"
        n = 0


playB = ttk.Button(middleframe, image=play, command=play_song)
playB.grid(row=0, column=0, padx=10)

playS = ttk.Button(middleframe, image=stop, command=stop_song)
playS.grid(row=0, column=1, padx=10)

playP = ttk.Button(middleframe, image=pause, command=pause_song)
playP.grid(row=0, column=2, padx=10)

botframe = Frame(rightframe)
botframe.pack()

playR = ttk.Button(botframe, image=rewind, command=rewind_song)
playR.grid(row=0, column=0, padx=10)

mute = PhotoImage(file='mute.png')
volume = PhotoImage(file='volume.png')
playV = ttk.Button(botframe, image=volume, command=mute_song)
playV.grid(row=0, column=1, padx=10)

scale = ttk.Scale(botframe, from_=0, to=100, orient=HORIZONTAL, command=set_v)
scale.set(45)
scale.grid(row=0, column=2, pady=20, padx=20)


def on_pressing_X_button():
    stop_song()
    root.destroy()


root.protocol("WM_DELETE_WINDOW", on_pressing_X_button)
root.mainloop()
