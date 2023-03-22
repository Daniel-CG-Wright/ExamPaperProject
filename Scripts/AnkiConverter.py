import sqlite3
import genanki
import re
from typing import List
import re
from typing import List
from sqlitehandler import *
from Frontend.Util.QuestionPartFunctionHelpers import *




class Anki_card_model: #defining a model for a single card
    def __init__(self):
        self.my_model = genanki.Model(
        1607392319,
        'Simple Model',
        fields=[
            {'name': 'Question'},
            {'name': 'Answer'},
        ],
        templates=[
            {
            'name': 'Card 1',
            'qfmt': '{{Question}}',
            'afmt': '{{FrontSide}}<hr id="answer">{{Answer}}',
            },
        ])
class Anki_converter(Anki_card_model):
    def __init__(self, path_to_database, name):
        super().__init__()
        self.db_path = path_to_database
        self.name = name
        self.my_deck = genanki.Deck(2059400110, self.name)

    def add_cards(self, questions):
        front_list =  questions# put all of the questions here
        #back_list = [] #put all of the question numbers and from which paper
        print(self.db_path)
        print(len(front_list))
        query = SQLiteHandler.queryDatabase(SQLiteHandler(), 'SELECT QuestionID FROM QUESTION')
        connection = sqlite3.connect("Database/ExamQuestions.db")
        cursor = connection.cursor()
        w = cursor.execute('SELECT QuestionID FROM QUESTION')
        z = w.fetchall()
        for i in range(0,len(front_list)-1):
            ret = GetFullMarkscheme(SQLiteHandler(),  str(z[i])[1:-2][1:-1])
            question = '{}'.format(ret)
            string = "{}".format(front_list[i])
            my_note = genanki.Note(
            model=self.my_model,
            fields=[string, question])
            self.my_deck.add_note(my_note)
    def create_deck(self):
        genanki.Package(self.my_deck).write_to_file(self.name)
        


if __name__ == '__main__':
    model = Anki_card_model()
    start = Anki_converter('database.sqlite', 'CS 2017-2019.apkg')
    start.add_cards(GetAllQuestionsAndParts(SQLiteHandler()))
    start.create_deck()
