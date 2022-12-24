import csv
from tkinter import *
import time
from gtts import gTTS
from english_words import english_words_set
import random
from pygame import mixer

mixer.init()


def make_sound(music):
    mixer.music.load(music)
    mixer.music.play()


class SpellingMaster:
    def __init__(self):
        self.music = None
        self.text_entry = None
        self.word = "apple"
        self.name_box = None
        self.name = "Guest"

        self.root = Tk()

        self.ans = StringVar()
        self.score = IntVar()
        self.root.title("Spelling Master")
        # self.width = str(self.root.winfo_screenwidth())
        # self.height = str(self.root.winfo_screenheight())
        self.width = "800"
        self.height = "600"
        self.root.geometry(self.width + 'x' + self.height)
        self.root.resizable(width=False, height=False)
        # self.root.geometry("800x600")
        self.bg = PhotoImage(file="assets/loading.png")
        self.bgl = Label(self.root, image=self.bg)
        self.bgl.place(x=0, y=0)
        self.loading()
        # self.start_btn = Button(self.root, text="Start", command=self.login)
        # self.start_btn.place(x=str(int(self.width) / 2),
        #                      y=str(int(self.height) / 2))
    
    def loading(self):
        self.root.after(2000, self.login)

    def readcsvdataset(self):
        with open("archive/easy_set.csv") as f:
            csvreader = csv.reader(f)
            for row in csvreader:
                print(row[0])
                self.makeaudiofiles(row[0])

    def readwordset(self):
        wordset = []
        c = 0
        with open("archive/easy_set.csv") as f:
            creader = csv.reader(f)
            for i in creader:
                if c < 990:
                    wordset.append(i[0])
                else:
                    break
                c = c + 1
        return wordset

    def makeaudiofiles(self, word):
        tts = gTTS(text=word, lang='en', slow=False)
        music = "tmp/"+word+'.mp3'
        tts.save(music)

    def login(self):
        self.clean()
        form_frame = Frame(self.root)
        form_frame.place(x=str(int(self.width) / 2),
                        y=str(int(self.height) / 2), anchor=CENTER)

        name_label = Label(form_frame, text="Type your name", font=("Arial Bold", 14))
        name_label.pack(side=TOP, pady=10)

        self.name_box = Entry(form_frame, width=30, font=("Arial Bold", 14), justify=CENTER)
        self.name_box.focus_set()
        self.name_box.bind('<Return>', lambda e : self.play())
        self.name_box.pack(ipadx=40, ipady=10)

        login_btn = Button(form_frame, text="Login", command=self.play)
        login_btn.pack(side=BOTTOM, fill=BOTH)

    def play(self):
        name = self.name_box.get()
        if name!= '':
            self.name = name
        self.clean()

        self.bg = PhotoImage(file='assets/gamebg.png')
        playbg = Label(self.root, image=self.bg)
        playbg.place(x=0, y=0)

        heading = Label(
            self.root, text="Welcome ".upper() + self.name.upper(), font=("Arial Bold", 30), bg="white", relief=GROOVE)
        heading.place(x=str(int(self.width) / 2),
                         y=str(int(self.height) / 10), anchor=CENTER)

        type_frame = Frame(self.root)
        type_frame.place(x=str(int(self.width) / 2),
                         y=str(int(self.height) / 2), anchor=CENTER)
        btn_bg = PhotoImage(file='assets/speaker.png')
        sound_btn = Button(type_frame, text="S", image=btn_bg, command=lambda : make_sound(self.music))
        sound_btn.image = btn_bg
        sound_btn.pack(side=TOP)

        text_label = Label(type_frame, text="Type below", bg='white', font=("Arial bold", 12))
        text_label.pack(side=TOP, pady=20)

        self.text_entry = Entry(type_frame, width=30, font=('Arial 20'), justify=CENTER)
        self.text_entry.focus()
        self.text_entry.bind('<Return>', lambda e : self.check())
        self.text_entry.pack(fill=X, ipadx=100, ipady=10)

        self.next_word()

        check_btn = Button(type_frame, text="Check", command=self.check)
        check_btn.pack(side=BOTTOM, fill=BOTH)

    def next_word(self):
        # word_set = self.readcsvdataset()
        word_set = self.readwordset()
        self.word = random.choice(list(word_set))
        print(self.word)
        # tts = gTTS(text=self.word, lang='en', slow=False)
        self.music = "tmp/"+self.word+'.mp3'
        # tts.save(self.music)
        make_sound(self.music)

    def check(self):
        
        label_frame = Frame(self.root)
        label_frame.place(x=str(int(self.width)/2),
                        y=str(int(self.height)/2+200),anchor=E, relwidth=0.5)
        score_frame = Frame(self.root)
        score_frame.place(x=str(int(self.width)/2),
                        y=str(int(self.height)/2+200),anchor=W, relwidth=0.5, height=100)
        if self.text_entry.get().lower() == self.word.lower():
            self.next_word()
            # self.ans.set("Correct spelling.")
            img = PhotoImage(file='assets/right.png')
            right_label = Label(label_frame, image=img)
            right_label.image = img
            # right_label.place(x=0, y=500)
            right_label.pack()
            self.score.set(self.score.get() + 1)
        else:
            if self.score.get() > 0:
                self.score.set(self.score.get() - 1)
            make_sound(self.music)
            # self.ans.set("Check your spelling again.")
            img = PhotoImage(file='assets/wrong.png')
            right_label = Label(label_frame, image=img)
            right_label.image = img
            right_label.pack()
            # right_label.place(x=0, y=500)

        
        self.text_entry.delete(0, END)

        # anstext_label = Label(label_frame, textvariable=self.ans,fg="dark green")
        # anstext_label.pack(side=TOP)
        # anstext_label.grid(column=1, row=1, rowspan=2, sticky=NW)
        
        scoretext_label = Label(score_frame, text="SCOREBOARD", font=("Arial Bold", 14))
        # scoretext_label.pack(side=LEFT)
        scoretext_label.pack()

        score_label = Label(score_frame, textvariable=self.score, bg='white', font=("Arial Bold", 16))
        # score_label.pack(side=LEFT)
        score_label.pack(side=BOTTOM, ipadx=25, ipady=25)
        

    def clean(self):
        for i in self.root.winfo_children():
            i.destroy()

    def run(self):
        self.root.mainloop()


sm = SpellingMaster()
sm.run()