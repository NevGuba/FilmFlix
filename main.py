import tkinter as tk
from tkinter import ttk
import sqlite3
from connect import *
from tkinter import messagebox

def readAll():
    windowRead = tk.Tk()
    windowRead.title("Read All Records")
    titleLabel = ttk.Label(master=windowRead, text='FilmFlix', font='Candara 25 bold')
    titleLabel.pack()
    dbCursor.execute("SELECT * FROM tblFilms")
    allRecords = dbCursor.fetchall()
    printRecords = ''
    for eachRecord in allRecords:
        printRecords += str(eachRecord[0]) + " " + str(eachRecord[1])+ " " + str(eachRecord[2])+ " " + str(eachRecord[3])+ " " + str(eachRecord[4])+ " " + str(eachRecord[5]) + "\n"
    recordsLabel = ttk.Label(windowRead, text=printRecords)
    recordsLabel.pack()    

def searchRecords():
    def searchValue():
        searchValue = entry.get()
        dbCursor.execute(
        f"SELECT * FROM tblFilms WHERE LOWER(Title) LIKE '%{searchValue}%' "
        f"OR LOWER(yearReleased) LIKE '%{searchValue}%' "
        f"OR LOWER(Rating) LIKE '%{searchValue}%'"
        f"OR LOWER(Duration) LIKE '%{searchValue}%'"
        f"OR LOWER(Genre) LIKE '%{searchValue}%'")
        allRecords = dbCursor.fetchall()
        printRecords = ''
        for eachRecord in allRecords:
            printRecords += str(eachRecord[0]) + " " + str(eachRecord[1])+ " " + str(eachRecord[2])+ " " + str(eachRecord[3])+ " " + str(eachRecord[4])+ " " + str(eachRecord[5]) + "\n"
        recordsLabel.config(text=printRecords)
        
    def clearResults():
        recordsLabel.config(text='')
        entry.delete(0, tk.END)  

    def onEnterPressed(event):
        searchValue()
        
    searchWindow = tk.Tk()
    searchWindow.geometry('400x600')

    mainFrame = tk.Frame(searchWindow)
    mainFrame.pack(fill='both', expand=1)

    myCanvas = tk.Canvas(mainFrame)
    myCanvas.pack(side='left', fill='both', expand=1)

    scrollbar = tk.Scrollbar(mainFrame, orient='vertical', command=myCanvas.yview)
    scrollbar.pack(side='right', fill='y')

    myCanvas.configure(yscrollcommand=scrollbar.set)
    myCanvas.bind('<Configure>', lambda e: myCanvas.configure(scrollregion=myCanvas.bbox("all")))

    secondFrame = tk.Frame(myCanvas)
    myCanvas.create_window((0, 0), window=secondFrame, anchor='nw')

    searchWindow.title('Search Records')  # Set the title of the searchWindow

    titleLabel = ttk.Label(master=secondFrame, text='FilmFlix', font='Candara 25 bold')
    titleLabel.pack()

    recordsLabel = ttk.Label(secondFrame, text='')
    recordsLabel.pack()

    entry = ttk.Entry(master=secondFrame)
    entry.pack()

    button = ttk.Button(master=secondFrame, text='Search', command=searchValue)
    button.pack()

    clearButton = ttk.Button(master=secondFrame, text='Clear', command=clearResults)
    clearButton.pack()
    #searchWindow.mainloop()
    

def addRecord():
    def submitRecord():
        titleValue = title.get().title()
        yearreleasedValue = yearReleased.get()
        ratingValue = rating.get().upper()
        durationValue = duration.get()
        genreValue = genre.get().title()

        valid_ratings = ["G", "PG", "R"]

        if titleValue and yearreleasedValue and ratingValue and durationValue and genreValue:
            if yearreleasedValue.isdigit() and durationValue.isdigit():
                if ratingValue in valid_ratings:
                    dbCursor.execute("INSERT INTO tblFilms (title, yearReleased, rating, duration, genre) VALUES(?,?,?,?,?)", (titleValue, yearreleasedValue, ratingValue, durationValue, genreValue))
                    dbCon.commit() 
                    messagebox.showinfo("Success", "Record added successfully!")
                    title.delete(0, tk.END)
                    yearReleased.delete(0, tk.END)
                    rating.delete(0, tk.END)
                    duration.delete(0, tk.END)
                    genre.delete(0, tk.END)

                elif ratingValue not in valid_ratings:
                    messagebox.showwarning("Error", "Rating must be G, PG, or R.")
            else:
                messagebox.showwarning("Error", "Year Released and Duration must be in numbers")
        else:
            messagebox.showwarning("Error", "Please fill in all fields.")

    addWindow = tk.Tk()
    addWindow.title('Add Record')
    titleLabel = ttk.Label(master=addWindow, text='FilmFlix', font='Candara 25 bold')
    titleLabel.grid(row = 0, column = 1)
    # Create Text Boxes
    title = ttk.Entry(addWindow, width=30)
    title.grid(row=2, column=1,)
    yearReleased = ttk.Entry(addWindow, width=30)
    yearReleased.grid(row=3, column=1)
    rating = ttk.Entry(addWindow, width=30)
    rating.grid(row=4, column=1)
    duration = ttk.Entry(addWindow, width=30)
    duration.grid(row=5, column=1)
    genre = ttk.Entry(addWindow, width=30)
    genre.grid(row=6, column=1)
    # Create Text Box Labels
    titleLabel = ttk.Label(addWindow, text='Title')
    titleLabel.grid(row = 2, column = 0)
    yearReleasedLabel = ttk.Label(addWindow, text='Year Released')
    yearReleasedLabel.grid(row = 3, column = 0)
    ratingLabel = ttk.Label(addWindow, text='Rating')
    ratingLabel.grid(row = 4, column = 0)
    durationLabel = ttk.Label(addWindow, text='Duration')
    durationLabel.grid(row = 5, column = 0)
    genreLabel = ttk.Label(addWindow, text='Genre')
    genreLabel.grid(row = 6, column = 0)

    button = ttk.Button(master=addWindow, text='Submit', command=submitRecord) 
    button.grid(row = 7, column = 1)


