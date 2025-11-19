import csv, os, random

from PyQt6.QtWidgets import QMainWindow
from gui import Ui_libraryCatalog


def gen_call_back_num(genre):
    """
    Generate a random call back number based on genre
    :param genre:
    :return: int
    """
    if genre == 0:
        return random.randint(0,99)
    elif genre == 1:
        return random.randint(100, 199)
    elif genre == 2:
        return random.randint(200, 299)
    elif genre == 3:
        return random.randint(300, 399)
    elif genre == 4:
        return random.randint(400, 499)
    elif genre == 5:
        return random.randint(500, 599)
    elif genre == 6:
        return random.randint(600, 699)
    elif genre == 7:
        return random.randint(700, 799)
    elif genre == 8:
        return random.randint(800, 899)
    return random.randint(900, 1000)


class Logic(QMainWindow, Ui_libraryCatalog):
    def __init__(self):
        """
        Main setup

        Changes visibility for bookLabel, bookDropDown, and Back button
        Adds genres to the genreDropDown box and sets default to -1 (no option chosen)
        Adds any books in the books.csv file to the bookDropDown box
        Connects buttons enter, view, and back buttons to functions
        """
        super().__init__()
        self.setupUi(self)

        #setting up visibility for bookLabel, bookDropDown, and back Button
        self.bookLabel.setVisible(False)
        self.errorLabel.setText("")
        self.bookDropDown.setVisible(False)
        self.backButton.setVisible(False)

        #adding genres to genreDropDown and setting default values for both combo boxes
        self.genreDropDown.addItems(["CompSci Info General works",
        "Philosophy and psychology", "Religion", "Social Sciences",
        "Language", "Science", "Technology", "Arts and recreation",
        "Literature", "History and geography"])

        self.genreDropDown.setCurrentIndex(-1)

        # add current books in books.csv file to bookDropDown (if csv file is NOT empty)
        if os.path.getsize("books.csv") != 0:
            with open("books.csv", "r") as file:
                next(file)
                for line in file:
                    title = line.split(',')[0]
                    author = line.split(',')[1]

                    self.bookDropDown.addItem(f"{title} by {author}")
        #self.bookDropDown.clear()

        #connecting buttons to functions
        self.enterButton.clicked.connect(lambda: self.enter())
        self.viewButton.clicked.connect(lambda: self.view())
        self.backButton.clicked.connect(lambda: self.back())


    # enter
    def enter(self):
        """
        Takes in user input for title, author, and genre,
        and adds them to bookDropDown box as well as books.csv, along with a call back number

        If the title or author is empty, or the author entered is a number, or no genre was chosen,
        show error label and clear input.
        """
        if self.titleInput.text() == "" or self.authorInput.text() == "" or self.authorInput.text().isdigit() or self.genreDropDown.currentIndex() == -1:
            self.errorLabel.setText("Please enter a title, author, and select a genre \n" + "Note: DO NOT ENTER NUMBERS FOR AUTHOR")
            # clear all input
            self.titleInput.clear()
            self.authorInput.clear()
            self.genreDropDown.setCurrentIndex(-1)

            # set focus to titleInput
            self.titleInput.setFocus()

        else:
            title = self.titleInput.text().strip()
            author = self.authorInput.text().strip()
            genre = self.genreDropDown.currentIndex()
            call_back = gen_call_back_num(genre)

            with open("books.csv", "a", newline='') as file:
                csv_writer = csv.writer(file)

                if os.path.getsize("books.csv") == 0:
                    csv_writer.writerow(["Title", "Author", "Genre", "Callback"])

                # sorting and writing to csv
                csv_writer.writerow([title, author, str(self.genreDropDown.currentText()).strip(), call_back])

            # add book to bookDropDown
            self.bookDropDown.addItem(f"{title} by {author}")

            # clear all input
            self.titleInput.clear()
            self.authorInput.clear()
            self.genreDropDown.setCurrentIndex(-1)
            self.errorLabel.setText("")

            # set focus to titleInput
            self.titleInput.setFocus()

    # view
    def view(self):
        """
        Change Screens to look at current books in the books.csv file
        """
        self.bookDropDown.setCurrentIndex(-1)

        # hide widgets on main page
        self.titleLabel.setVisible(False)
        self.titleInput.setVisible(False)
        self.authorLabel.setVisible(False)
        self.authorInput.setVisible(False)
        self.genreLabel.setVisible(False)
        self.genreDropDown.setVisible(False)
        self.enterButton.setVisible(False)
        self.viewButton.setVisible(False)
        self.errorLabel.setText("")

        # show widgets for book viewing
        self.bookLabel.setVisible(True)
        self.bookDropDown.setVisible(True)
        self.backButton.setVisible(True)


    # back
    def back(self):
        """
        From the book viewing screen, return to the main screen
        """
        # back to main book catalog page
        self.titleLabel.setVisible(True)
        self.titleInput.setVisible(True)
        self.authorLabel.setVisible(True)
        self.authorInput.setVisible(True)
        self.genreLabel.setVisible(True)
        self.genreDropDown.setVisible(True)
        self.enterButton.setVisible(True)
        self.viewButton.setVisible(True)
        self.errorLabel.setText("")

        self.bookLabel.setVisible(False)
        self.bookDropDown.setVisible(False)
        self.backButton.setVisible(False)