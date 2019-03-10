"""
Contains functionalities to track interview questions
"""
from datetime import datetime
from utils import db

from tables import InterviewQuestion


def add_interview_question(application_id, question):
    if type(application_id) != int:
        return {"status": "The application must be an integer."}

    application = Application.query.filter_by(application_id=application_id).first()
    if not application_id or not application:
        return {"status": "You need to provide a valid application ID!"}

    if not question or type(question) != str:
        return {"status": "You need to provide a question!"}

    question = InterviewQuestion(application_id=application_id, question=question)
    db.session.add(question)
    db.session.commit()
    questions = InterviewQuestion.query.filter_by(application_id).all()
    return [question.to_dict() for question in questions]
