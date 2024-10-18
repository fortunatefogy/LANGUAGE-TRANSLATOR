from tkinter import *
from customtkinter import *
import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from PIL import Image
import googletrans
from googletrans import Translator
import speech_recognition as sr
# Ensure this line is included
import pyttsx3
from gtts import gTTS
from langdetect import detect, DetectorFactory

# Ensure consistent results for language detection
DetectorFactory.seed = 0
# app setup-------------------------------------------------------
app = CTk()
app.geometry('1350x600')
app.after(0, lambda: app.state('zoomed'))
ctk.set_default_color_theme("green")
app.wm_attributes("-topmost", 1)


# functions*******************************************************


# translate function----------------------------------------------

def translate():
    global textt
    textt = input_text.get(1.0, END)
    if textt.strip() == "":
        CTkMessagebox(mainframe,
                      title="Message",
                      message="Please give input",
                      button_color="#0061ff",
                      fg_color="#ffffff",
                      bg_color="#ffffff",
                      border_width=1,
                      border_color="#000000",
                      text_color="#000000",
                      width=50,
                      height=50,
                      )
        return
    t = Translator()
    try:
        cancel_button.configure(cancel_button.place(x=560, y=12))
        global transtext
        transtext = t.translate(textt, src=language1.get(), dest=language2.get())
        global transtext_text
        transtext_text = transtext.text
        output_text.delete(1.0, END)
        output_text.insert(END, transtext_text)
    except:
        CTkMessagebox(mainframe,
                      title="Message",
                      message="Select language",
                      fg_color="#ffffff",
                      bg_color="#ffffff",
                      border_width=3,
                      border_color="#f5f5f5",
                      text_color="#000000",
                      width=200,
                      height=100,
                      button_color="#0061ff"
                      )


# clear function-------------------------------------------------------

def clear():
    input_text.delete(0.0, 'end')
    output_text.delete(0.0, 'end')
    cancel_button.configure(cancel_button.place(x=600, y=10))


# cancel input---------------------------------------------------------

def cancel_input():
    input_text.delete(0.0, 'end')
    cancel_button.configure(cancel_button.place(x=600, y=10))


# switch values--------------------------------------------------------

def switch():
    input = input_text.get(1.0, END)
    output = output_text.get(1.0, END)
    input_text.delete(1.0, END)
    output_text.delete(1.0, END)
    output_text.insert(END, input)
    input_text.insert(END, output)
    lang1 = language2.get()
    lang2 = language1.get()
    language1.set(lang1)
    language2.set(lang2)


def switch_tabs():
    pass


# speech to text function----------------------------------------------

def speech():
    recognizer = sr.Recognizer()
    while True:
        try:
            with sr.Microphone() as mic:
                # Show the message box before starting to listen
                # CTkMessagebox(
                #     mainframe,
                #     title="Message",
                #     # message="Please give input",
                #     fg_color="#ffffff",
                #     bg_color="#ffffff",
                #     border_width=3,
                #     border_color="#f5f5f5",
                #     text_color="#000000",
                #     width=200,
                #     height=100,
                #     button_color="#0061ff"
                # )

                # Adjust for ambient noise and listen
                recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                audio = recognizer.listen(mic)

            # Recognize speech using Google Web Speech API
            text = recognizer.recognize_google(audio)
            text = text.lower()
            input_text.insert(END, " " + text + ".")  # Insert recognized text into the input box

            # Close the message box after receiving input
            break  # Exit the while loop after successful recognition
        except sr.UnknownValueError:
            # If the audio is unintelligible, you can choose to continue silently
            continue  # Continue listening for speech
        except sr.RequestError as e:
            # Handle request error (API unavailable or unreachable)
            CTkMessagebox(
                mainframe,
                title="Error",
                message="Could not request results from Google Speech Recognition service; {0}".format(e),
                fg_color="#ffffff",
                bg_color="#ffffff",
                border_width=3,
                border_color="#f5f5f5",
                text_color="#000000",
                width=300,
                height=100,
                button_color="#ff0000"
            )
            break  # Exit the loop on error


# input text copy------------------------------------------------------

def copy_text1():
    app.clipboard_clear()
    copy_text1 = input_text.get(1.0, END)
    app.clipboard_append(copy_text1)
    ack1 = CTkMessagebox(container,
                         title="",
                         message="Text Copied !",
                         icon="check",
                         fg_color="#ffffff",
                         bg_color="#ffffff",
                         border_width=1,
                         border_color="#000000",
                         text_color="#000000",
                         width=50,
                         height=50,
                         button_color="#ffffff",
                         button_text_color="#ffffff"
                         )
    app.after(1000, ack1.destroy)


