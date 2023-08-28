#import nltk
#from nltk.corpus import wordnet
import tkinter as tk
import tkinter.ttk as ttk
from functools import partial
import re
import wn
 

def RemoveDupes(dic): #gets a dictionary composed of strings as keys and lists as values and returns the dictionary with no duplicates in its nested lists
        for k in dic:
            dic[k] = list(dict.fromkeys(dic[k]))
        return dic

#wn.add_exomw()
#wn.add_omw()
hFront = ("Arial", 12, "bold") #Title font
maxLen = 300 #Max lenght of a displayed text in characters before is displayer with the scrollbar
maxSize = { #Max size of the TextScroll widget
    "V":150,
    "H":300
    }


class TextScroll (ttk.Frame): #Instantiates a Scrollable text with a given size (width and height) through a really messy process of creating a canvas and a scrollbar inside a frame and then a frame inside that canvas to place the label widget with the text uuh
    def __init__(self, master, tx, width, height):
        super().__init__(master, relief=tk.RIDGE, padding="5 5 5 5")
        self.tx = tx
        self.canvas = tk.Canvas(self, height=height, width=width)
        self.scroll = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.canvas.yview)
        self.innerFrame = ttk.Frame(self.canvas)
        self.innerFrame.grid(column=0, row=0, sticky=tk.NSEW)
        ttk.Label(self.innerFrame, textvariable=self.tx, wraplength=300, justify=tk.LEFT).grid(column=0, row=0, sticky=tk.EW)
        self.canvas.configure(yscrollcommand=self.scroll.set)
        self.canvas.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0,0), window=self.innerFrame, anchor=tk.NW)
        self.canvas.grid(column=0, row=0, sticky=tk.NSEW)
        self.scroll.grid(column=1, row=0, sticky=tk.NS)

