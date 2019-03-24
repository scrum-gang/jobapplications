from flask import Flask, request, jsonify
from sqlalchemy import create_engine

from flask_cors import CORS, cross_origin

from applications import get_application_by_id, update_comment, update_status, withdraw_application
from external import apply_external, get_applications_external
from internal import apply_internal, get_applications_internal
from interview import add_interview_question, get_interview_questions, update_interview_question

from tables import Application
from utils import app, validate_authentication, query_auth

CORS(app)
auth_error = "You must be authenticated to perform this call."
auth_error_admin = "You must be authenticated as a Recruiter to perform this call."
missing_application_id_error = {"status": "You need to provide a job application id."}
application_not_found_error = {"status" : "Application not found!"}
missing_question_or_id_error = {"status": "You need to provide a question and a question_id"}
add_interview_question_error = {"status": "Something went wrong... "
                                          "Make sure you included a `application_id`, `question` and `title`."}


@app.route('/')
@cross_origin(origin='*',headers=['Content-Type'])
def index():
  return "<h1> Hello World! </h1>"


@app.route('/apply/external', methods=['POST'])
@cross_origin(origin='*',headers=['Authorization', 'Content-Type'])
def apply_external_endpoint():
  """
  Enables user to apply to an external job posting.

  Request body:
  - `url`: URL of the external posting
  - `position`: Job position of the external posting
  - `company`: Company where job takes place
  - `resume`: Handy tool for applying to jobs
  - `date_posted`: When the application was posted
  - `deadline`: Deadline to apply for the job
  """
  content = request.json
  headers = request.headers

  if not validate_authentication(headers):
    return jsonify({"status": auth_error})

  url, position, company = content.get("url", ""), content.get('position', ""), content.get('company', "")
  date_posted, deadline = content.get('date_posted', ""), content.get('deadline', "")
  resume, status, comment = content.get('resume', ""), content.get("status", "Applied"), content.get('comment', '')
  user_id = query_auth(headers['Authorization'])['_id']
  return jsonify(apply_external(user_id, url, position, company, resume,
                                date_posted, deadline, comment, status=status))


@app.route('/apply/internal', methods=['POST'])
@cross_origin(origin='*',headers=['Authorization', 'Content-Type'])
def apply_internal_endpoint():
  """
  Enables user to apply to an external job posting.

  Request body:
  - `job_id`: ID of the job the user is applying to
  - `resume`: Handy tool for applying to jobs
  """
  content = request.json
  headers = request.headers

  if not validate_authentication(headers):
    return jsonify({"status": auth_error})

  user_id = query_auth(headers['Authorization'])['_id']
  job_id = content.get('job_id', '')
  resume = content.get('resume', '')
  comment = content.get('comment', '')
  return jsonify(apply_internal(user_id, job_id, resume, comment))


@app.route('/interview/question', methods=['POST'])
@cross_origin(origin='*',headers=['Authorization', 'Content-Type'])
def add_interview_question_endpoint():
  """
  Enables user to track interview questions

  Request body:
  - `application_id`: ID of the application to which the question maps to
  - `question`: Interview question
  """
  content = request.json
  headers = request.headers

  if not validate_authentication(headers):
    return jsonify({"status": auth_error})

  user_id = query_auth(headers['Authorization'])['_id']
  try:
    application_id = content['application_id']
    question = content['question']
    title = content['title']
  except Exception as e:
    print(e)
    return jsonify(add_interview_question_error)
  return jsonify(add_interview_question(application_id, question, title, user_id))


@app.route('/update/status', methods=['PUT'])
@cross_origin(origin='*',headers=['Authorization', 'Content-Type'])
def update_status_internal_endpoint():
  """
  Updates the status of a job application

  Request body:
  - `id`: Job application ID
  - `new_status`: New status of the job application
  """
  content = request.json
  headers = request.headers

  application_id = content.get('id', '')
  if not application_id:
    return jsonify(missing_application_id_error)

  application = Application.query.filter_by(id=application_id).first()
  if not application:
    return jsonify(application_not_found_error)

  if not validate_authentication(headers):
    return jsonify({"status": auth_error_admin})

  user_id = query_auth(headers['Authorization'])['_id']
  new_status = content.get('new_status', '')
  return jsonify(update_status(application_id, new_status, user_id))


