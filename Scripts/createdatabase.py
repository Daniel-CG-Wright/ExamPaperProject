from flask_sqlalchemy import SQLAlchemy
from flask import Flask

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///examquestions.sqlite3'


db = SQLAlchemy()
db.init_app(app)

class Paper(db.Model):
    PaperID = db.Column(db.String(40), primary_key=True, nullable=False)
    PaperComponent = db.Column(db.String(15))
    PaperYear = db.Column(db.String(4))
    PaperLevel = db.Column(db.String(10))

class Question(db.Model):
    QuestionID = db.Column(db.String(50), primary_key=True, nullable=False)
    PaperID = db.Column(db.String(40), db.ForeignKey('paper.PaperID'))
    QuestionNumber = db.Column(db.Integer)
    QuestionContents = db.Column(db.Text)

class Images(db.Model):
    ImageID = db.Column(db.Integer, primary_key=True, nullable=False)
    QuestionID = db.Column(db.String(50), db.ForeignKey('question.QuestionID'))
    ImageData = db.Column(db.LargeBinary)

class Parts(db.Model):
    PartID = db.Column(db.String(60), primary_key=True, nullable=False)
    QuestionID = db.Column(db.String(50), db.ForeignKey('question.QuestionID'))
    PartNumber = db.Column(db.String(10))
    PartContents = db.Column(db.Text)

class QuestionTopic(db.Model):
    QuestionTopicID = db.Column(db.String(150), primary_key=True)
    QuestionID = db.Column(db.String(50), db.ForeignKey('question.QuestionID'))
    TopicID = db.Column(db.String(100))


if __name__ == "__main__":
    
    db.create_all()
    app.run()