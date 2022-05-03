from modules import *

def main():
    #table view
    data = DataLoader.Data()
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
        print(data.f_movies.head())

    #GUI:
    turnon = 0  ################################# YOU CAN TURN OFF THE GUI HERE
    if turnon:
        root = tk.Tk()
        root.iconphoto(False, tk.PhotoImage(file='img\\icon1.png'))
        root.title("MOVIE RATING PREDICTOR")
        root.resizable(0, 0)
        canvas = tk.Canvas(root, width=600, height=300)
        canvas.grid(columnspan=13, rowspan=5)
        logo = Image.open('img\\logo3.png')
        logo = ImageTk.PhotoImage(logo)
        logo_label = tk.Label(image=logo)
        logo_label.image = logo
        logo_label.place(x=0, y=0, relwidth=1, relheight=1)
        entry1 = tk.Entry(root, width=5)
        entry2 = tk.Entry(root, width=5)
        entry3 = tk.Entry(root, width=5)
        entry4 = tk.Entry(root, width=5)
        entry5 = tk.Entry(root, width=5)
        entry6 = tk.Entry(root, width=5)
        entry7 = tk.Entry(root, width=5)
        entry1.grid(row=2, column=0)
        entry2.grid(row=2, column=1)
        entry3.grid(row=2, column=2)
        entry4.grid(row=2, column=3)
        entry5.grid(row=2, column=4)
        entry6.grid(row=2, column=5)
        entry7.grid(row=2, column=6)
        root.mainloop()
    else:
        pass


if __name__ == "__main__":
    main()

