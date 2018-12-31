import tkinter as tk
import nltk
from nltk.corpus import words
from nltk.corpus import wordnet as wn
from tkinter import messagebox

global isClick #Get event when user click on Create new word button
global isFavoriteClick #Get event when user click on My Favorite button
isClick = False
isFavoriteClick = False

#Function for display windows to user for getting their input
def createNewWord():

    global f1, f2

    f1 = tk.Frame(root)
    f1.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
    f2 = tk.Frame(root)
    f2.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

    l1 = tk.Label(f1, text="Word")
    l1.pack(fill=tk.BOTH, expand=1)

    word_input = tk.Entry(f2)
    word_input.pack(fill=tk.BOTH, expand=1)

    l2 = tk.Label(f1, text="Definition")
    l2.pack(fill=tk.BOTH, expand=1)

    definition_input = tk.Entry(f2)
    definition_input.pack(fill=tk.BOTH, expand=1)

    l3 = tk.Label(f1, text="Example")
    l3.pack(fill=tk.BOTH, expand=1)

    l4 = tk.Label(f1, text="️")
    l4.pack(fill=tk.BOTH, expand=1)

    example_input = tk.Entry(f2)
    example_input.pack(fill=tk.BOTH, expand=1)

    b = tk.Button(f2, text="Add", width=10, command=lambda:writeNewWord(word_input.get(), definition_input.get(), example_input.get()))
    b.pack(fill=tk.BOTH, expand=1)


# Remove any selected Favorite from the list
def removeFavorite():

    global selected_favorite
    global favorite_frame

    if checkisFavorite(selected_favorite.strip()):
        f=open("Myfavorite.txt","r")
        lines=f.readlines()
        f.close()

        f=open("Myfavorite.txt", "w")
        for line in lines:
            if line.split('$')[1].strip() != selected_favorite.strip():
                f.write(line)

        f.close()
        favorite_frame.destroy()
        myFavoriteFrame()
    else:
        tk.messagebox.showinfo("Warning", "No Word is Selected!")


# Remove any selected New Words from the list
def removeNewWords():

    global newWords_frame
    global selected_newWords

    text = selected_newWords.strip()

    if checkWordInFile(text):
        f=open("words.txt","r")
        lines=f.readlines()
        f.close()

        f=open("words.txt", "w")
        for line in lines:
            if line.split('$')[1].strip() != text:
                f.write(line)

        f.close()
        newWords_frame.destroy()
        new_word_frame()

    else:
        tk.messagebox.showinfo("Warning", "No Word is Selected!")


# Create a screen to display favorite words list
def myFavoriteFrame():

    global favorite_frame
    global selected_favorite

    selected_favorite = ""

    favorite_frame = tk.Frame(root)
    favorite_frame.pack(fill=tk.BOTH, expand=1)

    l1 = tk.Label(favorite_frame, text="Your Favorite Word List")
    l1.pack(fill=tk.BOTH, expand=1)

    scrollbar = tk.Scrollbar(favorite_frame, orient="vertical")
    scrollbar.pack(side=tk.RIGHT, fill=tk.BOTH)

    listbox = tk.Listbox(favorite_frame,yscrollcommand=scrollbar.set)
    listbox.pack(fill=tk.BOTH, expand=1)
    scrollbar.config(command=listbox.yview)
    listbox.bind('<<ListboxSelect>>', CurSelet)

    favorites = getMyFavorite().split("$")

    b = tk.Button(favorite_frame, text="Remove", width=10, command=removeFavorite)
    b.pack(fill=tk.Y, expand=1)


    for i in range(0, len(favorites)):
        if(i!=0):
            listbox.insert(i, favorites[i].strip())


# ON/OFF My Favorite Frame when user press on button
def onMyFavoritePress():
    global isFavoriteClick, isClick
    global favorite_frame, f1, f2

    if isFavoriteClick:
        isFavoriteClick = False
        favorite_frame.destroy()
    else:
        if isClick:
            f1.destroy()
            f2.destroy()
            isClick = False
            isFavoriteClick=True
            myFavoriteFrame()
        else:
            isFavoriteClick=True
            myFavoriteFrame()


# Get the Latest ID from word_id file
def getNewWordID():
    f=open("word_id.txt", "r")
    id=f.readline()
    return int(id)



# Get the Latest ID from favoriteword_id file
def getFavoriteWordID():
    f = open("favoriteword_id.txt", "r")
    id = f.readline()
    return int(id)



