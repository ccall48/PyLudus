
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
 - Prepare your hosts file

### Without Docker
Some additional steps are needed when not using Docker. Docker abstracts away these steps which is why using it is generally recommended.

1. **PostgreSQL setup**
	. . . 

2. **Environment variables**
	These contain various settings used by the website. 
	. . .

3. **Fusion Auth setup**
	. . . 
	
# Run the project
The project can be started with Docker or by running it directly on your system.

### Run with Docker
Start the containers using Docker Compose:
```bash
docker-compose up
```
The `-d` option can be appended to the command to run in detached mode. This runs the containers in the background so the current terminal session is available for use with other things.

### Run on the host
Running on the host is particularly useful if you wish to debug the site. The environment variables shown in a previous section need to have been configured.

**Database**
. . .

**Fusion Auth**
. . .

**Starting The Site**
. . .

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
