from tabnanny import check
from modules import *
import tkinter as tk
from PIL import Image, ImageTk

class GUI:
    def __init__(self, ann):
        #main tkinter object
        self.ann = ann
        self.user_input = user_input.UserInput(ann)
        self.root = tk.Tk()
        #small icon
        self.root.iconphoto(False, tk.PhotoImage(file='img\\icon1.png'))
        #window title
        self.root.title("MOVIE RATING PREDICTOR")
        #disallows resizing the window
        self.root.resizable(0, 0)
        #tkinter canvas
        self.canvas = tk.Canvas(self.root, width=600, height=300)
        #setting up the grid
        self.canvas.grid(columnspan=13, rowspan=5)
        #logo
        self.logo = Image.open('img\\logo4.png')
        self.logo = ImageTk.PhotoImage(self.logo)
        self.logo_label = tk.Label(image=self.logo)
        self.logo_label.image = self.logo
        self.logo_label.place(x=0, y=0, relwidth=1, relheight=1)
        self.entries = self.entry_definition()
        self.text_boxes = self.text_boxes()
        self.buttons = self.button_definitions()
        self.root.mainloop()

    def entry_definition(self):
        #entry definitions
        self.entry1 = tk.Entry(self.root, width=5, bg='gray')
        self.entry2 = tk.Entry(self.root, width=5, bg='gray')
        self.entry3 = tk.Entry(self.root, width=5, bg='gray')
        self.entry4 = tk.Entry(self.root, width=5, bg='gray')
        self.entry5 = tk.Entry(self.root, width=5, bg='gray')
        self.entry6 = tk.Entry(self.root, width=5, bg='gray')
        self.entry7 = tk.Entry(self.root, width=5, bg='gray')
        self.entry8 = tk.Entry(self.root, width=5, bg='gray')
        self.entry9 = tk.Entry(self.root, width=5, bg='gray')
        self.entry10 = tk.Entry(self.root, width=5, bg='gray')
        #screen position
        self.entry1.grid(row=2, column=0)
        self.entry2.grid(row=2, column=1)
        self.entry3.grid(row=2, column=2)
        self.entry4.grid(row=2, column=3)
        self.entry5.grid(row=2, column=4)
        self.entry6.grid(row=3, column=0)
        self.entry7.grid(row=3, column=1)
        self.entry8.grid(row=3, column=2)
        self.entry9.grid(row=3, column=3)
        self.entry10.grid(row=3, column=4)
        entries = [self.entry1, self.entry2, self.entry3, self.entry4, 
                    self.entry5, self.entry6, self.entry7, 
                    self.entry8, self.entry9, self.entry10]
        return entries

    def text_boxes(self):
        #current values textbox
        T = tk.Text(self.root, height = 1, width = 20, bg='gray')
        T.grid(row=2, column=7)

        #prediction textbox
        P = tk.Text(self.root, height = 1, width = 10, bg='gray')
        P.grid(row=3, column=7)
        #text boxes
        text_boxes = [T, P]
        return text_boxes

    def clear_entry_boxes(self):
        for entry in self.entries:
            entry.delete(0, tk.END)

    def read_input(self):
        entry_values = []
        for entry in self.entries:
            if not entry.get():
                entry_values.append('0')
            else:
                entry_values.append(entry.get())
        self.text_boxes[0].configure(state='normal')
        self.text_boxes[0].delete('1.0', tk.END)
        self.text_boxes[0].insert(tk.END, entry_values)
        self.text_boxes[0].config(state=tk.DISABLED)
        self.user_input.entries = entry_values
        self.user_input.new_row = self.user_input.create_row()  
        self.user_input.send_row()
        X, y, self.ann.user_row , PredictorScalerFit, TargetVarScalerFit, X_train, X_test, y_train, y_test = self.user_input.train_and_test.scaling(with_extraction=True)

    def range_threshold(self, func):
        output = func()[0][0]
        if output > 10:
            output = 10
        elif output < 1:
            output = 1 
        return output 

    def Prediction(self):
        self.read_input()
        self.text_boxes[1].configure(state='normal')
        self.text_boxes[1].delete('1.0', tk.END) #clearuje za kazdym razem text box
        self.text_boxes[1].insert(tk.END, round(self.range_threshold(self.ann.prediction_constraint),2))
        self.text_boxes[1].config(state=tk.DISABLED) #blokuje edyotowanie
         

    def button_definitions(self):
        b1 = tk.Button(self.root, text='   Clear all   ', 
                   command=self.clear_entry_boxes, bg='gray').grid(row=4, 
                                                            column=1, 
                                                            sticky=tk.W, 
                                                            pady=4)
        #PREDICT BUTTON
        b2 = tk.Button(self.root, text='    Predict    ', 
                    command=self.Prediction, bg='grey').grid(row=4, 
                                                  column=3, 
                                                  sticky=tk.W, 
                                                  pady=4)
        buttons = [b1, b2]
        return buttons

    
        


        
    
        