class Semantics(ttk.Frame): #A class to process and display all the semantic information of the word
    def __init__(self, master):
        super().__init__(master, width=200, height=100, borderwidth=7)
        self.synonims = tk.StringVar()
        self.antonyms = tk.StringVar()
        self.hypers = tk.StringVar()
        self.hipos = tk.StringVar()
        self.defin = tk.StringVar()
        self.lang = ""
        self.mer = PartWholeRelationship(self, 4, isMeronym=True)
        self.hol = PartWholeRelationship(self, 5, isMeronym=False)
        self.widgetController = []
        self.__update()
        self.grid(column=0, row=1)

    def set_lang(self, newLang):
        self.lang = newLang

    def SynsAnts(self, w): #Computes all the semantic relation information and saves then in a dictionary that is then returned with no dupes
        self.defin.set("")
        rt = {
            "Syns":[],
            "Ants":[],
            "Hipers":[],
            "Hipos":[],
            "Meros":[],
            "Holos":[]
            }
        
        for i in wn.synsets(w, lang=self.lang):
            for l in i.lemmas(): #Logica para los sinonimos
                if l.title() != w:
                    rt["Syns"].append(l.title())
                    
            for h in i.hypernyms(): #Logica para los hiperonimos
                for e in h.lemmas():
                    rt["Hipers"].append(e.title())

            for h in i.hyponyms(): #Logica para los hiponimos
                for e in h.lemmas():
                    rt["Hipos"].append(e.title())
                
            for s in i.senses(): #Logica para los antonimos
                for trad in s.translate(lang="en"):
                    for a in trad.get_related("antonym"):
                        for t in a.translate(lang=self.lang):
                            rt["Ants"].append(t.word().lemma())
                
            if len(self.defin.get()) < 5: #Para la definicion
                if i.definition() != None:
                    self.defin.set(i.definition())
                else:
                    for t in i.translate(lang="en"):
                        if t.definition() != None:
                            self.defin.set(t.definition())
                            break

        return RemoveDupes(rt)
    def setOutput(self, w): #assigns the output of the previous method to each attribute and then updates the widgets to display the information
        print(self.lang)
        dic={} #temportal dict
        w = w.get()
        dic = self.SynsAnts(w)
        self.synonims.set(re.sub("_", " ", ", ".join(dic["Syns"])))
        self.antonyms.set(re.sub("_", " ",", ".join(dic["Ants"])))
        self.hypers.set(re.sub("_", " ",", ".join(dic["Hipers"])))
        self.hipos.set(re.sub("_", " ",", ".join(dic["Hipos"])))
        self.mer.setOutput(w, self.lang)
        self.hol.setOutput(w, self.lang)
        self.__update()
        print("done")
    def __update(self): #Updates the widgets to display the information
        self.resetVarWidgets()#clears the variable labels
        ttk.Label(self, text="Sinónimos:", background="#A4F598", font=hFront, relief=tk.RIDGE).grid(column="0", row="2", sticky=(tk.NSEW))
        if (len(self.synonims.get()) < maxLen):#Each variable display has this conditional to control whether the information should be display as a normal label or as a scrollable text
            w = ttk.Label(self, textvariable=self.synonims, background="#A4F598", wraplength=200, relief=tk.RIDGE, width=-25, padding="5 5 5 5")
            self.widgetController.append(w)
            w.grid(column="1", row="2", sticky=(tk.NSEW))
        else:
            w = TextScroll(self, self.synonims, maxSize["H"], maxSize["V"])
            self.widgetController.append(w)
            w.grid(column="1", row="2", sticky=(tk.NSEW))

        ttk.Label(self, text="Antónimos:", background="#F9877B", font=hFront, relief=tk.RIDGE).grid(column="2", row="2", sticky=(tk.NSEW))
        if (len(self.antonyms.get()) < maxLen):
            w=ttk.Label(self, textvariable=self.antonyms, background="#F9877B", wraplength=200, relief=tk.RIDGE, width=-25, padding="5 5 5 5")
            self.widgetController.append(w)
            w.grid(column="3", row="2", sticky=(tk.NSEW))
        else:
            w=TextScroll(self, self.antonyms, maxSize["H"], maxSize["V"])
            self.widgetController.append(w)
            w.grid(column="3", row="2", sticky=(tk.NSEW))

        ttk.Label(self, text="Hiperónimos:", background="#d7d4ff", font=hFront, relief=tk.RIDGE).grid(column="0", row="3", sticky=(tk.NSEW))
        if (len(self.hypers.get()) < maxLen):
           w = ttk.Label(self, textvariable=self.hypers, background="#d7d4ff", wrap=200, relief=tk.RIDGE, padding="5 5 5 5")
           self.widgetController.append(w)
           w.grid(column="1", row="3", sticky=(tk.NSEW))
        else:
            w=TextScroll(self, self.hypers, maxSize["H"], maxSize["V"])
            self.widgetController.append(w)
            w.grid(column="1", row="3",  sticky=(tk.NSEW))

        ttk.Label(self, text="Hipónimos:", background="#feffd4", font=hFront, relief=tk.RIDGE).grid(column="2", row="3", sticky=(tk.NSEW))
        if (len(self.hipos.get()) < maxLen):
            w = ttk.Label(self, textvariable=self.hipos, background="#feffd4", wraplength=200, relief=tk.RIDGE, padding="5 5 5 5")
            self.widgetController.append(w)
            w.grid(column="3", row="3", sticky=(tk.NSEW))
        else:
            w = TextScroll(self, self.hipos, maxSize["H"], maxSize["V"])
            self.widgetController.append(w)
            w.grid(column="3", row="3", sticky=(tk.NSEW))

        self.mer.update()
        self.hol.update()

        ttk.Label(self, text="Definición", font=hFront, relief=tk.RIDGE).grid(column="0", row="6", sticky=(tk.NSEW))
        ttk.Label(self, textvariable=self.defin, wraplength=600, relief=tk.RIDGE, padding="5 5 5 5").grid(column="1", row="6", sticky=(tk.NSEW), columnspan=3)
        
    def resetVarWidgets(self): #resets all the variable labels so they don't instantiate twice and overlap
        for i in self.widgetController:
            i.destroy()
        self.widgetController = []

