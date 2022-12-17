# KreditCart

AWS Deployment instructions: Set debug to False in project. Create AWS server. Install git. Set remote origin to this repository. Take a pull of main branch. Create a virtual environment, install all requirements. Run python manage.py collectstatic. Install Gunicorn and supervisor. Bind gunicorn socket file with wsgi file of this Django project in Supervisor configuration. Reload and restart supervisor. Install Nginx and redirect ip of server at port 80 to socket file set in Gunicorn, as well as redirect static to static directory of our project. Reload and restart nginx.
Hurray! Project will run now at given ip.