# output text copy------------------------------------------------------

def copy_text2():
    app.clipboard_clear()
    copy_text2 = output_text.get(1.0, END)
    app.clipboard_append(copy_text2)
    ack2 = CTkMessagebox(container,
                         title="",
                         message="Text Copied !",
                         icon="check",
                         fg_color="#ffffff",
                         bg_color="#ffffff",
                         border_width=3,
                         border_color="#000000",
                         text_color="#000000",
                         width=50,
                         height=50,
                         corner_radius=30,
                         button_color="#ffffff",
                         button_text_color="#ffffff"
                         )
    app.after(1000, ack2.destroy)


# text to speech function------------------------------------------------

def talk():
    talk = pyttsx3.init()
    answer = input_text.get(1.0, END)
    talk.say(answer)
    talk.runAndWait()
    language = 'en'
    output = gTTS(text=answer, lang=language, slow=False)
    output.save("output.mp3")


import pyttsx3
from gtts import gTTS
from langdetect import detect, DetectorFactory
import pygame
import os

# Set a seed for consistent language detection
DetectorFactory.seed = 0

import tempfile


def talk2():
    talk = pyttsx3.init()
    answer = output_text.get(1.0, END).strip()

    if answer:
        try:
            language = detect(answer)
            print(f"Detected language: {language}")  # Debug output

            # Speak the text using pyttsx3
            talk.say(answer)
            talk.runAndWait()

            # Convert text to speech using gTTS
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_file:
                output = gTTS(text=answer, lang=language, slow=False)
                output.save(temp_file.name)  # Save to a temporary file
                temp_file_path = temp_file.name  # Store the temp file path

            # Initialize pygame mixer
            pygame.mixer.init()
            pygame.mixer.music.load(temp_file_path)  # Load the temporary audio file
            pygame.mixer.music.play()  # Play the audio file

            # Optionally, you can wait until the music finishes
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)

        except Exception as e:
            print(f"Error during processing: {e}")
            # Fallback to English if detection fails or an error occurs
            language = 'en'
            talk.say(answer)
            talk.runAndWait()

            # Use temporary file for fallback audio as well
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_file:
                output = gTTS(text=answer, lang=language, slow=False)
                output.save(temp_file.name)  # Save to a temporary file
                temp_file_path = temp_file.name  # Store the temp file path

            # Play the English version
            pygame.mixer.init()
            pygame.mixer.music.load(temp_file_path)
            pygame.mixer.music.play()

            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
    else:
        print("No text to convert to speech.")


# to light theme function-------------------------------------------------

def light():
    mainframe.configure(fg_color="#ffffff")
    switch_theme.configure(command=change_theme)
    switch_theme.configure(text="Dark")
    container.configure(fg_color="#ffffff")


# change theme function---------------------------------------------------

def change_theme():
    container.configure(fg_color="#191919")
    switch_theme.configure(command=light)
    switch_theme.configure(text="Light")
    mainframe.configure(fg_color="#191919")


# get history-------------------------------------------------------------
def display_file():
    input_text.delete(1.0, END)
    input_text.insert(END, textt)
    output_text.delete(1.0, END)
    output_text.insert(END, transtext_text)


# widgets*****************************************************************

# parent frame------------------------------------------------------------
mainframe = CTkFrame(app,
                     width=1536,
                     height=842,
                     corner_radius=0,
                     fg_color="#ffffff"
                     )
mainframe.place(relx=0.5, rely=0.5, anchor="c")

# header-----------------------------------------------------------------

# header frame
head1 = CTkFrame(mainframe,
                 width=500,
                 height=40,
                 corner_radius=0,
                 fg_color="#ffffff"
                 )
head1.place(y=0)

# shadow
shadow = ctk.CTkFrame(mainframe,
                      width=1596,
                      height=4,
                      fg_color="#f5f5f5",
                      corner_radius=0
                      )
shadow.place(x=0, y=55)

# header label
label1 = CTkLabel(mainframe,
                  text="Translate",
                  bg_color="#ffffff",
                  text_color="#000000",
                  font=('poppins', 23)
                  )
label1.place(x=50, y=13)

