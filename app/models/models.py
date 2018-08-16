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


class Answer(object):
    """questions answers"""

    def  __init__(self, answer_list):
        """initialized question list"""
        self.answer_list = answer_list

    def show_answers(self, question_id):
        '''show question answers'''
        answers = [answers for answers in self.answer_list if answers["question_id"] == question_id]
        if answers:
            return answers

    def add_answer(self, answer):
        '''and answer to the list'''
        self.answer_list.append(answer);
        return answer

    def update_answer(self, answer_id, answer_text):
        '''update an existing answer'''
        answer=[answer for answer in self.answer_list if answer["id"] == answer_id]
        if answer:
            answer[0]["answer_text"]=answer_text
            return answer[0]

    def delete_answer(self, id):
        """delete answer"""
        answer= [answer for answer in self.answer_list if answer["id"] == id]
        if answer:
            self.answer_list.remove(answer[0])
            return True