def updateRecord():
    def showInfo():
        searchValue = updateField.get()
        dbCursor.execute("SELECT * FROM tblFilms WHERE oid = ?", (searchValue,))
        valueID = dbCursor.fetchall()

        if valueID:
            for id in valueID:
                title.delete(0, tk.END)
                title.insert(0, id[1])
                yearReleased.delete(0, tk.END)
                yearReleased.insert(0, id[2])
                rating.delete(0, tk.END)
                rating.insert(0, id[3])
                duration.delete(0, tk.END)
                duration.insert(0, id[4])
                genre.delete(0, tk.END)
                genre.insert(0, id[5])

            updateField.config(state="disabled")
        else:
            messagebox.showinfo("Error", "No record found for the given ID.")

    def saveChanges():
        # Retrieve values from the entry fields
        new_title = title.get().title()
        new_year_released = yearReleased.get()
        new_rating = rating.get().upper()
        new_duration = duration.get()
        new_genre = genre.get().title()
        searchValue = updateField.get()

        valid_ratings = ["G", "PG", "R"]

        if new_title and new_year_released and new_rating and new_duration and new_genre:
            if new_year_released.isdigit() and new_duration.isdigit():
                if new_rating in valid_ratings:
                        # Update the record in the database
                        dbCursor.execute("UPDATE tblFilms SET title=?, yearReleased=?, rating=?, duration=?, genre=? WHERE oid=?", (new_title, new_year_released, new_rating, new_duration, new_genre, searchValue))
                        dbCon.commit()  # Commit the changes to the database
                        messagebox.showinfo("Success", "Record updated successfully!")
                        updateField.config(state="normal")
                else:
                    messagebox.showwarning("Error", "Rating must be G, PG, or R.")
            else:
                messagebox.showwarning("Error", "Year Released and Duration must be integers.")
        else:
            messagebox.showwarning("Error", "Please fill in all fields.")

    updateWindow = tk.Tk()
    updateWindow.title('Update Record')

    titleLabel = ttk.Label(master=updateWindow, text='FilmFlix', font='Candara 25 bold')
    titleLabel.grid(row=0, column=1)

    updateField = ttk.Entry(updateWindow, width=30)
    updateField.grid(row=1, column=1)
    updateLabel = ttk.Label(updateWindow, text='Enter ID')
    updateLabel.grid(row=1, column=0)
    #Button 
    showRecordBtn = ttk.Button(updateWindow, text='Submit', command=showInfo)
    showRecordBtn.grid(row=1, column=2)
    #Entry Boxes
    title = ttk.Entry(updateWindow, width=30)
    title.grid(row=3, column=1)
    yearReleased = ttk.Entry(updateWindow, width=30)
    yearReleased.grid(row=4, column=1)
    rating = ttk.Entry(updateWindow, width=30)
    rating.grid(row=5, column=1)
    duration = ttk.Entry(updateWindow, width=30)
    duration.grid(row=6, column=1)
    genre = ttk.Entry(updateWindow, width=30)
    genre.grid(row=7, column=1)

    # Create Text Box Labels
    titleLabel = ttk.Label(updateWindow, text='Title')
    titleLabel.grid(row=3, column=0)
    yearReleasedLabel = ttk.Label(updateWindow, text='Year Released')
    yearReleasedLabel.grid(row=4, column=0)
    ratingLabel = ttk.Label(updateWindow, text='Rating')
    ratingLabel.grid(row=5, column=0)
    durationLabel = ttk.Label(updateWindow, text='Duration')
    durationLabel.grid(row=6, column=0)
    genreLabel = ttk.Label(updateWindow, text='Genre')
    genreLabel.grid(row=7, column=0)

    saveBtn = ttk.Button(updateWindow, text='Save', command=saveChanges)
    saveBtn.grid(row=8, column=1)

    updateWindow.mainloop()

