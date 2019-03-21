"""
Contains functionalities to track interview questions
"""
from datetime import datetime
from utils import db

from tables import InterviewQuestion

integer_id_error = {"status": "The application ID must be an integer."}
invalid_id_error = {"status": "You need to provide a valid application ID!"}
missing_question_error = {"status": "You need to provide a question!"}
missing_question_id_error = {"status": "You need to provide a question ID!"}
question_not_found_error = {"status": "No question found"}

def add_interview_question(application_id, question, title):
    if type(application_id) != int:
        return integer_id_error

    application = Application.query.filter_by(application_id=application_id).first()
    if not application_id or not application:
        return invalid_id_error

    if not question or type(question) != str:
        return missing_question_error

    question = InterviewQuestion(application_id=application_id, question=question, title=title)
    db.session.add(question)
    db.session.commit()
    questions = InterviewQuestion.query.filter_by(application_id).all()
    return [question.to_dict() for question in questions]


def get_interview_questions(application_id):
    if type(application_id) != int:
        return integer_id_error
    application = Application.query.filter_by(application_id=application_id).first()
    if not application_id or not application:
        return invalid_id_error
    questions = InterviewQuestion.query.filter_by(application_id=application_id).all()
    return [question.to_dict() for question in questions]


def update_interview_question(question_id, new_question):
    if not question_id:
        return missing_question_id_error
    interview_question = InterviewQuestion.query.filter_by(application_id).first()
    if not interview_question:
        return question_not_found_error
    interview_question.question = new_question
    return interview_question.to_dict()
