import csv, os, random

from PyQt6.QtWidgets import QMainWindow
from gui import Ui_libraryCatalog


def gen_call_back_num(genre: str) -> int:
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


def contains_char(text: str, lst: list) -> bool:
    """
    :param text:
    :param lst:
    :return bool:

    if a "forbidden" character from lst is found in text, return True. Otherwise, return False.
    """

    for i in range(len(lst)):
        if lst[i] in text:
            return True
    return False



class Logic(QMainWindow, Ui_libraryCatalog):
    def __init__(self) -> None:
        """
        Main setup

        Changes visibility for errorLabel and sets index to -1 for both combo boxes
        Adds genres to the genreDropDown box
        Adds any books in the books.csv file to the bookDropDown box
        Connects enter, view, and back buttons
        """
        super().__init__()
        self.setupUi(self)

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

                    self.bookDropDown.addItem(title)

        self.bookDropDown.setCurrentIndex(-1)

        #connecting buttons to functions
        self.enterButton.clicked.connect(lambda: self.enter())
        self.viewButton.clicked.connect(lambda: self.view())
        self.backButton.clicked.connect(lambda: self.back())
        self.bookViewButton.clicked.connect(lambda: self.bookView())


    # enter
    def enter(self):
        """
        Takes in user input for title, author, and genre,
        and adds them to bookDropDown box as well as books.csv, along with a call back number

        If the title or author is empty, or the author entered is a number,
        or no genre was chosen,
        or any of the text inputs contain a "forbidden" character ,
        show error label and clear input.
        """
        chars = ["<", ">", "@", "#", "$", "%", "^", "~" "*", "(", ")"]
        title_chars = contains_char(self.titleInput.text(), chars)
        author_chars = contains_char(self.authorInput.text(), chars)

        if (self.titleInput.text() == ""
        or self.authorInput.text() == ""
        or self.authorInput.text().isdigit()
        or self.genreDropDown.currentIndex() == -1
        or title_chars or author_chars):

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

            with open("books.csv", "a+", newline='') as file:
                csv_writer = csv.writer(file)

                if os.path.getsize("books.csv") == 0:
                    csv_writer.writerow(["Title", "Author", "Genre", "Callback"])

                # writing current book info to csv
                csv_writer.writerow([title, author, str(self.genreDropDown.currentText()).strip(), call_back])

            # add book to bookDropDown
            self.bookDropDown.addItem(title)

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
        Change Screens to bookView window
        """
        self.windows.setCurrentIndex(1)
        self.bookDropDown.setCurrentIndex(-1)
        self.bookTitleLabel.setText("")
        self.bookAuthorLabel.setText("")
        self.bookGenreLabel.setText("")
        self.bookCallLabel.setText("")


    # back
    def back(self):
        """
        From the book viewing screen, return to the main screen
        """
        # back to main book catalog page
        self.titleInput.clear()
        self.authorInput.clear()
        self.genreDropDown.setCurrentIndex(-1)
        self.windows.setCurrentIndex(0)
        self.errorLabel.setText("")

        # set focus to titleInput
        self.titleInput.setFocus()


    def bookView(self):
        if self.bookDropDown.currentIndex() != -1:
            self.bookErrorLabel.setText("")
            with open("books.csv", "r") as file:
                for line in file:
                    if self.bookDropDown.currentText() in line:
                        self.bookTitleLabel.setText(f"Title: {line.split(',')[0]}")
                        self.bookAuthorLabel.setText(f"Author: {line.split(',')[1]}")
                        self.bookGenreLabel.setText(f"Genre: {line.split(',')[2]}")
                        self.bookCallLabel.setText(f"Callback: {line.split(',')[3]}")
        else:
            self.bookErrorLabel.setText("Please select a book")

