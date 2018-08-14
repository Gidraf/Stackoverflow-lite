"""this module it contains all the models"""

class Question(object):
    """question model"""
    def __init__(self, question_list):
        """init the question receiveed"""
        self.question_list = question_list

    def show_questions(self,):
        """show the questions"""
        return self.question_list

    def add_question(self, question):
        """add questions to the list"""
        self.question_list.append(question)

    def update_questions(self, index, question):
        "update a question"
        self.question_list[index] = question

    def delete_question(self, index):
        """delete questions"""
        del self.question_list[index]
