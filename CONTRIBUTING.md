
# Setup Instructions

1. [Install requirements](#Requirements)
2. [Fork the project repository](#Fork-the-Project)
4. [Configure the development environment](#Development-Environment)
5. [Run the project](#Run-The-Project)
6. [Work with git to make changes](#Working-with-Git)

# Requirements

- [Python 3.8](https://docs.python.org/3.8/)
- [Fusion Auth]()
- [Git](https://git-scm.com/doc)
- [Docker](https://docs.docker.com/compose/install/)
    - `pip install docker-compose`
- [Django]()

# Fork the project
You will need access to a copy of the git repository of your own that will allow you to edit the code and push your commits to. Creating a copy of a repository under your own account is called a **fork**.

This is where all your changes and commits will be pushed to, and from where your PRs will originate from.

For any Collaborators, since you have write permissions already to the original repository, you can just create a feature branch to push your commits to instead.

# Development environment

 - Clone your fork to a local project directory 
 - Install the project's dependencies 
 - **Configuring Environment variables**

	These contain various settings used by the website.
	You need to make the following changes to the [`.env.sample`](https://github.com/AAADevs/PyLudus/blob/main/.env.sample).
	```bash
	# FUSION AUTH
	POSTGRES_USER=postgres
	POSTGRES_PASSWORD=<replace me> # create a random bunch of characters, and do not share this

	# Prior to version 1.19.0, using DATABASE_USER
	DATABASE_USER=fusionauth

	# >= 1.19.0, using DATABASE_USERNAME
	DATABASE_USERNAME=fusionauth
	DATABASE_PASSWORD=<replace me> # create a random bunch of characters, and do not share this
	ES_JAVA_OPTS=-Xms512m -Xmx512m

	# Prior to version 1.19.0, using FUSIONAUTH_MEMORY
	FUSIONAUTH_MEMORY=512M

	# >= 1.19.0, using FUSIONAUTH_APP_MEMORY
	FUSIONAUTH_APP_MEMORY=512M
	FUSIONAUTH_APP_PROTOCOL='http'
	FUSIONAUTH_APP_HOST='192.168.1.141' # replace with your local machine IP address (`hostname -I`)
	FUSIONAUTH_APP_PORT='9011'

	# ----------------------------------------------------------------------------------------------

	# DJANGO
	SECRET_KEY='<replace me>' # create a random bunch of characters, and do not share this

	# For dev and testing
	DEBUG=true
	# For production
	# DEBUG = false

	# can be a list seperated by commas
	ALLOWED_HOSTS='192.168.1.141,127.0.0.1' # replace with your local machine IP address, followed with your localhost IP 

	# Fusion specific variables
	# NOTE: SECURE_SSL_REDIRECT is not used currently
	# SECURE_SSL_REDIRECT=true
	
	DJANGO_PROTOCOL='http'
	DJANGO_HOST='192.168.1.141' # replace with your local machine IP address
	DJANGO_PORT='8000'

	# get from fusion after app creation
	FUSION_AUTH_APP_ID='<replace me>'
	# get from fusion after app creation
	FUSION_AUTH_CLIENT_SECRET='<replace me>'
	# get from fusion in the settings -> api keys
	FUSION_AUTH_API_KEY='<replace me>'

	# internal hostname for fusion, for now we don't need to go out the container network to do API auth
	FUSION_AUTH_INTERNAL_API_PROTOCOL='http'
	FUSION_AUTH_INTERNAL_API_HOST='fusionauth'
	FUSION_AUTH_INTERNAL_API_PORT='9011'
	```
	
# Run the project
The project can be started with Docker as of now.

### Run with Docker
Start the containers using Docker Compose:
```bash
./start.sh # Runs docker-compose -d

# Init the database and running initial migrations
docker exec -it pyludus_web_1 /bin/bash
python manage.py makemigrations
python manage.py migrate
exit # Exit out of the docker shell

# Restart the docker images
docker-compose down; sleep 2; docker-compose up -d
```
The `-d` option can be appended to the command to run in detached mode. This runs the containers in the background so the current terminal session is available for use with other things.

# Django admin site
Django provides an interface for administration with which you can view and edit the models among other things. It can be found at  http://<local_host_url_here>. The default credentials are `admin` for the username and `admin` for the password.


# Working on the project
The development environment will watch for code changes in your project directory and will restart the server when a module has been edited automatically. Unless you are editing the Dockerfile or docker-compose.yml, you shouldn't need to manually restart the container during a developing session.

Click [here](https://rogerdudler.github.io/git-guide/) to see the basic Git workflow when contributing to Pyludus.

# Rules

1. You must be a member of [our Discord community](https://discord.gg/gZzpQkF6rx) in order to contribute to this project.

2. Your pull request must solve an issue created or approved by a collaborator. Feel free to suggest issues of your own, which collaborators can review for approval.

3. If you have direct access to the repository, **create a branch for your changes** and create a pull request for that branch. If not, create a branch on a fork of the repository and create a pull request from there.
    * If PR*ing* from your own fork, **ensure that "Allow edits from maintainers" is checked**. This gives permission for maintainers to commit changes directly to your fork, speeding up the review process.

4. **Adhere to the prevailing code style**, which we enforce using [`flake8`](http://flake8.pycqa.org/en/latest/index.html) and [`pre-commit`](https://pre-commit.com/).
    * Run `flake8` and `pre-commit` against your code **before** you push. Your commit will be rejected by the build server if it fails to lint. You can run the lint by executing `pipenv run lint` in your command line.

5. **Make great commits**. A well structured git log is key to a project's maintainability; it efficiently provides insight into when and *why* things were done for future maintainers of the project.
    * A more in-depth guide to writing great commit messages can be found in Chris Beam's [*How to Write a Git Commit Message*](https://chris.beams.io/posts/git-commit/).

6. If someone is working on an issue or pull request, **do not open your own pull request for the same task**. Instead, collaborate with the author(s) of the existing pull request. Duplicate PRs opened without communicating with the other author(s) or collaborators, will be closed. 
    * One option is to fork the other contributor's repository and submit your changes to their branch with your own pull request. We suggest following these guidelines when interacting with their repository as well.
