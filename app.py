from flask import Flask, request
from sqlalchemy import create_engine

from external import apply_external_posting, update_status_external_posting, get_applications_external
from internal import get_applications_internal
from utils import app


@app.route('/')
def index():
  return "<h1> Hello World! </h1>"


@app.route('/apply-external', methods=['POST'])
def apply_external():
  """
  Enables user to apply to an external job posting.

  Request body:
  - `url`: URL of the external posting
  - `title`: Job title at the external posting
  - `season`: Season during which the job takes place
  - `user_id`: ID of the user applying
  """
  content = request.json
  job_url, job_title, job_season = content['url'], content['title'], content['season']
  user_id = content['user_id']
  return apply_external_posting(user_id, job_url, job_title, job_season)


@app.route('/update-status-external', methods=['POST'])
def update_status_external():
  """
  Updates the status of an external job posting

  Request body:
  - `id`: Job application ID
  - `new_status`: New status of the job application
  """
  content = request.json
  job_id = content['id']
  new_status = content['new_status']
  return update_status_external_posting(job_id, new_status)


@app.route('/get-external/<user_id>')
def get_external(user_id):
  """
  Gets external job postings for a specific user.
  """
  return get_applications_external(user_id)


@app.route('/get-internal/<job_id>')
def get_internal(job_id):
  """
  Gets all job postings to an internal job
  """
  return get_applications_internal(job_id)


if __name__ == '__main__':
  app.run()