#Write the word definition example to file
def writeNewWord(word, definition, example):

    global f1, f2

    if(word.strip() == ""):
        tk.messagebox.showinfo("Warning", "The Input cannot be empty")
    elif (' ' in word.strip()):
        tk.messagebox.showinfo("Warning", "You cannot input a sentence, Please input a word only!")
    else :
        if checkIncorrectWord(word) or checkWordInFile(word):
            tk.messagebox.showinfo("Warning", "The word is either in Dictionary or already created!")
        else:
            id = getNewWordID() +1

            id= str(id)

            f=open("words.txt", "a+")
            f_1=open("definitions.txt", "a+")
            f_2=open("examples.txt","a+")
            f_3=open("word_id.txt", "w+")

            f.write(id+"$"+word+"\n")
            f_1.write(id+"$"+definition+"\n")
            f_2.write(id+"$"+example+"\n")
            f_3.write(str(id))

            f.close()
            f_1.close()
            f_2.close()
            f_3.close()

            tk.messagebox.showinfo("Success", "The new word have been created successfully")

            f1.destroy()
            f2.destroy()
            createNewWord()




#Show Definition and Example
def info_frame(title , word, content):
    win = tk.Toplevel()
    win.wm_title(title)

    l1 = tk.Label(win, text=word.upper())
    l1.pack()

    T = tk.Text(win)
    T.pack(fill=tk.BOTH, expand=1)
    T.insert(tk.END, content)
    T.config(state=tk.DISABLED)


# Show Definition and Example
def definitionPress(word):

    if word.strip() == "":
        tk.messagebox.showinfo("Warning", "The input cannot be emtpy!")
    else:
        if checkIncorrectWord(word):
            syns = wn.synsets(word)
            definition = str(syns[0].definition())
            examples = syns[0].examples()
            exp = ""
            for each in examples:
                exp = exp + each + ".\n" + " "*10
            string = "Definition:  " + definition + ".\n\n" + "Example:  " + exp
            info_frame("Definition and Example", word, string)
        elif checkWordInFile(word):
            string = getDefinitionFromFile(word) + "\n\n" + getExampleFromFile(word)
            info_frame("Definition and Example", word, string)
        else:
            tk.messagebox.showinfo("Warning", "The word is not valid!")




#when user click on the list
def CurSelet(event):
    global input_text
    global selected_favorite
    global selected_newWords
    widget = event.widget
    selection=widget.curselection()
    if len(selection) > 0:
        picked = widget.get(selection[0])
        input_text.set(picked)
        selected_favorite=picked
        selected_newWords=picked



# ON/OFF Create New Word Frame when user click on button
def onCreateNewWordPress():

    global isClick, isFavoriteClick
    global f1, f2, favorite_frame

    if isClick:
        isClick = False
        f1.destroy()
        f2.destroy()
    else:
        if isFavoriteClick:
            favorite_frame.destroy()
            isFavoriteClick = False
            isClick = True
            createNewWord()
        else:
            isClick = True
            createNewWord()



# Add word to favorite file
def addFavorite(word):

    global favorite_frame

    if(word.strip() == ""):
        tk.messagebox.showinfo("Warning", "The Input is empty!")
    else:
        if checkisFavorite(word):
            tk.messagebox.showinfo("Warning", "The word is already in favorite!")

        elif checkIncorrectWord(word) or checkWordInFile(word):

            id = getFavoriteWordID() + 1

            id = str(id)

            f=open("Myfavorite.txt", "a+")
            f1=open("favoriteword_id.txt", "w")
            f.write(id+"$"+word+"\n")
            f1.write(id)

            f.close()
            f1.close()
            tk.messagebox.showinfo("Success", "You have added the word to favorite")

            if isFavoriteClick:
                favorite_frame.destroy()
                myFavoriteFrame()

        else:
            tk.messagebox.showinfo("Warning", "The word is not valid")


# Check the word if it is already in favorite or not (True mean the word already in favorite)
def checkisFavorite(word):
    with open('Myfavorite.txt') as f:
        listWords = f.readlines()

    flag = False

    for each in listWords:
        if each.split('$')[1].strip().upper() == word.upper():
            flag = True

    if flag:
        return True
    else:
        return False

# Get all Favorite words
def getMyFavorite():

    favorite = ""

    with open('Myfavorite.txt') as f:
        listwords = f.readlines()
    for w in listwords:
        tmp = w.split("$")
        favorite = favorite + "$" + tmp[1]

    return favorite



# Get all New Word from File
def getNewWords():

    newWords = ""

    with open('words.txt') as f:
        listwords = f.readlines()
    for w in listwords:
        tmp = w.split("$")
        newWords = newWords + "$" + tmp[1]

    return newWords


