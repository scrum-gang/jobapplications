from flask import Flask, request, jsonify
from sqlalchemy import create_engine
from flask_cors import CORS
from external import apply_external, update_status_external, get_applications_external
from internal import apply_internal, update_status_internal, get_applications_internal
from applications import get_application_by_id
from utils import app, validate_authentication

CORS(app)
auth_error = "You must be authenticated to perform this call."

@app.route('/')
def index():
  return "<h1> Hello World! </h1>"


@app.route('/apply/external', methods=['POST'])
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
  if not validate_authentication(content):
    return jsonify({"status": auth_error})

  url, position, company = content.get("url", ""), content.get('position', ""), content.get('company', "")
  date_posted, deadline = content.get('date_posted', ""), content.get('deadline', "")
  user_id, resume, status = content['user_id'], content.get('resume', ""), content.get("status", "Applied")
  return jsonify(apply_external(user_id, url, position, company, resume,
                                date_posted, deadline, status=status))


@app.route('/apply/internal', methods=['POST'])
def apply_internal_endpoint():
  """
  Enables user to apply to an external job posting.

  Request body:
  - `user_id`: ID of the user applying
  - `job_id`: ID of the job the user is applying to
  - `resume`: Handy tool for applying to jobs
  - `auth`: Authentication token
  """
  if not validate_authentication(content):
    return jsonify({"status": auth_error})
  content = request.json
  job_id = content['job_id']
  user_id, resume = content['user_id'], content['resume']
  return jsonify(apply_internal(user_id, job_id, resume))


@app.route('/update-status/external', methods=['POST'])
def update_status_external_endpoint():
  """
  Updates the status of an external job posting

  Request body:
  - `id`: Job application ID
  - `new_status`: New status of the job application
  - `auth`: Authentication token
  """
  if not validate_authentication(content):
    return jsonify({"status": auth_error})

  content = request.json
  application_id = content['id']
  new_status = content['new_status']
  return jsonify(update_status_external(application_id, new_status))


@app.route('/update-status/internal', methods=['POST'])
def update_status_internal_endpoint():
  """
  Updates the status of an external job posting

  Request body:
  - `id`: Job application ID
  - `new_status`: New status of the job application
  - `auth`: Authentication token
  """
  if not validate_authentication(content, admin=True):
    return jsonify({"status": auth_error})

  content = request.json
  application_id = content['id']
  new_status = content['new_status']
  return jsonify(update_status_internal(application_id, new_status))


@app.route('/applications/user/<user_id>')
@app.route('/applications/user/<user_id>/<application_type>')
def get_application_by_user_endpoint(user_id, application_type=None):
  """
  Gets job postings for a specific user.
  - `auth`: Authentication token
  """
  if not validate_authentication(content, user=user_id):
    return jsonify({"status": auth_error})

  applications_external, applications_internal = [], []
  if application_type == "external" or not application_type:
    applications_external = get_applications_external(user_id)
  if application_type == "internal" or not application_type:
    applications_internal = get_applications_internal(user_id, 'user')
  return jsonify(applications_external + applications_internal)


@app.route('/applications/job/<job_id>')
def get_application_by_job_endpoint(job_id):
  """
  Gets all job postings to an internal job
  """
  if not validate_authentication(content, admin=True):
    return jsonify({"status": auth_error})

  return jsonify(get_applications_internal(job_id, 'job'))


@app.route('/applications/<application_id>')
def get_application(application_id):
  """
  Gets a single application by its unique ID
  """
  if not validate_authentication(content, admin=True):
    return jsonify({"status": auth_error})

  return jsonify(get_application_by_id(application_id))


if __name__ == '__main__':
  app.run()
