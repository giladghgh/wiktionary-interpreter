import sys
import webbrowser
import tkinter as tk

from Translators import *





class Interfacer(tk.Tk):
    LANGUAGES = [
        "Arabic",
        "Danish",
    ]

    GO = {
        # "Lang" : ["go" , (translation font) , (button font) , (display font)]
        "Arabic" : ["!يلا" , ("Segoe UI",15) , ("Lexend",14) , ("Lexend",13,"bold")],
        "Danish" : ["Gå!" , ("Segoe UI",13) , ("Lexend",12) , ("Lexend",10,"bold")],
    }

    def __init__(self , *args , **kwargs):
        super().__init__(*args , **kwargs)

        # Foundation
        self.title("Wiktionary Interpreter")

        self.Arabiciser = Arabiciser()
        # self.Danishiser = Danishiser()
        self.T = self.Arabiciser

        self.window_w = 500
        self.window_h = 555
        self.geometry('%dx%d+%d+%d'%(
            self.window_w,
            self.window_h,
            self.winfo_screenwidth()*2/5 - self.window_w/2,
            self.winfo_screenheight()*2/5 - self.window_h/2
        ))

        # Function
        self.word = tk.StringVar(self)
        self.lang = tk.StringVar(self)
        self.lang.set(self.LANGUAGES[0])

        self.table_T = {}
        self.table_S = {}

        # Format
        self.bg_header = self.hex(50)
        self.bg_thesis = self.hex(150)
        self.bg_suffix = self.hex(125)

        self.Header = tk.Frame(self)
        self.setup_Header()

        self.Thesis = tk.Frame(self)
        self.setup_Thesis()

        self.Suffix = tk.Frame(self)
        self.setup_Suffix()

        # Formulae
        self.bind("<Escape>",self.quit)
        self.bind("<Return>",self.go)
        self.bind(
            "<MouseWheel>",
            lambda e : self.Thesis.Canvas.yview_scroll(-int(e.delta/100),"units")
        )
        self.Thesis.body.bind(
            "<Configure>",
            lambda e : self.Thesis.Canvas.configure(scrollregion=self.Thesis.Canvas.bbox("all"))
        )

        self.lang.trace(
            tk.W,
            lambda *_ : self.Header.go.configure(
                text=self.GO[self.lang.get()][0],
                font=self.GO[self.lang.get()][2]
            )
        )

        # Finishing touches
        self.Header.entry.focus_set()


    def setup_Header(self):
        self.Header.configure(bg=self.bg_header)
        self.Header.pack(fill=tk.BOTH)

        # Language dropdown
        self.Header.dropdown = tk.OptionMenu(self.Header , self.lang , *self.LANGUAGES)
        self.Header.dropdown.grid(
            row=0,
            column=0,
            padx=(30,5),
            pady=15,
            ipadx=0,
            ipady=3
        )

        # Word entry
        self.Header.entry = tk.Entry(self.Header , textvariable=self.word)
        self.Header.entry.grid(
            row=0,
            column=1,
            padx=5,
            pady=15,
            ipadx=0,
            ipady=5
        )

        # Go button
        self.Header.go = tk.Button(self.Header , text=self.GO[self.lang.get()][0] , command=self.go , font=self.GO[self.lang.get()][2] , cursor="hand2")
        self.Header.go.grid(
            row=0,
            column=2,
            padx=5,
            pady=0,
            ipadx=3,
            ipady=1
        )

        # Word display
        self.Header.display = tk.Label(self.Header , text=self.word.get() , font=self.GO[self.lang.get()][3] , bg=self.hex(75) , fg=self.hex(225) , width=8 , pady=5 , relief=tk.SUNKEN)
        self.Header.display.place(x=338,y=16)

        # Clear button
        self.Header.clear = tk.Button(self.Header , text="❌" , command=self.go , font=("Lexend",13) , cursor="hand2")
        self.Header.clear.configure(background=self.hex(100,50,50) , activebackground=self.hex(100,75,75))
        self.Header.clear.place(x=430,y=16)


    def setup_Thesis(self):
        self.Thesis.pack(fill=tk.BOTH , expand=True)

        self.Thesis.Canvas = tk.Canvas(self.Thesis , bg=self.bg_thesis , highlightthickness=0)
        self.Thesis.Scroll = tk.Scrollbar(self.Thesis , orient=tk.VERTICAL , width=15)
        self.Thesis.body = tk.Frame(self.Thesis.Canvas , bg=self.bg_thesis)

        self.Thesis.Canvas.pack(side=tk.LEFT , fill=tk.BOTH , expand=True)
        self.Thesis.Scroll.pack(side=tk.RIGHT , fill=tk.Y , expand=False)
        self.Thesis.Canvas.create_window((0,0) , window=self.Thesis.body , anchor=tk.NW)

        self.Thesis.Canvas.configure(yscrollcommand=self.Thesis.Scroll.set)
        self.Thesis.Scroll.configure(command=self.Thesis.Canvas.yview)

        self.Thesis.label = tk.Label(self.Thesis.body , text="Translations:" , bg=self.bg_thesis , fg=self.bg_suffix)
        self.Thesis.label.grid(
            row=0,
            column=0,
            padx=35,
            pady=(15,0),
            sticky=tk.W
        )


    def setup_Suffix(self):
        self.Suffix.configure(bg=self.bg_suffix)
        self.Suffix.pack(fill=tk.BOTH)

        self.Suffix.label = tk.Label(self.Suffix , text="Suggestions:" , anchor=tk.W , bg=self.bg_suffix , fg=self.hex(150) , padx=5)
        self.Suffix.label.grid(
            row=0,
            column=0,
            padx=(35,15),
            pady=0,
            ipadx=5,
            ipady=1
        )


    def write_Thesis(self):
        if not self.table_T:
            return

        i,j,k = 1,1,1
        for sense,gloss in self.table_T.items():
            tk.Label(
                self.Thesis.body,
                text=sense.title(),
                anchor=tk.W,
                justify=tk.LEFT,
                wraplength=150,
                bg=self.bg_thesis,
                width=18
            ).grid(
                row=i,
                column=0,
                padx=(35,15),
                pady=(10,5),
                rowspan=2,
                sticky=tk.NW
            )

            for lang,trans in gloss.items():
                tk.Label(
                    self.Thesis.body,
                    text=self.T.ISO[lang],
                    anchor=tk.W,
                    justify=tk.LEFT,
                    bg=self.bg_thesis,
                    width=18
                ).grid(
                    row=j,
                    column=1,
                    padx=(35,15),
                    pady=(10,5),
                    sticky=tk.NW
                )

                for tran,link in trans:
                    txl = tk.Label(
                        self.Thesis.body,
                        text=tran,
                        anchor=tk.E,
                        justify=tk.RIGHT,
                        bg=self.bg_thesis,
                        width=8,
                        font=self.GO[self.lang.get()][1],
                        cursor="hand2"
                    )
                    txl.bind("<Button-1>" , lambda event,url=link:webbrowser.open(url))
                    txl.grid(
                        row=k,
                        column=2,
                        pady=(0,5),
                        sticky=tk.NE
                    )

                    i += 1
                    j += 1
                    k += 1


    def write_Suffix(self):
        if not self.table_S:
            return

        for i,(name,link) in enumerate( self.table_S.items() ):
            sugg = tk.Label(
                self.Suffix,
                text=name,
                bg=self.bg_suffix,
                fg=self.hex(50,50,185),
                font=("Lexend",9,"underline"),
                cursor="hand2"
            )
            sugg.bind("<Button-1>" , lambda event:webbrowser.open(link))
            sugg.grid(
                row=0,
                column=i+1,
                padx=(15,0),
                pady=15,
                ipadx=0,
                ipady=0
            )


    def go(self , event=None):
        search = self.word.get().lower()
        self.word.set("")

        self.Header.display.configure(text=search , fg="white" , font=self.GO[self.lang.get()][3])

        # Reset
        self.table_T.clear()
        self.table_S.clear()
        for widget in self.Suffix.winfo_children()[1:] + self.Thesis.body.winfo_children()[1:]:
            widget.destroy()

        # Search
        if search:
            try:
                self.table_T , self.table_S = self.T.translate(search)
            except TranslationExceptions as e:
                self.Header.display.configure(fg=self.hex(175,75,75) , font=self.GO[self.lang.get()][3][:1])

        # Write Thesis
        self.write_Thesis()
        self.Thesis.label.configure(fg=self.hex(75) if self.table_T else self.bg_suffix)

        # Write Suffix
        self.write_Suffix()
        self.Suffix.label.configure(fg=self.hex(50) if self.table_S else self.bg_thesis)
        self.rowconfigure(3,pad=15 if self.table_S else 1)


    def quit(self , event=None):
        self.withdraw()
        sys.exit()


    @staticmethod
    def hex(*args):
        if len(args) == 1:
            return "#%02x%02x%02x"%(args[0],args[0],args[0])
        else:
            return "#%02x%02x%02x"%(args[0],args[1],args[2])
