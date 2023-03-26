# handles the topics window
from PyQt5.QtWidgets import QDialog
from .Generated.TopicsWindowGenerated import Ui_TopicsDialog
from typing import List, Set
from .Util.CriteriaClass import TOPICKEYWORDS


class TopicsWindowHandler(Ui_TopicsDialog, QDialog):
    def __init__(self, currentTopics: List[str], parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.ConnectSignalSlots()
        self.topics = currentTopics if currentTopics else []
        self.finalTopics = currentTopics if currentTopics else []
        self.UpdateTopicList()

        self.show()
        self.exec()

    def ConnectSignalSlots(self):
        self.pbAddTopic.clicked.connect(self.AddTopic)
        self.pbDeleteSelectedTopic.clicked.connect(self.RemoveTopic)
        self.pbAccept.clicked.connect(self.Accept)
        self.pbCancel.clicked.connect(self.close)

    def AddTopic(self):
        """
        Adds a topic to the list
        """
        if self.cbTopicSelect.currentIndex() <= 0:
            return

        topic = self.cbTopicSelect.currentText()
        self.topics.append(topic)
        self.UpdateTopicList()

    def RemoveTopic(self):
        """
        Removes a topic from the list
        """
        if self.lwTopics.currentRow() == -1:
            return

        self.topics.pop(self.lwTopics.currentRow())
        self.UpdateTopicList()

    def UpdateTopicList(self):
        """
        Updates the list widget
        """
        self.lwTopics.clear()
        self.lwTopics.addItems(self.topics)
        self.RefreshTopicComboBox()

    def GetAllAvailableTopics(self) -> List[str]:
        """
        Gets all available topics
        """
        return list(TOPICKEYWORDS.keys())

    def RefreshTopicComboBox(self):
        """
        Refreshes the topic combobox
        """
        self.cbTopicSelect.clear()
        # get topics which are not selected
        topicsToAdd = [
            i for i in self.GetAllAvailableTopics() if i not in self.topics]
        self.cbTopicSelect.addItems(["Select a topic"] + topicsToAdd)

    def Accept(self):
        """
        Accepts the changes and stores them in self.finalTopics
        """
        self.finalTopics = self.topics
        self.close()

    def GetTopics(self):
        """
        Returns the topics
        """
        return self.finalTopics