# Find Synonyms of a word
def synonyms(word):
    synonyms = []
    string = "Synonym: "

    for syn in wn.synsets(word):
        for l in syn.lemmas():
            if l.name() != word:
                synonyms.append(l.name())
    if (len(synonyms) > 0):
        for i in range (0,len(synonyms)):
            if i == len(synonyms)-1:
                string = string + synonyms[i] + "."
            else:
                string = string + synonyms[i] + ", "

        info_frame("Synonyms", word, string)

    else:
        if not wn.synsets(word) and not checkWordInFile(word):
            tk.messagebox.showerror("Warning", "The word is not valid")
        else:
            tk.messagebox.showerror("Warning", "The word has no synonym")


# Find Antonyms of a word
def antonyms(word):
    from nltk.corpus import wordnet
    antonyms = []
    string = "Antonym: "

    for syn in wordnet.synsets(word):
        for l in syn.lemmas():
            if l.antonyms():
                antonyms.append(l.antonyms()[0].name())
    antonyms=list(set(antonyms))
    if (len(antonyms) > 0):
        for i in range(0, len(antonyms)):
            if i == len(antonyms)-1:
                string = string + antonyms[i] + "."
            else:
                string = string + antonyms[i] + ", "

        info_frame("Antonyms", word, string)
    else:
        if not wn.synsets(word) and not checkWordInFile(word):
            tk.messagebox.showinfo("Warning", "The word is not valid")
        else:
            tk.messagebox.showinfo("Warning", "The word has no antonym")


#Check if the word is in English (False is when the word is not English word)
def checkIncorrectWord(w):
    if not wn.synsets(w):
        return False
    else:
        return True


# Check word in created file (True mean the word is in File False mean not found)
def checkWordInFile(w):
    with open('words.txt') as f:
        listWords = f.readlines()

    flag = False

    for each in listWords:
        if each.split('$')[1].strip().upper() == w.upper():
            flag = True

    if flag:
        return True
    else:
        return False


# Get Sense of Word
def senseOfWord(w):
    string = "Definition:   "
    for synset in wn.synsets(w):
        string = string + "- " + synset.definition() + ".\n              "

    return string


# Get the Definition of the word in File created
def getDefinitionFromFile(w):
    with open('words.txt') as f:
        listWords = f.readlines()

    for each in listWords:
        tmp = each.split('$')
        if tmp[1].strip().upper() == w.upper():
            id = tmp[0].strip()

    with open('definitions.txt') as f:
        listDef = f.readlines()

    flag = True
    for definition in listDef:
        tmp = definition.split('$')
        if id == tmp[0].strip():
            flag = False
            return "Definition:  " + tmp[1].strip() + "."

    if flag:
        return "Definition:  None"


# Get the Example of the word in file created
def getExampleFromFile(w):
    with open('words.txt') as f:
        listWords = f.readlines()

    for each in listWords:
        tmp = each.split('$')
        if tmp[1].strip().upper() == w.upper():
            id = tmp[0].strip()

    with open('examples.txt') as f:
        listDef = f.readlines()

    flag = True
    for definition in listDef:
        tmp = definition.split('$')
        if id == tmp[0].strip():
            flag = False
            return "Example:  " + tmp[1].strip() + "."

    if flag:
        return "Example:  None"


# Get the event when user click on button Word Sense
def wordSensePress(word):
    if checkIncorrectWord(word):
        info_frame("Word Sense", word, senseOfWord(word))
    else:
        if checkWordInFile(word):
            info_frame("Word Sense", word, getDefinitionFromFile(word))
        else:
            tk.messagebox.showinfo("Warning","Word Not Found!")


# Open The list of New words that user already created
def openNewWords():

    global newWords_frame
    global selected_newWords
    global win

    selected_newWords=""

    win = tk.Tk()
    win.wm_title("New Word List")

    new_word_frame()


def new_word_frame():
    global win
    global newWords_frame

    newWords_frame = tk.Frame(win)
    newWords_frame.pack(fill=tk.BOTH, expand=1)

    l1 = tk.Label(newWords_frame, text="Your New Word List:")
    l1.pack(fill=tk.BOTH, expand=1)

    scrollbar = tk.Scrollbar(newWords_frame, orient="vertical")
    scrollbar.pack(side=tk.RIGHT, fill=tk.BOTH)

    listbox = tk.Listbox(newWords_frame, yscrollcommand=scrollbar.set)
    listbox.pack(fill=tk.BOTH, expand=1)
    scrollbar.config(command=listbox.yview)
    listbox.bind('<<ListboxSelect>>', CurSelet)

    b = tk.Button(newWords_frame, text="Remove", command=removeNewWords)
    b.pack(side=tk.LEFT,fill=tk.Y, expand=1)

    b1 = tk.Button(newWords_frame, text="Refresh", command=reload)
    b1.pack(side=tk.LEFT, fill=tk.Y, expand=1)


    newWords = getNewWords().split("$")

    for i in range(0, len(newWords)):
        if (i != 0):
            listbox.insert(i, newWords[i].strip())


