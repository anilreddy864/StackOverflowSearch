# StackOverflowSearch

StackOverFlow Search is implemented using StackOverFlow Advanced search API to fetch questions. This is Django Project. 

Below requirements are fulfilled in this project.

Requirement:
1) Able to search all available fields/parameters. 
2) List the result with pagination with Django template.
3) Page/Data should be cached. (Application should only call StackOverflowAPI if we didn't pull data already for same query param)
4) Add Search limit per min(5) and per day(100) for each session.

Used Local Memory Cache for Caching.
Used ratelimit lib for Search rate limiting. 
Used Bootstrap4 for Django web Template design..

How to test the project?
1. Download the Repo.
2. Install the required libraries. "pip install req_lib.txt"
3. run "python manage.py runserver" from the project folder. 
4. View the output on "http://127.0.0.1:8000/
