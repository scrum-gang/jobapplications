from flask import Flask, request, jsonify
from sqlalchemy import create_engine

from flask_cors import CORS, cross_origin

from external import apply_external, update_status_external, get_applications_external, withdraw_application_external
from internal import apply_internal, update_status_internal, get_applications_internal, withdraw_application_internal
from interview import add_interview_question, get_interview_questions, update_interview_question

from applications import get_application_by_id
from utils import app, validate_authentication

CORS(app)
auth_error = "You must be authenticated to perform this call."
missing_application_id_error = {"status": "You need to provide a job application id."}
missing_question_or_id_error = {"status": "You need to provide a question and a question_id"}
add_interview_question_error = {"status": "Something went wrong... "
                                          "Make sure you included a `application_id`, `question` and `title`."}


@app.route('/')
@cross_origin(origin='*',headers=['Content-Type'])
def index():
  return "<h1> Hello World! </h1>"


@app.route('/apply/external', methods=['POST'])
@cross_origin(origin='*',headers=['Content-Type'])
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
  - `user_id`: ID of the user applying
  - `auth`: Authentication token
  """
  content = request.json
  #if not validate_authentication(content):
  #  return jsonify({"status": auth_error})

  url, position, company = content.get("url", ""), content.get('position', ""), content.get('company', "")
  date_posted, deadline = content.get('date_posted', ""), content.get('deadline', "")
  user_id, resume, status = content.get('user_id', ""), content.get('resume', ""), content.get("status", "Applied")
  return jsonify(apply_external(user_id, url, position, company, resume,
                                date_posted, deadline, status=status))


@app.route('/apply/internal', methods=['POST'])
@cross_origin(origin='*',headers=['Content-Type'])
def apply_internal_endpoint():
  """
  Enables user to apply to an external job posting.

  Request body:
  - `user_id`: ID of the user applying
  - `job_id`: ID of the job the user is applying to
  - `resume`: Handy tool for applying to jobs
  - `auth`: Authentication token
  """
  #if not validate_authentication(content):
  #  return jsonify({"status": auth_error})
  content = request.json
  job_id = content['job_id']
  user_id, resume = content['user_id'], content['resume']
  return jsonify(apply_internal(user_id, job_id, resume))


@app.route('/interview/question', methods=['POST'])
def add_interview_question_endpoint():
  """
  Enables user to track interview questions

  Request body:
  - `application_id`: ID of the application to which the question maps to
  - `question`: Interview question
  - `auth`: Authentication token
  """
  content = request.json
  if not validate_authentication(content):
    return jsonify({"status": auth_error})
  try:
    application_id = content['application_id']
    question = content['question']
    title = content['title']
  except Exception as e:
    print(e)
    return jsonify(add_interview_question_error)
  return jsonify(add_interview_question(application_id, question, title))


@app.route('/update-status/external', methods=['PUT'])
@cross_origin(origin='*',headers=['Content-Type'])
def update_status_external_endpoint():
  """
  Updates the status of an external job posting

  Request body:
  - `id`: Job application ID
  - `new_status`: New status of the job application
  - `auth`: Authentication token
  """
  #if not validate_authentication(content):
  #  return jsonify({"status": auth_error})

  content = request.json
  application_id = content['id']
  new_status = content['new_status']
  return jsonify(update_status_external(application_id, new_status))


@app.route('/update-status/internal', methods=['PUT'])
@cross_origin(origin='*',headers=['Content-Type'])
def update_status_internal_endpoint():
  """
  Updates the status of an external job posting

  Request body:
  - `id`: Job application ID
  - `new_status`: New status of the job application
  - `auth`: Authentication token
  """
  #if not validate_authentication(content, admin=True):
  #  return jsonify({"status": auth_error})

  content = request.json
  application_id = content['id']
  new_status = content['new_status']
  return jsonify(update_status_internal(application_id, new_status))


@app.route('/update/question', methods=['PUT'])
@cross_origin(origin='*', headers=['Content-Type'])
def update_interview_questions_endpoint():
  """
  Updates an interview question

  Request body:
  - `id`: Question ID
  - `new_question`: New question for that interview
  - `auth`: Authentication token
  """
  content = request.json
  if 'question' not in content or 'id' not in content:
    return jsonify(missing_question_or_id_error)
  return jsonify(update_interview_question(content['id'], content['question']))


@app.route('/applications/user/<user_id>')
@app.route('/applications/user/<user_id>/<application_type>')
@cross_origin(origin='*',headers=['Content-Type'])
def get_application_by_user_endpoint(user_id, application_type=None):
  """
  Gets job postings for a specific user.
  - `auth`: Authentication token
  """
  #if not validate_authentication(content, user=user_id):
  #  return jsonify({"status": auth_error})

  applications_external, applications_internal = [], []
  if application_type == "external" or not application_type:
    applications_external = get_applications_external(user_id)
  if application_type == "internal" or not application_type:
    applications_internal = get_applications_internal(user_id, 'user')
  return jsonify(applications_external + applications_internal)


@app.route('/applications/job/<job_id>')
@cross_origin(origin='*',headers=['Content-Type'])
def get_application_by_job_endpoint(job_id):
  """
  Gets all job postings to an internal job
  """
  #if not validate_authentication(content, admin=True):
  #  return jsonify({"status": auth_error})

  return jsonify(get_applications_internal(job_id, 'job'))


@app.route('/applications/<application_id>')
@cross_origin(origin='*',headers=['Content-Type'])
def get_application(application_id):
  """
  Gets a single application by its unique ID
  """
  #if not validate_authentication(content, admin=True):
  #  return jsonify({"status": auth_error})

  return jsonify(get_application_by_id(application_id))


@app.route('/withdraw/internal', methods=['DELETE'])
@cross_origin(origin='*',headers=['Content-Type'])
def withdraw_internal_application_endpoint():
  """
  Withdraws an application to an internal posting

  Request body:
  - `id`: Job application ID
  - `auth`: Authentication token
  """
  #if not validate_authentication(content, admin=True):
  #  return jsonify({"status": auth_error})

  content = request.json
  if 'id' not in content:
    return jsonify(missing_application_id_error)

  application_id = content['id']
  return jsonify(withdraw_application_internal(application_id))


@app.route('/withdraw/external', methods=['DELETE'])
@cross_origin(origin='*',headers=['Content-Type'])
def withdraw_external_application_endpoint():
  """
  Withdraws an application to an external posting

  Request body:
  - `id`: Job application ID
  - `auth`: Authentication token
  """
  #if not validate_authentication(content, admin=True):
  #  return jsonify({"status": auth_error})

  content = request.json
  if 'id' not in content:
    return jsonify(missing_application_id_error)

  application_id = content['id']
  return jsonify(withdraw_application_external(application_id))


@app.route('/interview/question/<application_id>')
@cross_origin(origin='*', headers=['Content-Type'])
def get_interview_questions_endpoint(application_id):
  """
  Gets all interview questions

  Request body:
  - `auth`: Authentication token
  """
  content = request.json
  return jsonify(get_interview_questions(application_id))


if __name__ == '__main__':
  app.run()
