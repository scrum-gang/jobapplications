Database design for Job Applications

# Tables

* Applications
* Inhouse
* External
* InterviewQuestion

# Columns

## Applications
* `id` : integer, primary key, unique, mandatory
* `date` : date, mandatory
* `user_id`: string, mandatory, comes from auth microservice
* `is_inhouse_posting` : Boolean, true if it's an inhouse posting false if not
* `status` : String, tracks the status of a given application. Can be modified by user for external postings but not 
* `resume`: String, handy tool for applying to jobs
* `comment`: String, Optional comment a user might add to his application

for inhouse postings.
* `resume`: String

## Inhouse
* `id` : Integer, primary key
* `application_id` : Integer, foreign key from `Applications`
* `job_id` : String, mandatory, comes from inhouse postings microservice

## External
* `id`: Integer, primary key
* `application_id` : Integer, foreign key from `Applications`
* `url`: String, mandatory
* `position`: String
* `company`: String
* `date_posted`: String, but it's just a stringified datetime object
* `deadline`: String, but it's just a stringified datetime object

## InterviewQuestion
* `id`: Integer, primary key
* `application_id`: Integer, foreign key from `Applications`
* `title`: String, title of the interview question
* `question`: String, specific interview question