####### DELETE WINDOW #######

def deleteRecord():
    def showInfo():
        searchValue = deleteField.get()
        dbCursor.execute("SELECT * FROM tblFilms WHERE oid = ?", (searchValue,))
        valueID = dbCursor.fetchall()

        if valueID:
            for id in valueID:
                title.delete(0, tk.END)
                title.insert(0, id[1])
                yearReleased.delete(0, tk.END)
                yearReleased.insert(0, id[2])
                rating.delete(0, tk.END)
                rating.insert(0, id[3])
                duration.delete(0, tk.END)
                duration.insert(0, id[4])
                genre.delete(0, tk.END)
                genre.insert(0, id[5])

            deleteField.config(state="disabled")
            title.config(state="disabled")
            yearReleased.config(state="disabled")
            rating.config(state="disabled")
            duration.config(state="disabled")
            genre.config(state="disabled")

        else:
            messagebox.showinfo("Error", "No record found for the given ID.")
    def deleteNow():
        response = messagebox.askyesno("Confirm", "Are you sure you want to delete this record?")
        searchValue = deleteField.get()
        if response == 1:
            dbCursor.execute("DELETE FROM tblFilms WHERE oid =?", (searchValue,))
            dbCon.commit() 
            dbCon.close() # Commit the changes to the database
            messagebox.showinfo("Success", "Record updated successfully!")
            deleteField.config(state="normal")
            title.config(state="normal")
            yearReleased.config(state="normal")
            rating.config(state="normal")
            duration.config(state="normal")
            genre.config(state="normal")
            deleteField.delete(0, tk.END)
            title.delete(0, tk.END)
            yearReleased.delete(0, tk.END)
            rating.delete(0, tk.END)
            duration.delete(0, tk.END)
            genre.delete(0, tk.END)

    deleteWindow = tk.Tk()
    deleteWindow.title('Delete Record')

    titleLabel = ttk.Label(master=deleteWindow, text='FilmFlix', font='Candara 25 bold')
    titleLabel.grid(row=0, column=1)

    deleteField = ttk.Entry(deleteWindow, width=30)
    deleteField.grid(row=1, column=1)
    deleteLabel = ttk.Label(deleteWindow, text='Enter ID')
    deleteLabel.grid(row=1, column=0)
    #Button 
    showRecordBtn = ttk.Button(deleteWindow, text='Submit', command=showInfo)
    showRecordBtn.grid(row=1, column=2)
    #Entry Boxes
    title = ttk.Entry(deleteWindow, width=30)
    title.grid(row=3, column=1)
    yearReleased = ttk.Entry(deleteWindow, width=30)
    yearReleased.grid(row=4, column=1)
    rating = ttk.Entry(deleteWindow, width=30)
    rating.grid(row=5, column=1)
    duration = ttk.Entry(deleteWindow, width=30)
    duration.grid(row=6, column=1)
    genre = ttk.Entry(deleteWindow, width=30)
    genre.grid(row=7, column=1)

    # Create Text Box Labels
    titleLabel = ttk.Label(deleteWindow, text='Title')
    titleLabel.grid(row=3, column=0)
    yearReleasedLabel = ttk.Label(deleteWindow, text='Year Released')
    yearReleasedLabel.grid(row=4, column=0)
    ratingLabel = ttk.Label(deleteWindow, text='Rating')
    ratingLabel.grid(row=5, column=0)
    durationLabel = ttk.Label(deleteWindow, text='Duration')
    durationLabel.grid(row=6, column=0)
    genreLabel = ttk.Label(deleteWindow, text='Genre')
    genreLabel.grid(row=7, column=0)

    deleteBtn = ttk.Button(deleteWindow, text='Delete', command=deleteNow)
    deleteBtn.grid(row=8, column=1)

    deleteWindow.mainloop()


# Window - Main Menu 
window = tk.Tk()
window.title("Film Flix")
window.geometry('400x200')

# Navigation Menu
# Title - Main Menu 
titleLabel = ttk.Label(master=window, text='FilmFlix', font='Candara 25 bold')
titleLabel.pack()

# Read All Button 
readAllBtn = ttk.Button(master=window, text='Read All Records', command = readAll)
readAllBtn.pack()

# Search Button 
searchBtn = ttk.Button(master=window, text='Search Record', command = searchRecords)
searchBtn.pack()

# Add Button 
addBtn = ttk.Button(master=window, text='Add a Record', command = addRecord)
addBtn.pack()

# Update Button 
updateBtn = ttk.Button(master=window, text='Update a Record', command = updateRecord)
updateBtn.pack()

# Delete Button 
deleteButton = ttk.Button(master=window, text='Delete a Record', command = deleteRecord)
deleteButton.pack()

#Run 
window.mainloop()
