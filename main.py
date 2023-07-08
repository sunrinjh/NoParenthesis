import tkinter as tk
import tkinter.font
import tarfile
from tempfile import TemporaryDirectory
import os
from tkinter import filedialog
from tkinter import simpledialog
from tkinter import ttk
from PIL import ImageTk, Image
from pdf2img import findFromFile


app = tk.Tk()
app.geometry("800x600")
tabControl = ttk.Notebook(app)
tabControl.pack(expand=True, fill="both")
loaderTab = ttk.Frame(tabControl, width=800, height=300)
viewerTab = ttk.Frame(tabControl, width=800, height=300)

tabControl.add(loaderTab, text="Loader")
tabControl.add(viewerTab, text="Viewer")


filename: str = ""
booknameInput = tk.StringVar()
eqnnumInput = tk.StringVar()

tempdir = TemporaryDirectory().name


def select_file(booknameInput: str):
    bookname = booknameInput.get()
    if bookname == "":
        return
    while os.path.exists("./data/" + bookname):
        bookname = simpledialog.askstring(
            title="Re-Enter Your Bookname", prompt="Duplicated Bookname."
        )

    filetypes = (("PDF files", "*.pdf"),)

    filename = filedialog.askopenfilename(
        title="Open a file", initialdir="~", filetypes=filetypes
    )
    print(filename)
    findFromFile(filepath=filename, bookname=bookname)
    combo.config(values=os.listdir("./data"))


loader_Label = ttk.Label(
    loaderTab,
    text="Write Down Your Book Name. (It will be the database's file name)\nIf you don't you can't select the file. sry\nLoading will take some time, it's good time to stand up from your desk and drink some water.",
    font=tkinter.font.Font(family="맑은 고딕", size=12),
)
loader_Label.pack()

name_entry = ttk.Entry(
    loaderTab,
    width=50,
    textvariable=booknameInput,
    font=tkinter.font.Font(family="맑은 고딕", size=12),
)
name_entry.pack(expand=True)

open_button = ttk.Button(
    loaderTab, text="Open a File", command=lambda: select_file(booknameInput)
)
open_button.pack(expand=True)

equationNumber_entry = ttk.Entry(
    viewerTab,
    width=30,
    textvariable=eqnnumInput,
    font=tkinter.font.Font(family="맑은 고딕", size=10),
)
equationNumber_entry.pack(expand=True)

combo = ttk.Combobox(viewerTab, state="readonly", values=os.listdir("./data"))
def comboboxSelected(eventObject):
    print(tempdir)
    selection = combo.get()
    if not os.path.exists(tempdir + "/" + selection):
        with tarfile.open("./data/" + selection, "r") as tar:
            os.makedirs(tempdir + "/" + selection)
            tar.extractall(path=(tempdir +"/" +selection))
            

combo.bind("<<ComboboxSelected>>", comboboxSelected)
combo.pack()


img = Image.open("DoNotDelete.png")
img = img.resize(
    (round(img.width / img.width * 800), round(img.height / img.width * 800))
)
eqnImage = ImageTk.PhotoImage(image=img)

eqnImage_Canvas = tk.Canvas(viewerTab, width=800, height=500)

imgArea = eqnImage_Canvas.create_image(400, 250, image=eqnImage)
eqnImage_Canvas.image = img
eqnImage_Canvas.pack(expand=True)



def update_image(var, index, mode):
    global current
    selection = combo.get()

    global imgArea, img, eqnImage, eqnImage_Canvas
    if os.path.exists(tempdir + "/" + selection + "/" + eqnnumInput.get() + ".png"):
        img = Image.open(tempdir + "/" + selection + "/" + eqnnumInput.get() + ".png")
        img = img.resize(
            (round(img.width / img.width * 800), round(img.height / img.width * 800))
        )
        eqnImage = ImageTk.PhotoImage(image=img)
        eqnImage_Canvas.itemconfig(imgArea, image=eqnImage)
        eqnImage_Canvas.image = img


eqnnumInput.trace("w", update_image)

app.mainloop()