# icon
icon = ctk.CTkImage(light_image=Image.open("images/icon2.png"), size=(25, 25))
icon_label = ctk.CTkLabel(mainframe, image=icon, text="", bg_color="#ffffff")
icon_label.place(x=20, y=12)

# parent container---------------------------------------------------------

container = CTkFrame(mainframe,
                     width=1350,
                     height=600,
                     corner_radius=0,
                     fg_color="#ffffff",
                     border_width=1,
                     border_color="#ffffff"
                     )
container.place(relx=0.5, rely=0.5, anchor="c")

# center aligner-----------------------------------------------------------

# aligner=CTkFrame(container,
#     width=2,
#     height=580,
#     corner_radius=0,
#     fg_color="#ffffff"
#     )
# aligner.place(relx=0.5,rely=0.5,anchor="c")


# theme toggle--------------------------------------------------------------

# segemented_button_var = ctk.StringVar(value="1")
# switch_theme = CTkButton(app,
#     text="Dark",
#     corner_radius=20,
#     bg_color="#ffffff",
#     fg_color="#f5f5f5",
#     height=35,
#     width=123,
#     command=change_theme
#     )
# switch_theme.place(x=1400,y=10)


# language values-----------------------------------------------------------

language = googletrans.LANGUAGES
languagev = list(language.values())
lang1 = language.keys()


# source language container-------------------------------------------------

def english():
    English.configure(border_width=2, border_color="#000000")
    Malayalam.configure(border_color="#ffffff")
    Hindi.configure(border_color="#ffffff")
    global choose1
    choose1.configure(choose1.place(x=21, y=10))
    set = "english"
    language1.set(set)


def malayalam():
    Malayalam.configure(border_width=2, border_color="#000000")
    English.configure(border_color="#ffffff")
    Hindi.configure(border_color="#ffffff")
    global choose1
    choose1.configure(choose1.place(x=21, y=10))
    set = "malayalam"
    language1.set(set)


def hindi():
    temp = language1.get()
    Hindi.configure(border_width=2, border_color="#000000")
    English.configure(border_color="#ffffff")
    Malayalam.configure(border_color="#ffffff")
    global choose1
    choose1.configure(choose1.place(x=21, y=10))
    set = "hindi"
    language1.set(set)


def kill_choose1(event):
    global choose1
    global language1
    choose1.configure(choose1.place(x=100, y=100))
    Hindi.configure(border_color="#ffffff")
    English.configure(border_color="#ffffff")
    Malayalam.configure(border_color="#ffffff")


language_container = CTkFrame(container,
                              fg_color="#ffffff",
                              bg_color="#ffffff",
                              height=35,
                              width=500,
                              corner_radius=20
                              )
language_container.place(x=64, y=55)

language = googletrans.LANGUAGES
languagev = list(language.values())
lang1 = language.keys()

English = ctk.CTkButton(language_container,
                        text="English",
                        height=36,
                        width=100,
                        command=english,
                        fg_color="#ffffff",
                        hover_color="#f5f5f5",
                        text_color="#000000",
                        corner_radius=20,
                        font=('poppins', 13, 'bold')
                        )
English.place(x=0, y=0)

Malayalam = ctk.CTkButton(language_container,
                          text="Malayalam",
                          height=35, width=85,
                          command=malayalam,
                          fg_color="#ffffff",
                          hover_color="#f5f5f5",
                          text_color="#000000",
                          corner_radius=20, font=('poppins', 13, 'bold'),
                          )
Malayalam.place(x=110, y=0)

Hindi = ctk.CTkButton(language_container,
                      text="Hindi",
                      height=36,
                      width=85,
                      fg_color="#ffffff",
                      hover_color="#f5f5f5",
                      text_color="#000000",
                      corner_radius=20,
                      font=('poppins', 13, 'bold'),
                      command=hindi
                      )
Hindi.place(x=220, y=0)


# destination language container---------------------------------------------------

def english2():
    English2.configure(border_width=2, border_color="#000000")
    Malayalam2.configure(border_color="#ffffff")
    Hindi2.configure(border_color="#ffffff")
    global choose2
    choose2.configure(choose2.place(x=21, y=10))
    set2 = "english"
    language2.set(set2)


def malayalam2():
    Malayalam2.configure(border_width=2, border_color="#000000")
    English2.configure(border_color="#ffffff")
    Hindi2.configure(border_color="#ffffff")
    global choose2
    choose2.configure(choose2.place(x=21, y=10))
    set2 = "malayalam"
    language2.set(set2)