def showAboutUs():
    content = "Low Budget Dictionary was developed by a group of students of Institute of Technology of Cambodia (ITC) in Department of Information and Communication Technology (DICE). \n"
    content = content + "Member : "
    content = content + "LAY Chhivchung\n"
    content = content + " "*9 + "LIM Horhout\n"
    content = content + " " * 9 + "SOEURT Pisey\n"
    content = content + " " * 9 + "CHOU SEAKNY\n"
    content = content + " " * 9 + "MICH Mongkul\n"
    content = content + " " * 9 + "NGO Uyuong\n"
    info_frame("ABOUT US", "ABOUT US", content)


def reload():
    global newWords_frame
    newWords_frame.destroy()
    new_word_frame()


class Application(tk.Frame):


    def __init__(self, master):

        global input_text
        global word_list

        input_text = tk.StringVar()

        tk.Frame.__init__(self, master)
        self.pack(fill=tk.BOTH, expand=1)
        self.winfo_toplevel().title("Low Budget Dictionary")

        self.input_text = tk.StringVar()

        num = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.']

        word_list = list(i for i in wn.words() if i[0] not in num)
        word_list.insert(0, "a")

        menubar = tk.Menu(root)

        self.scrollbar = tk.Scrollbar(self, orient="vertical")

        self.listbox = tk.Listbox(self, yscrollcommand=self.scrollbar.set)
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

        self.listbox.bind('<<ListboxSelect>>', CurSelet)
        self.scrollbar.config(command=self.listbox.yview)


        self.scrollbar.pack(side=tk.LEFT, fill=tk.BOTH)

        self.txtDisplay = tk.Entry(self, textvariable=input_text)
        self.txtDisplay.pack(ipady=6, expand=1)
        self.txtDisplay.config(highlightbackground='#e6e9ef')

        i=0
        for item in word_list:
            self.listbox.insert(i, item)
            i=i+1


        self.button_definition = tk.Button(self, text="Definitions & Example", command=lambda:definitionPress(self.txtDisplay.get().strip()), width=20, height=2)
        self.button_definition.pack(fill=tk.BOTH, expand=1)

        self.button_synonym = tk.Button(self, text="Synonym", command=lambda:synonyms(self.txtDisplay.get().strip()),  width=20, height=2)
        self.button_synonym.pack(fill=tk.BOTH, expand=1)

        self.button_antonym = tk.Button(self, text="Antonym", command=lambda:antonyms(self.txtDisplay.get().strip()), width=20, height=2)
        self.button_antonym.pack(fill=tk.BOTH, expand=1)

        self.button_wordsense = tk.Button(self, text="Word Sense", command=lambda:wordSensePress(self.txtDisplay.get().strip()), width=20, height=2)
        self.button_wordsense.pack(fill=tk.BOTH, expand=1)

        self.addFavorite = tk.Button(self, text="Add to Favorite", command=lambda:addFavorite(self.txtDisplay.get().strip()), width=20, height=2)
        self.addFavorite.pack(fill=tk.BOTH, expand=1)

        self.myFavorite = tk.Button(self, text="My Favorite",command=onMyFavoritePress, width=20, height=2)
        self.myFavorite.pack(fill=tk.BOTH, expand=1)

        self.button_create = tk.Button(self, text="Create New Words", command=onCreateNewWordPress, width=20, height=2)
        self.button_create.pack(fill=tk.BOTH, expand=1)

        # Menu Bar
        # File Tab
        self.filemenu = tk.Menu(menubar, tearoff=0)
        self.filemenu.add_command(label="Display New Word", command=openNewWords)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Exit", command=root.quit)
        menubar.add_cascade(label="File", menu=self.filemenu)

        # Edit Tab
        self.filemenu = tk.Menu(menubar, tearoff=0)
        self.filemenu.add_command(label="Copy")
        self.filemenu.add_command(label="Paste")
        menubar.add_cascade(label="Edit", menu=self.filemenu)

        # Help
        self.filemenu = tk.Menu(menubar, tearoff=0)
        self.filemenu.add_command(label="About", command=showAboutUs)
        menubar.add_cascade(label="Help", menu=self.filemenu)

        root.config(menu=menubar)



root = tk.Tk()
# root.geometry("450x450")

app = Application(root)

root.mainloop()