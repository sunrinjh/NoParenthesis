import tkinter
from tkinter import filedialog
from tkinter import ttk
from pdf2img import findFromFile

app = tkinter.Tk()
filename:str = ""
def select_file():
    filetypes = (("PDF files", "*.pdf"), )

    filename = filedialog.askopenfilename(
        title="Open a file", initialdir="~", filetypes=filetypes
    )
    print(filename)
    findFromFile(filename)
    
    


open_button = ttk.Button(app, text="Open a File", command=select_file)
open_button.pack(expand=True)

app.mainloop()