def hindi2():
    Hindi2.configure(border_width=2, border_color="#000000")
    English2.configure(border_color="#ffffff")
    Malayalam2.configure(border_color="#ffffff")
    global choose2
    choose2.configure(choose2.place(x=21, y=10))
    set2 = "hindi"
    language2.set(set2)


def kill_choose2(event):
    global choose2
    global language2
    choose2.configure(choose2.place(x=100, y=100))
    Hindi2.configure(border_color="#ffffff")
    English2.configure(border_color="#ffffff")
    Malayalam2.configure(border_color="#ffffff")


language_container2 = CTkFrame(container,
                               fg_color="#ffffff",
                               bg_color="#ffffff",
                               height=35, width=500,
                               corner_radius=20
                               )
language_container2.place(x=690, y=55)

language = googletrans.LANGUAGES
languagev = list(language.values())
lang1 = language.keys()

English2 = ctk.CTkButton(language_container2,
                         text="English",
                         height=36, width=100,
                         fg_color="#ffffff",
                         hover_color="#f5f5f5",
                         text_color="#000000",
                         corner_radius=20, font=('poppins', 13, 'bold'),
                         command=english2
                         )
English2.place(x=0, y=0)

Malayalam2 = ctk.CTkButton(language_container2,
                           text="Malayalam",
                           height=35, width=85,
                           fg_color="#ffffff",
                           hover_color="#f5f5f5",
                           text_color="#000000",
                           corner_radius=20,
                           font=('poppins', 13, 'bold'),
                           command=malayalam2
                           )
Malayalam2.place(x=110, y=0)

Hindi2 = ctk.CTkButton(language_container2,
                       text="Hindi",
                       height=36,
                       width=85,
                       fg_color="#ffffff",
                       hover_color="#f5f5f5",
                       text_color="#000000",
                       corner_radius=20,
                       font=('poppins', 13, 'bold'),
                       command=hindi2,
                       )
Hindi2.place(x=220, y=0)

# language values-----------------------------------------------------------

language = googletrans.LANGUAGES
languagev = list(language.values())
lang1 = language.keys()

# source language selector--------------------------------------------------

a = ctk.StringVar()
language1 = ctk.CTkComboBox(language_container,
                            width=125,
                            height=36,
                            corner_radius=20,
                            variable=a,
                            fg_color="#f5f5f5",
                            text_color="#000000",
                            border_width=2,
                            border_color="#f5f5f5",
                            button_color="#f5f5f5",
                            button_hover_color="#f5f5f5",
                            values=languagev,
                            justify=CENTER,
                            command=kill_choose1,
                            font=('poppins', 13, 'bold')
                            )
language1.set(" Choose")
language1.place(x=320, y=0)

choose1 = CTkLabel(language1,
                   text="Choose",
                   text_color="#000000",
                   bg_color="#f5f5f5",
                   height=15,
                   width=68,
                   corner_radius=20,
                   font=('poppins', 13, 'bold'))
choose1.place()

# destination language selector-------------------------------------------

l = ctk.StringVar()
language2 = ctk.CTkOptionMenu(language_container2,
                              width=125,
                              height=36,
                              corner_radius=20,
                              variable=l,
                              fg_color="#f5f5f5",
                              text_color="#000000",
                              button_color="#f5f5f5",
                              button_hover_color="#f5f5f5",
                              values=languagev,
                              command=kill_choose2,
                              font=('poppins', 13, 'bold')
                              )
language2.set(" Choose")
language2.place(x=320, y=0)

choose2 = CTkLabel(language2,
                   text="Choose",
                   text_color="#000000",
                   bg_color="#f5f5f5",
                   height=15,
                   width=68,
                   corner_radius=20,
                   font=('poppins', 13, 'bold'))
choose2.place()

# input field--------------------------------------------------------------

input_text = ctk.CTkTextbox(container,
                            width=600,
                            height=350,
                            corner_radius=32,
                            text_color="#5f6368",
                            fg_color='#ffffff',
                            border_color="#d6d6d6",
                            border_width=1.5,
                            pady=10,
                            padx=10,
                            font=('poppins', 20)
                            )
input_text.place(x=64, y=108)

# cancel button
cancel = ctk.CTkImage(light_image=Image.open("images/cancel.png"), size=(15, 15))
cancel_button = ctk.CTkButton(input_text,
                              image=cancel, text="",
                              width=5,
                              height=5,
                              corner_radius=10,
                              fg_color="#ffffff",
                              hover_color="#f4f4f4",
                              command=cancel_input
                              )
