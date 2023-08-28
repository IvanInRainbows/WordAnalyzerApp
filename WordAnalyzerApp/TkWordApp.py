import nltk
from nltk.corpus import wordnet
import tkinter as tk
import tkinter.ttk as ttk
from functools import partial

from TkWordApp_class import Semantics

global subRoot 
subRoot = tk.Tk()

def debugOption(*args):
    sem.set_lang(langCodes[langSel.get()])

def debugWord():
    print(word.get())

def close(currentRoot):
    currentRoot.destroy()
    quit()

subRoot.title("Buscador de sinonimos y antonimos")

languages = [
    "Español",
    "English",
    "Deutsch"
    ]
langCodes = {
    "Español":"es",
    "English":"en",
    "Deutsch":"de"
    }
langSel = tk.StringVar()
langSel.set(languages[0])

frame = ttk.Frame(subRoot)
word = tk.StringVar()
sem = Semantics(subRoot)
debugOption()
optMenu = ttk.OptionMenu(frame, langSel, languages[0], *languages, command=debugOption)
optMenu.grid(column=0, row=0)
ttk.Label(frame, text="Introduce una palabra").grid(column="1", row="0")
wEntry = ttk.Entry(frame, textvariable=word, width = 15, takefocus=True).grid(column="2", row="0")
ttk.Button(frame, text="Buscar", command=partial(sem.setOutput, word)).grid(column="3", row="0")
frame.grid(column="0", row="0")

subRoot.update()
print(sem.grid_bbox(1,1))
ttk.Button(subRoot, command=partial(close, subRoot), text="Cerrar").grid(column=4, row=3)

subRoot.mainloop()

