from tkinter import Frame, Label, Tk, BOTH, Text, Menu, INSERT, END, filedialog
from tkinter.ttk import Frame, Button, Style
import tkinter.messagebox as mbox
from PIL import Image, ImageTk

from copy_move_detection import CM_Detection


class aFrame(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.img_name = ""
        self.initUI()

    def initUI(self):
        self.parent.title("Image Copy-Move Detection")
        self.style = Style().configure("TFrame", background="#333")
        self.pack(fill=BOTH, expand=1)

        open_button = Button(self, text="Open File", command=self.onFilePicker)
        open_button.place(x=10, y=10)

        detect_button = Button(self, text="Detect", command=self.onDetect)
        detect_button.place(x=10, y=40)

        self.textBoxFile = Text(self, state='disabled', width=80, height = 1)
        self.textBoxFile.place(x=90, y=10)

        self.textBoxLog = Text(self, state='disabled', width=40, height=3)
        self.textBoxLog.place(x=90, y=40)

        # absolute image widget
        imageLeft = Image.open("resource/empty.png")
        imageLeftLabel = ImageTk.PhotoImage(imageLeft)
        self.labelLeft = Label(self, image=imageLeftLabel)
        self.labelLeft.image = imageLeftLabel
        self.labelLeft.place(x=5, y=100)

        imageRight = Image.open("resource/empty.png")
        imageRightLabel = ImageTk.PhotoImage(imageRight)
        self.labelRight = Label(self, image=imageRightLabel)
        self.labelRight.image = imageRightLabel
        self.labelRight.place(x=525, y=100)

        self.centerWindow()

    def centerWindow(self):
        w = 1045
        h = 620

        sw = self.parent.winfo_screenwidth()
        sh = self.parent.winfo_screenheight()

        x = (sw - w)/2
        y = (sh - h)/2
        self.parent.geometry('%dx%d+%d+%d' % (w, h, x, y))

    def onFilePicker(self):

        ftypes = [('PNG Files', '*.png'), ('All files', '*')]
        dlg = filedialog.Open(self, initialdir='/', filetypes = ftypes)
        choosedFile = dlg.show()

        if choosedFile != '':
            self.img_name = str(choosedFile).split("/")[-1]
            self.imgPath = str(choosedFile).replace(self.img_name, '')

            self.textBoxFile.config(state='normal')
            self.textBoxFile.delete('1.0', END)
            self.textBoxFile.insert(END, choosedFile)
            self.textBoxFile.config(state='disabled')

            newImageLeft = Image.open(choosedFile)
            imageLeftLabel = ImageTk.PhotoImage(newImageLeft)
            self.labelLeft = Label(self, image=imageLeftLabel)
            self.labelLeft.image = imageLeftLabel
            self.labelLeft.place(x=5, y=100)

            imageRight = Image.open("resource/empty.png")
            imageRightLabel = ImageTk.PhotoImage(imageRight)
            self.labelRight = Label(self, image=imageRightLabel)
            self.labelRight.image = imageRightLabel
            self.labelRight.place(x=525, y=100)

        pass

    def onDetect(self):
        if self.img_name == "":
            mbox.showerror("Error", 'No image selected\nSelect an image by clicking "Open File"')
        else:

            self.textBoxLog.config(state='normal')
            self.textBoxLog.insert(END, "Detecting: "+self.img_name+"\n")
            self.textBoxLog.see(END)
            self.textBoxLog.config(state='disabled')

            # imageResultPath = main.detect(self.imgPath, self.img_name, '../Copy_Move_Forgery_Detection/Outputs/', block_size=16)
            self.input_img_path = self.imgPath + self.img_name
            image_inst = CM_Detection(self.input_img_path,self.img_name, '../Copy_Move_Forgery_Detection/Outputs/', block_size = 16 )
            imageResultPath = image_inst.run()
            newImageRight = Image.open(imageResultPath)
            imageRightLabel = ImageTk.PhotoImage(newImageRight)
            self.labelRight = Label(self, image=imageRightLabel)
            self.labelRight.image = imageRightLabel
            self.labelRight.place(x=525, y=100)

            self.textBoxLog.config(state='normal')
            self.textBoxLog.insert(END, "Done.")
            self.textBoxLog.see(END)
            self.textBoxLog.config(state='disabled')

if __name__ == '__main__':
    root = Tk()
    app = aFrame(root)
    root.mainloop()