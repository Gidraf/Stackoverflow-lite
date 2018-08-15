"""this module it contains all the models"""
from flask import abort

class Question(object):
    """question model"""
    def __init__(self, question_list):
        """init the question receiveed"""
        self.question_list = question_list

    def show_questions(self):
        """show the questions"""
        return self.question_list

    def add_question(self, question):
        """add questions to the list"""
        self.question_list.append(question)

    def update_questions(self, index, title, description, time):
        "update a question"
        new_question = [new_question for new_question in self.question_list if new_question["id"] == index]
        if new_question:
            new_question[0]["title"] = title
            new_question[0]["description"] = description
            new_question[0]["time"] = time
            return new_question[0]

    def delete_question(self, index):
        """delete questions"""
        del_question = [del_question for del_question in self.question_list if del_question["id"] == index]
        if del_question:
            self.question_list.remove(del_question[0])
            return True
        return False


class Answer(object):
    """questions answers"""

    def  __init__(self, answer_list):
        """initialized question list"""
        self.answer_list = answer_list
