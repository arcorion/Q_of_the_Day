import json
import random
import shutil

from os.path import exists
from typing import Generic, NamedTuple, TypeVar

Q = TypeVar('Q')

class QuestionList(Generic[Q]):
    """
    QuestionList represent a QOTD Bot's question storehouse.
    It takes requests from the Q Bot and passes back results, as needed.
    It also stores previously asked question and questions to be asked.
    """
    class Question(NamedTuple):
        ask_url: str    # URL of where the question was last asked - IMPLEMENT
        author: str     # Name of the author
        url: str        # URL of where the author's message - IMPLEMENT
        text: str       # URL of the question's text


    def __init__(self, name: str):
        """
        Creating QuestionList object.
        name - name of the QuestionList instance and
        the associated json file name.
        """
        self.name = name
        self.questions = dict()
        self.current_id = 0

        file_name = name + ".json"
        if (exists(file_name)):
            with open(file_name, 'r') as file:
                self.questions = json.load(file)
        
        if self.questions:
            self.current_id = list(self.questions)[-1]



    def make_question(self, author: str, text: str) -> Q:
        """
        Creates a question object.
        author - Represents the author of the question
        proposal id - Represents the original post 
        """
        return self.Question(author=author, text=text, url=None, ask_url=None)

    def add(self, question: Question):
        """
        Adds a question to the QuestionList.
        question - An object containing the question.  Use make_question() to create this.
        """
        self.current_id = self.current_id + 1
        self.questions.update({self.current_id: question})

    def get(self, is_random=False) -> Q:
        """
        Returns a question. If no question is available, returns None.
        is_random (False default) - If true, asks random question from list.
        If false, asks the next one in the list.
        """
        question = None

        if self.questions:
            if is_random:
                key = random.choice(list(self.questions))
                question = self.questions.pop(key)
            else:
                question = list(self.questions)[0]

        return question

    def list(self) -> str:
        """
        Returns a string formatted list of the questions in this QuestionList.
        """
        formatted_list = f""
        for key in self.questions:
            question = self.questions[key]
            formatted_list += f"{question.author} wrote: " + \
            f"\"{question.text}\" at {question.url}\n" + \
            f"It was last asked at: {question.ask_url}\n"

        return formatted_list

    def move(self, question_id: int, other: Q):
        """
        Moves a question to another QuestionList
        question_id - ID number of question to be moved
        other - Other QuestionList to be moved to.
        """
        this_question = self.remove(question_id)
        other.add(this_question)

    def remove(self, question_id: int):
        """
        Removes a question from the QuestionList.
        question_id - ID number of question to be removed
        """
        if question_id not in self.questions:
            return ValueError(f"ID number not in {self.name}")

        return self.questions.pop(question_id)

    def save_list(self):
        """
        Saves a copy of the QuestionList to a file.
        Note, backs up one copy of the file as '<file_name>.bak'
        if one with the same name already exists.
        """
        file_name = self.name + ".json"
        backup_name = file_name + ".bak"
        if exists(file_name):
            shutil.move(file_name, backup_name)

        with open(file_name, 'w') as file:
            json.dump(self.questions, file)
