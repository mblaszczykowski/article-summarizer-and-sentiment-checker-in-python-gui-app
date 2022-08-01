import tkinter
import customtkinter

import nltk
from textblob import TextBlob
from newspaper import Article

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("Article Summarizer")
        self.geometry("830x520")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        # two frames
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.frame_left = customtkinter.CTkFrame(master=self,
                                                 width=180,
                                                 corner_radius=0)
        self.frame_left.grid(row=0, column=0, sticky="nswe")

        self.frame_right = customtkinter.CTkFrame(master=self)
        self.frame_right.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)

        # frame_left
        self.frame_left.grid_rowconfigure(0, minsize=100)   # empty row with minsize as spacing

        self.label_1 = customtkinter.CTkLabel(master=self.frame_left,
                                              text="Article Summarizer",
                                              text_font=("Poppins", 18, "bold"))
        self.label_1.grid(row=1, column=0, pady=18, padx=30)

        self.entry = customtkinter.CTkEntry(master=self.frame_left,
                                            width=180,
                                            placeholder_text="Link to article",
                                            justify="center")
        self.entry.grid(row=2, column=0, pady=0, padx=10)

        self.button_1 = customtkinter.CTkButton(master=self.frame_left,
                                                text="Summarize",
                                                command=self.summarizeFunc)
        self.button_1.grid(row=10, column=0, pady=22, padx=20, sticky="nsew")

        # frame_right
        self.frame_right.rowconfigure((0, 1), weight=1)
        self.frame_right.columnconfigure((0), weight=1)

        self.frame_info = customtkinter.CTkFrame(master=self.frame_right)
        self.frame_info.grid(row=0, column=0, columnspan=1, rowspan=3, pady=20, padx=20, sticky="nsew")

        self.frame_info.columnconfigure(0, weight=1)

        self.frame_info.grid_rowconfigure(0, minsize=5)

        self.titleLabel = customtkinter.CTkLabel(master=self.frame_info, text="Title", text_font=("Poppins", 13, "bold"))
        self.titleLabel.grid(column=0, row=1, pady=0, padx=0, sticky="nsew")

        self.title = customtkinter.CTkLabel(master=self.frame_info,
                                                   text="" ,
                                                   height=25,
                                                   corner_radius=6,  # <- custom corner radius
                                                   fg_color=("white", "gray38"),  # <- custom tuple-color
                                                   justify="center")
        self.title.grid(column=0, row=2, sticky="nwe", padx=15, pady=5)

        self.authorsLabel = customtkinter.CTkLabel(master=self.frame_info, text="Authors", text_font=("Poppins", 13, "bold"))
        self.authorsLabel.grid(column=0, row=3, pady=0, padx=20, sticky="nsew")

        self.authors = customtkinter.CTkLabel(master=self.frame_info,
                                                   text="" ,
                                                   height=25,
                                                   corner_radius=6,  # <- custom corner radius
                                                   fg_color=("white", "gray38"),  # <- custom tuple-color
                                                   justify="center")
        self.authors.grid(column=0, row=4, sticky="nwe", padx=15, pady=5)

        self.summaryLabel = customtkinter.CTkLabel(master=self.frame_info, text="Summary", text_font=("Poppins", 13, "bold"))
        self.summaryLabel.grid(column=0, row=5, pady=0, padx=20, sticky="nsew")

        self.summary = customtkinter.CTkLabel(master=self.frame_info,
                                                   text="",
                                                   height=220,
                                                   wraplength=420,
                                                   corner_radius=6,  # <- custom corner radius
                                                   fg_color=("white", "gray38"),  # <- custom tuple-color
                                                   justify="center")
        self.summary.grid(column=0, row=6, sticky="nwe", padx=15, pady=5)

        self.sentiment = customtkinter.CTkLabel(master=self.frame_info, text="Sentiment", text_font=("Poppins", 15, "bold"))
        self.sentiment.grid(column=0, row=7, pady=0, padx=20, sticky="nsew")

        self.frame_right.grid_rowconfigure(5, minsize=10)

    def summarizeFunc(self):
        url = self.entry.get()

        if url!="":
            nltk.download('punkt')

            article = Article(url)

            article.download()
            article.parse()

            article.nlp()

            analysis = TextBlob(article.text).polarity

            authors_string = ""
            for i in range(len(article.authors)):
                if i!=0:
                    authors_string+= ", " + article.authors[i]
                else: authors_string+= article.authors[i]

            self.title.configure(text=article.title)
            self.authors.configure(text=authors_string)
            self.summary.configure(text=article.summary)

            if analysis>0:
                self.sentiment.configure(text="Positive sentiment")
            elif analysis<0:
                self.sentiment.configure(text="Negative sentiment")
            else:
                self.sentiment.configure(text="Neutral sentiment")

    def on_closing(self, event=0):
        self.destroy()

if __name__ == "__main__":
    app = App()
    app.mainloop()
