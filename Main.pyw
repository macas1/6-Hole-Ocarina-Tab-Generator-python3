###Settings
rowSpace = 12
save = True

###GUI Initiation
##Import correctly for both windows and mac
try:
  from tkinter import *
  from tkinter import messagebox
except ImportError:
  from Tkinter import *
  import tkMessageBox as messagebox
from PIL import Image
from datetime import datetime
import os
Dir = os.path.dirname(os.path.abspath(__file__)) + ""
noteList = ["B0", "C1", "C#1", "D1", "Eb1", "E1", "F1", "F#1", "G1", "Ab1", "A1", "Bb1", "B1", "C2", "C#2", "D2", "Eb2", "E2"]

###GUI inititation
root = Tk()
root.wm_title("6 Hole Ocarina Tab Transcriber (C major)")

runConfirm = False
notes = None
saveData = ""
###Functions
def merge_row(imgList):
    result = Image.new('RGB', (68*(len(imgList)+1), 68)) #Get new image size
    for x in range(len(imgList)):
        result.paste(im=Image.open(imgList[x]), box=(68*(x), 0)) #Paste current images into new one
    return result

def merge_column(imgList):
    totalWidth = imgList[0].size[0]-68 #Width from all images are the same (68)
    totalHeight = 68*(len(imgList))
    if rowSpace: totalHeight += rowSpace*len(imgList)
    
    result = Image.new('RGB', (totalWidth, totalHeight))
    currentHeight = 0
    for x in range(len(imgList)):
        result.paste(im=imgList[x], box=(0, currentHeight))
        currentHeight += 68

        if currentHeight != totalHeight and rowSpace:
            spacer = Image.new('RGB', (totalWidth, rowSpace), (255, 255, 255)) #Get new image size
            result.paste(im=spacer, box=(0, currentHeight))
            currentHeight += rowSpace
    return result

###GUI functions
def addText(t):
    text = textWig.get("1.0", 'end-1c')
    if len(text) > 0 and text[-1:] != " " and text[-1:] != "\n": t = " " + t
    textWig.insert(END, t)
    
def button_B0():
    addText("B0 ")

def button_C1():
    addText("C1 ")

def button_D1():
    addText("D1 ")

def button_E1():
    addText("E1 ")

def button_F1():
    addText("F1 ")

def button_G1():
    addText("G1 ")

def button_A1():
    addText("A1 ")

def button_B1():
    addText("B1 ")

def button_C2():
    addText("C2 ")

def button_D2():
    addText("D2 ")

def button_E2():
    addText("E2 ")

def button_Cs1():
    addText("C#1 ")

def button_Eb1():
    addText("Eb1 ")

def button_Fs1():
    addText("F#1 ")

def button_Ab1():
    addText("Ab1 ")

def button_Bb1():
    addText("Bb1 ")

def button_Cs2():
    addText("C#2 ")

def button_Eb2():
    addText("Eb2 ")

def button_space():
    addText("- ")

def button_newLine():
    text = textWig.get("1.0", 'end-1c')
    if text.count("\n") > 3:textWig["height"] = text.count("\n")+2
    textWig.insert(END, "\n")

def button_complete():
    confirm = messagebox.askyesno(message="Is your input complete?", parent=root, title="Confirm")
    if confirm:
        #Get variables
        global notes, saveData, runConfirm
        notes = textWig.get("1.0", 'end-1c')
        saveData = entry_save.get()

        #Process and check for errors
        notes = notes.replace("\n", "/ ")           #Replace new lines
        if notes[-3:] == " / ": notes = notes[:-3]  #Remove leading new lines
        if notes[-1:] == "\n": notes == notes[:-1]
        notes = notes.split(" ")                    #Split into seperate notes


        #remove spaces
        for n in notes:
            if n == "":
                notes.remove(n)
        
        invalid = []
        for n in range(len(notes)):
            #Change spaces and ignore new lines
            if notes[n] == "-":
                notes[n] = "S"
            elif notes[n] != "/":
                #Add octave 1 if no octave is permitted
                changed = False
                try:
                    int(notes[n][-1:])
                except ValueError:    
                    changed = True
                    notes[n] += "1"

                notes[n] = [notes[n][:-1], notes[n][-1:]] #Split octaves from notes

                #Correct sharps
                if notes[n][0] == "Db": notes[n][0] = "C#"
                if notes[n][0] == "D#": notes[n][0] = "Eb"
                if notes[n][0] == "Gb": notes[n][0] = "F#"
                if notes[n][0] == "G#": notes[n][0] = "Ab"
                if notes[n][0] == "A#": notes[n][0] = "Bb"

                #Check if valid and get indexes
                if notes[n][0] and notes[n][0]+notes[n][1] in noteList:
                    notes[n] = str(noteList.index(notes[n][0]+notes[n][1]))
                else:
                    if changed:
                        invalid.append(notes[n][0])
                    else:
                        invalid.append(notes[n][0]+notes[n][1])

        msg = ""
        #Test for save data:
        if os.path.isfile(Dir + "\\Saved\\" + saveData + ".jpg"):
          msg += "There is already a file named " + saveData + " in the directory."
          
        if invalid:
          if msg: msg += "\n\n"
          msg += "The following notes are invalid notes, make sure they are typed correctly and are in the range B0 - E2:\n\n" + " ".join(invalid)
          
        if msg:
          messagebox.showinfo(message=msg, parent=root, title="Error")
        else:
          runConfirm = True
          if saveData == "": saveData = str(datetime.now()).replace(":", "-").split(".")[0]
          root.destroy()

    
