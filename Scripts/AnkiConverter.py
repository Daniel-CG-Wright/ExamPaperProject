import sqlite3
import genanki
class Anki_card_model:
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

    def add_cards(self):
        front_list = [] # put all of the questions here
        back_list = [] #put all of the question numbers and from which paper
        print(self.db_path)
        print(len(front_list))
        for i in range(0,10):
            my_note = genanki.Note(
            model=self.my_model,
            fields=[front_list[i], back_list[i]])
            self.my_deck.add_note(my_note)
    def create_deck(self):
        genanki.Package(self.my_deck).write_to_file(self.name)
        


if __name__ == '__main__':
    model = Anki_card_model()
    start = Anki_converter('database.sqlite', 'deck.apkg')
    start.add_cards()
    start.create_deck()