cancel_button.place()

toolbox = ctk.CTkFrame(input_text,
                       width=120,
                       height=65,
                       corner_radius=20,
                       fg_color='#f4f4f4',
                       )
toolbox.place(x=16, y=268)

# copy button1
copy = ctk.CTkImage(light_image=Image.open("images/copy.png"), size=(28, 28))
copy_button1 = ctk.CTkButton(input_text,
                             image=copy,
                             text="",
                             width=5,
                             height=5,
                             corner_radius=30,
                             fg_color="#ffffff",
                             hover_color="#ffffff",
                             command=copy_text1
                             )
copy_button1.place(x=540, y=285)

# speak button
audio = ctk.CTkImage(light_image=Image.open("images/speak.png"), size=(30, 30))
audio_button = ctk.CTkButton(toolbox,
                             image=audio, text="",
                             width=5,
                             height=5,
                             corner_radius=30,
                             fg_color="#f4f4f4",
                             hover_color="#f4f4f4",
                             command=speech
                             )
audio_button.place(x=12, y=13)

# talk button
speak = ctk.CTkImage(light_image=Image.open("images/talk.png"), size=(50, 50))
speak_button = ctk.CTkButton(toolbox,
                             image=speak, text="",
                             width=5, height=5,
                             corner_radius=30,
                             fg_color="#f4f4f4",
                             hover_color="#f4f4f4",
                             command=talk
                             )
speak_button.place(x=55, y=3)

# output field-----------------------------------------------------------------
output_text = ctk.CTkTextbox(container,
                             width=600,
                             height=350,
                             corner_radius=32,
                             text_color="#37373d",
                             fg_color='#F5F5F5',
                             border_color='#F5F5F5',
                             border_width=1,
                             pady=10,
                             padx=10,
                             font=('poppins', 20)
                             )
output_text.place(x=689, y=108)
output_text.insert(END, 'Translated text here...')

# copy button2
copy = ctk.CTkImage(light_image=Image.open("images/copy.png"), size=(28, 28))
copy_button2 = ctk.CTkButton(output_text,
                             image=copy, text="",
                             width=5, height=5,
                             corner_radius=30,
                             fg_color="#f4f4f4",
                             hover_color="#f4f4f4",
                             command=copy_text2
                             )
copy_button2.place(x=540, y=285)

# speaker button
speak = ctk.CTkImage(light_image=Image.open("images/talk.png"), size=(50, 50))
speak_button = ctk.CTkButton(output_text,
                             image=speak, text="",
                             width=5, height=5,
                             corner_radius=30,
                             fg_color="#f5f5f5",
                             hover_color="#f4f4f4",
                             command=talk2
                             )
speak_button.place(x=14, y=276)

# footer-------------------------------------------------------------------------

# switch toggle
# switchimg = ctk.CTkImage(light_image=Image.open("images/history.png"),size=(55, 55))
# switch_button = ctk.CTkButton(container, image=switchimg,text="",width=50,height=50,fg_color="#ffffff",hover_color="#ffffff",command= lambda : [switch(),switch_tabs()])
# switch_button.place(x=1140,y=489)

# history toggle
history = ctk.CTkImage(light_image=Image.open("images/history.png"), size=(55, 55))
history_button = ctk.CTkButton(container,
                               image=history, text="",
                               width=50, height=50,
                               fg_color="#ffffff",
                               hover_color="#ffffff",
                               command=display_file
                               )
history_button.place(x=1226, y=489)

# translate button
# translate_icon = ctk.CTkImage(light_image=Image.open("images/go.png"),size=(20, 20))
traslate_button = ctk.CTkButton(container,
                                text="Translate",
                                # image=translate_icon,
                                width=110, height=43,
                                corner_radius=30,
                                fg_color="#000000",
                                text_color="#ffffff",
                                hover_color="#000000",
                                command=translate
                                )
traslate_button.place(x=66, y=500)

# clear button
# translate = ctk.CTkImage(light_image=Image.open("images/close.png"),size=(20, 20))
traslate_button = ctk.CTkButton(container,
                                text="Clear",
                                width=110, height=43,
                                corner_radius=30,
                                fg_color="#ffffff",
                                border_width=2,
                                border_color="#000000",
                                text_color="#000000",
                                hover_color="#ffffff",
                                command=clear
                                )
traslate_button.place(x=195, y=500)

app.mainloop()