class PartWholeRelationship(tk.Label): #intended to use inside semantics object. Computes and displays all the semantic information related to part-whole relationships
    def __init__(self, master, row, isMeronym = True):
        self.member = tk.StringVar()
        self.part = tk.StringVar()
        self.substance = tk.StringVar()
        self.master = master
        self.row = row
        if isMeronym:
            self.title = "Merónimos"
        else:
            self.title = "Holónimos"
        super().__init__(master, text=self.title, background="#fdb8ff", font=hFront, relief=tk.RIDGE)
        self.grid(column=0, row=row, sticky=(tk.NSEW))
        self.update()
    def update(self):
        sFrame = ttk.Frame(self.master)
        sFrame.columnconfigure(0, weight=1)
        ttk.Label(sFrame, text=(self.title+" de membresía"), relief=tk.RIDGE, padding="5 5 5 5").grid(column="0", row="0", sticky=(tk.NSEW))
        ttk.Label(sFrame, text=(self.title+ " de sustancia"), relief=tk.RIDGE, padding="5 5 5 5").grid(column="0", row="1", sticky=(tk.NSEW))
        ttk.Label(sFrame, text=(self.title+ " de parte"), relief=tk.RIDGE, padding="5 5 5 5").grid(column="0", row="2", sticky=(tk.NSEW))
        sFrame2 = ttk.Frame(self.master)
        sFrame2.columnconfigure(0, weight=1)
        ttk.Label(sFrame2, textvariable=self.member, relief=tk.RIDGE, wraplength=400, padding="5 5 5 5").grid(column="0", row="0", sticky=(tk.NSEW), columnspan=2)
        ttk.Label(sFrame2, textvariable=self.substance, relief=tk.RIDGE, wraplength=400, padding="5 5 5 5").grid(column="0", row="1", sticky=(tk.NSEW), columnspan=2)
        ttk.Label(sFrame2, textvariable=self.part, relief=tk.RIDGE, wraplength=400, padding="5 5 5 5").grid(column="0", row="2", sticky=(tk.NSEW), columnspan=2)
        sFrame.grid(column=1, row=self.row, sticky=(tk.NSEW))
        sFrame2.grid(column=2, row=self.row, sticky=(tk.NSEW), columnspan=2)


    def setOutput(self, word, lang):
        tmpDict = {}
        if self.title == "Merónimos":
            tmpDict = self.meronyms(word, lang)
        else:
            tmpDict = self.holonyms(word, lang)
        
        self.member.set(", ".join(tmpDict["member"]))
        self.substance.set(", ".join(tmpDict['substance']))
        self.part.set(", ".join(tmpDict["part"]))
    def meronyms(self, word, lang):
        out = {
            "member":[],
            "substance":[],
            "part":[]
            }
        for synset in wn.synsets(word, lang=lang):
            for mer in synset.get_related("mero_member"):
                for l in mer.words():
                    out["member"].append(l.lemma())

        for synset in wn.synsets(word, lang=lang):
            for mer in synset.get_related("mero_substance"):
                for l in mer.words():
                    out["substance"].append(l.lemma())

        for synset in wn.synsets(word, lang=lang):
            for mer in synset.get_related("mero_part"):
                for l in mer.words():
                    out["part"].append(l.lemma())
        return out
    def holonyms(self, word, lang):
        out = {
            "member":[],
            "substance":[],
            "part":[]
            }
        for synset in wn.synsets(word, lang=lang):
            for mer in synset.get_related("holo_member"):
                for l in mer.words():
                    out["member"].append(l.lemma())

        for synset in wn.synsets(word, lang=lang):
            for mer in synset.get_related("holo_substance"):
                for l in mer.words():
                    out["substance"].append(l.lemma())

        for synset in wn.synsets(word, lang=lang):
            for mer in synset.get_related("holo_part"):
                for l in mer.words():
                    out["part"].append(l.lemma())
        return out

    def debugAttrs(self):
        print("part: " + self.part.get())
        print("member: " + self.member.get())
        print("substance: " + self.substance.get())



class Morphology(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.derivation = tk.StringVar()
        self.number = tk.StringVar()