###GUI Packing
##menubar

##Mainwindow
textWig = Text(root, width=60, height=5)
textWig.grid(row=0, column=0, columnspan=11, pady=(0, 20))

Button(text="B0", command=button_B0, width=4, height=3).grid(row=2, column=0, pady=(0, 20), padx=(30, 0))
Button(text="C1", command=button_C1, width=4, height=3).grid(row=2, column=1, pady=(0, 20))
Button(text="D1", command=button_D1, width=4, height=3).grid(row=2, column=2, pady=(0, 20))
Button(text="E1", command=button_E1, width=4, height=3).grid(row=2, column=3, pady=(0, 20))
Button(text="F1", command=button_F1, width=4, height=3).grid(row=2, column=4, pady=(0, 20))
Button(text="G1", command=button_G1, width=4, height=3).grid(row=2, column=5, pady=(0, 20))
Button(text="A1", command=button_A1, width=4, height=3).grid(row=2, column=6, pady=(0, 20))
Button(text="B1", command=button_B1, width=4, height=3).grid(row=2, column=7, pady=(0, 20))
Button(text="C2", command=button_C2, width=4, height=3).grid(row=2, column=8, pady=(0, 20))
Button(text="D2", command=button_D2, width=4, height=3).grid(row=2, column=9, pady=(0, 20))
Button(text="E3", command=button_E2, width=4, height=3).grid(row=2, column=10, pady=(0, 20), padx=(0, 30))

Button(text="C#1", command=button_Cs1, width=4, height=2).grid(row=1, column=1, columnspan=2)
Button(text="Eb1", command=button_Eb1, width=4, height=2).grid(row=1, column=2, columnspan=2)
Button(text="F#1", command=button_Fs1, width=4, height=2).grid(row=1, column=4, columnspan=2)
Button(text="Ab1", command=button_Ab1, width=4, height=2).grid(row=1, column=5, columnspan=2)
Button(text="Bb1", command=button_Bb1, width=4, height=2).grid(row=1, column=6, columnspan=2)
Button(text="C#2", command=button_Cs2, width=4, height=2).grid(row=1, column=8, columnspan=2)
Button(text="Eb2", command=button_Eb2, width=4, height=2).grid(row=1, column=9, columnspan=2, padx=(0, 30))

Button(text="Space", command=button_space, width=10, height=1).grid(row=3, column=0, columnspan=2, sticky=E)
Button(text="New line", command=button_newLine, width=10, height=1).grid(row=3, column=2, columnspan=4, sticky=W)
Button(text="Complete", command=button_complete, width=22, height=1).grid(row=4, column=0, columnspan=6, sticky=W, padx=(25, 0))

Label(root, text="""Save Name:""").grid(row=4, column=5, columnspan=3)
entry_save = Entry(root, width=25)
entry_save.grid(row=4, column=7, columnspan=4, sticky=E)

root.mainloop()  #Run GUI window

###Image processing and output
if runConfirm:
    #Split into rows
    data = [[]]
    for n in range(len(notes)):
        if notes[n] == "/":
            data.append([])
        else:
            data[len(data)-1].append(notes[n])

    #Get max row length
    maxRowLen = 0
    for n in data:
        if len(n) > maxRowLen: maxRowLen = len(n)

    #Ajust row length
    for n in data:
        while len(n) != maxRowLen:
            n.append("S")
  
    #Get image file paths
    for n in range(len(data)):
        for m in range(len(data[n])):
            data[n][m] = Dir + "\\Shapes\\Shape " + data[n][m] + ".jpg"

    ###Create images
    #Merge rows
    for n in range(len(data)):
        data[n] = merge_row(data[n])

    #merge and save/show full image
    fin = merge_column(data)
    if save:
        print("Saved: '" + Dir + "\\Saved\\" + saveData+ ".jpg'")
        fin.save(Dir + "\\Saved\\" + saveData+ ".jpg")
    fin.show()