@app.route('/update/comment', methods=['PUT'])
@cross_origin(origin='*',headers=['Authorization', 'Content-Type'])
def update_comment_endpoint():
  """
  Updates the comment of a job application

  Request body:
  - `id`: Job application ID
  - `new_comment`: New comment for the application
  """
  content = request.json
  headers = request.headers

  if not validate_authentication(headers):
    return jsonify({"status": auth_error_admin})

  user_id = query_auth(headers['Authorization'])['_id']
  application_id = content.get('id', '')
  new_comment = content.get('new_comment', '')
  return jsonify(update_comment(application_id, new_comment, user_id))


@app.route('/update/question', methods=['PUT'])
@cross_origin(origin='*',headers=['Authorization', 'Content-Type'])
def update_interview_questions_endpoint():
  """
  Updates an interview question

  Request body:
  - `id`: Question ID
  - `new_question`: New question for that interview
  """
  content = request.json
  headers = request.headers

  if not validate_authentication(headers):
    return jsonify({"status": auth_error})

  if 'new_question' not in content or 'id' not in content:
    return jsonify(missing_question_or_id_error)
  return jsonify(update_interview_question(content['id'], content['new_question']))


@app.route('/applications/user/')
@app.route('/applications/user/<application_type>')
@cross_origin(origin='*',headers=['Authorization', 'Content-Type'])
def get_application_by_user_endpoint(application_type=None):
  """
  Gets job postings for a specific user.
  """
  headers = request.headers

  if not validate_authentication(headers):
    return jsonify({"status": auth_error})

  user_id = query_auth(headers['Authorization'])['_id']

  applications_external, applications_internal = [], []
  if application_type == "external" or not application_type:
    applications_external = get_applications_external(user_id)
  if application_type == "internal" or not application_type:
    applications_internal = get_applications_internal(user_id, 'user')
  return jsonify(applications_external + applications_internal)


@app.route('/applications/job/<job_id>')
@cross_origin(origin='*',headers=['Authorization', 'Content-Type'])
def get_application_by_job_endpoint(job_id):
  """
  Gets all job postings to an internal job
  """
  headers = request.headers

  if not validate_authentication(headers, admin=True):
    return jsonify({"status": auth_error_admin})

  return jsonify(get_applications_internal(job_id, 'job'))


@app.route('/applications/<application_id>')
@cross_origin(origin='*',headers=['Authorization', 'Content-Type'])
def get_application(application_id):
  """
  Gets a single application by its unique ID
  """
  headers = request.headers

  if not validate_authentication(headers):
    return jsonify({"status": auth_error})

  user_id = query_auth(headers['Authorization'])['_id']
  return jsonify(get_application_by_id(application_id, user_id))


@app.route('/interview/question/<int:application_id>')
@cross_origin(origin='*',headers=['Authorization', 'Content-Type'])
def get_interview_questions_endpoint(application_id):
  """
  Gets all interview questions
  """
  headers = request.headers

  if not validate_authentication(headers):
    return jsonify({"status": auth_error})

  user_id = query_auth(headers['Authorization'])['_id']
  return jsonify(get_interview_questions(application_id, user_id))


@app.route('/withdraw', methods=['DELETE'])
@cross_origin(origin='*',headers=['Authorization', 'Content-Type'])
def withdraw_internal_application_endpoint():
  """
  Withdraws an application to a given job posting

  Request body:
  - `id`: Job application ID
  """
  content = request.json
  headers = request.headers

  if not validate_authentication(headers):
    return jsonify({"status": auth_error})

  if 'id' not in content:
    return jsonify(missing_application_id_error)

  application_id = content['id']
  user_id = query_auth(headers['Authorization'])['_id']

  return jsonify(withdraw_application(application_id, user_id))


if __name__ == '__main__':
  app.run()
