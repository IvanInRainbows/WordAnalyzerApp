#import nltk
#rom nltk.corpus import wordnet
import tkinter as tk
import tkinter.ttk as ttk
from functools import partial
import re
import wn
    

def RemoveDupes(dic): #recibe un diccionario y lo devuelve si elementos repetidos
        for k in dic:
            dic[k] = list(dict.fromkeys(dic[k]))
        return dic

#wn.add_exomw()
#wn.add_omw()
hFront = ("Arial", 12, "bold") #fuente de los titulos
class Semantics(ttk.Frame): #esta clase procesa y muestra toda la informacion semantica
    def __init__(self, master):
        super().__init__(master, width=200, height=100, borderwidth=7, relief=tk.RIDGE)
        self.synonims = tk.StringVar()
        self.antonyms = tk.StringVar()
        self.hypers = tk.StringVar()
        self.hipos = tk.StringVar()
        #self.mero = tk.StringVar()
        #self.holo = tk.StringVar()
        self.defin = tk.StringVar()
        self.lang = ""
        self.mer = PartWholeRelationship(self, 4, isMeronym=True)
        self.hol = PartWholeRelationship(self, 5, isMeronym=False)
        self.__update()
        self.grid(column=0, row=1)

    def set_lang(self, newLang):
        self.lang = newLang

    def SynsAnts(self, w): #Para procesar todas las relaciones de significado
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
            for l in i.lemmas(): #Logica para los sinonimos de aleman
                if l.title() != w:
                    rt["Syns"].append(l.title())
                    
            for h in i.hypernyms(): #Logica para los hiperonimos de aleman
                for e in h.lemmas():
                    rt["Hipers"].append(e.title())

            for h in i.hyponyms(): #Logica para los hiponimos de aleman
                for e in h.lemmas():
                    rt["Hipos"].append(e.title())
                
            for s in i.senses(): #Logica para los antonimos en aleman, ocurre lo mismo que en el resto de idiomas
                for trad in s.translate(lang="en"):
                    for a in trad.get_related("antonym"):
                        for t in a.translate(lang=self.lang):
                            rt["Ants"].append(t.word().lemma())
                
            if len(self.defin.get()) < 5: #Para la definicion en aleman
                self.defin.set(i.definition())

        return RemoveDupes(rt)
    def setOutput(self, w):
        print(self.lang)
        dic={} #diccionario temporal
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
    def __update(self): #actualiza los widgets para mostrar la informacion
        ttk.Label(self, text="Sinónimos:", background="#A4F598", font=hFront, relief=tk.RIDGE).grid(column="0", row="2", sticky=(tk.NSEW))
        ttk.Label(self, textvariable=self.synonims, background="#A4F598", wraplength=200, relief=tk.RIDGE, width=-25, padding="5 5 5 5").grid(column="1", row="2", sticky=(tk.NSEW))

        ttk.Label(self, text="Antónimos:", background="#F9877B", font=hFront, relief=tk.RIDGE).grid(column="2", row="2", sticky=(tk.NSEW))
        ttk.Label(self, textvariable=self.antonyms, background="#F9877B", wraplength=200, relief=tk.RIDGE, width=-25, padding="5 5 5 5").grid(column="3", row="2", sticky=(tk.NSEW))

        ttk.Label(self, text="Hiperónimos:", background="#d7d4ff", font=hFront, relief=tk.RIDGE).grid(column="0", row="3", sticky=(tk.NSEW))
        ttk.Label(self, textvariable=self.hypers, background="#d7d4ff", wraplength=200, relief=tk.RIDGE, padding="5 5 5 5").grid(column="1", row="3", sticky=(tk.NSEW))

        ttk.Label(self, text="Hipónimos:", background="#feffd4", font=hFront, relief=tk.RIDGE).grid(column="2", row="3", sticky=(tk.NSEW))
        ttk.Label(self, textvariable=self.hipos, background="#feffd4", wraplength=200, relief=tk.RIDGE, padding="5 5 5 5").grid(column="3", row="3", sticky=(tk.NSEW))

        self.mer.update()
        self.hol.update()

        ttk.Label(self, text="Definición", font=hFront, relief=tk.RIDGE).grid(column="0", row="6", sticky=(tk.NSEW))
        ttk.Label(self, textvariable=self.defin, wraplength=600, relief=tk.RIDGE, padding="5 5 5 5").grid(column="1", row="6", sticky=(tk.NSEW), columnspan=3)


class PartWholeRelationship(tk.Label):
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
        ttk.Label(sFrame, text=(self.title+" de membresía"), relief=tk.RIDGE).grid(column="0", row="0", sticky=(tk.NSEW))
        ttk.Label(sFrame, text=(self.title+ " de sustancia"), relief=tk.RIDGE).grid(column="0", row="1", sticky=(tk.NSEW))
        ttk.Label(sFrame, text=(self.title+ " de parte"), relief=tk.RIDGE).grid(column="0", row="2", sticky=(tk.NSEW))
        sFrame2 = ttk.Frame(self.master)
        sFrame2.columnconfigure(0, weight=1)
        ttk.Label(sFrame2, textvariable=self.member, relief=tk.RIDGE, wraplength=400).grid(column="0", row="0", sticky=(tk.NSEW), columnspan=2)
        ttk.Label(sFrame2, textvariable=self.substance, relief=tk.RIDGE, wraplength=400).grid(column="0", row="1", sticky=(tk.NSEW), columnspan=2)
        ttk.Label(sFrame2, textvariable=self.part, relief=tk.RIDGE, wraplength=400).grid(column="0", row="2", sticky=(tk.NSEW), columnspan=2)
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
            for mer in synset.member_meronyms():
                for l in mer.lemmas(lang=lang):
                    out["member"].append(l.name())

        for synset in wn.synsets(word, lang=lang):
            for mer in synset.substance_meronyms():
                for l in mer.lemmas(lang=lang):
                    out["substance"].append(l.name())

        for synset in wn.synsets(word, lang=lang):
            for mer in synset.part_meronyms():
                for l in mer.lemmas(lang=lang):
                    out["part"].append(l.name())
        return out
    def holonyms(self, word, lang):
        out = {
            "member":[],
            "substance":[],
            "part":[]
            }
        for synset in wn.synsets(word, lang=lang):
            for mer in synset.get_related("holo_member"):
                for l in mer.lemmas(lang=lang):
                    out["member"].append(l.name())

        for synset in wn.synsets(word, lang=lang):
            for mer in synset.substance_holonyms():
                for l in mer.lemmas(lang=lang):
                    out["substance"].append(l.name())

        for synset in wn.synsets(word, lang=lang):
            for mer in synset.part_holonyms():
                for l in mer.lemmas(lang=lang):
                    out["part"].append(l.name())
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