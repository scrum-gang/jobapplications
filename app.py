from flask import Flask, request
from sqlalchemy import create_engine

from external import apply_external, update_status_external, get_applications_external
from internal import apply_internal, update_status_internal, get_applications_internal
from utils import app


@app.route('/')
def index():
  return "<h1> Hello World! </h1>"


@app.route('/apply/external', methods=['POST'])
def apply_external():
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
  """
  content = request.json
  url, position, company = content['url'], content['position'], content['company']
  date_posted, deadline = content['date_posted'], content['deadline']
  user_id, resume = content['user_id'], content['resume']
  return apply_external(user_id, url, position, company, resume, date_posted, deadline)


@app.route('/apply/internal', methods=['POST'])
def apply_internal():
  """
  Enables user to apply to an external job posting.

  Request body:
  - `user_id`: ID of the user applying
  - `job_id`: ID of the job the user is applying to
  - `resume`: Handy tool for applying to jobs
  """
  content = request.json
  job_id = content['job_id']
  user_id, resume = content['user_id'], content['resume']
  return apply_external(user_id, job_id, resume)


@app.route('/update-status/external', methods=['POST'])
def update_status_external():
  """
  Updates the status of an external job posting

  Request body:
  - `id`: Job application ID
  - `new_status`: New status of the job application
  """
  content = request.json
  application_id = content['id']
  new_status = content['new_status']
  return update_status_external(application_id, new_status)


@app.route('/update-status/internal', methods=['POST'])
def update_status_internal():
  """
  Updates the status of an external job posting

  Request body:
  - `id`: Job application ID
  - `new_status`: New status of the job application
  """
  content = request.json
  application_id = content['id']
  new_status = content['new_status']
  return update_status_internal(application_id, new_status)


@app.route('/get/user/<user_id>')
@app.route('/get/user/<user_id>/<application_type>')
def get_application(user_id, application_type=None):
  """
  Gets job postings for a specific user.
  """
  applications_external, applications_internal = [], []
  if application_type == "external" or not application_type:
    applications_external = get_applications_external(user_id)
  if application_type == "internal" or not application_type:
    applications_internal = get_applications_internal(user_id, 'user')

  return applications_external + applications_internal


@app.route('/get/job/<job_id>')
def get_internal(job_id):
  """
  Gets all job postings to an internal job
  """
  return get_applications_internal(job_id, 'job')


if __name__ == '__main__':
  app.run()
