
# Software Engineering — Individual Assignment 1

[![Build Status](https://app.travis-ci.com/ShaliniGupta14/Software-Engineering_Individual_Assignment_1.svg?branch=main)](https://app.travis-ci.com/github/ShaliniGupta14/Software-Engineering_Individual_Assignment_1)
[![Coverage Status](https://coveralls.io/repos/github/ShaliniGupta14/Software-Engineering_Individual_Assignment_1/badge.svg?branch=main)](https://coveralls.io/github/ShaliniGupta14/Software-Engineering_Individual_Assignment_1?branch=main)

**New York University — Tandon School of Engineering**  
**Course:** Software Engineering  
**Student:** Shalini Gupta

## Project Overview

This project implements the Django Polls application and configures a complete Continuous Integration and Continuous Deployment (CI/CD) pipeline using GitHub, Travis CI, Coveralls, and AWS Elastic Beanstalk.

The application allows users to view poll questions, select an answer, submit a vote, and view voting results.

Every push to the `main` branch automatically triggers Travis CI to validate code quality, execute the Django test suite, generate a coverage report, and deploy the application to AWS Elastic Beanstalk if all checks pass.

## Project Links

| Resource | Link |
|---|---|
| GitHub Repository | [Source Code](https://github.com/ShaliniGupta14/Software-Engineering_Individual_Assignment_1) |
| Travis CI Dashboard | [Build History](https://app.travis-ci.com/github/ShaliniGupta14/Software-Engineering_Individual_Assignment_1) |
| Coveralls | [Coverage Report](https://coveralls.io/github/ShaliniGupta14/Software-Engineering_Individual_Assignment_1?branch=main) |
| Deployed Application | [Django Polls](http://individualassignment1-env.eba-ttrk3qeu.us-east-2.elasticbeanstalk.com/polls/) |

## Technology Stack

| Component | Technology |
|---|---|
| Language | Python 3.13 |
| Web Framework | Django |
| Database | SQLite |
| Source Control | Git and GitHub |
| Continuous Integration | Travis CI |
| Code Formatting | Black |
| Static Code Analysis | Flake8 |
| Automated Testing | Django TestCase |
| Code Coverage | Coverage.py |
| Coverage Reporting | Coveralls |
| Cloud Deployment | AWS Elastic Beanstalk |
| Deployment Automation | AWS CLI and Bash |
| Cloud Platform | Amazon Linux 2023 |

## Django Polls Application

The application contains two primary models:

- **Question:** Stores the poll question and publication date.
- **Choice:** Stores an answer option, its associated question, and vote count.

### Features

- Display the five most recently published poll questions.
- View individual poll questions and their choices.
- Submit votes for a selected choice.
- Display voting results.
- Handle invalid questions and missing or invalid vote selections.
- Manage questions and choices through Django Admin.

### Application Routes

| Route | Description |
|---|---|
| `/polls/` | List poll questions |
| `/polls/<id>/` | Display a question and its choices |
| `/polls/<id>/vote/` | Submit a vote |
| `/polls/<id>/results/` | Display voting results |
| `/admin/` | Django administration |

The deployed database may initially contain no questions, in which case `/polls/` displays **"No polls are available."**

## Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/ShaliniGupta14/Software-Engineering_Individual_Assignment_1.git
cd Software-Engineering_Individual_Assignment_1
```

### 2. Create and activate a virtual environment

```bash
python3.13 -m venv assignment_1
source assignment_1/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements-dev.txt
```

### 4. Configure Django environment variables

For local development, set the required Django configuration values:

```bash
export DJANGO_SECRET_KEY="your-local-development-secret"
export DJANGO_DEBUG="True"
export DJANGO_ALLOWED_HOSTS="localhost,127.0.0.1"
```

Do not commit production secrets or AWS credentials to GitHub.

### 5. Apply database migrations

```bash
python manage.py migrate
```

### 6. Start the development server

```bash
python manage.py runserver
```

Open:

http://127.0.0.1:8000/polls/

## Continuous Integration — Travis CI

Travis CI is configured using `.travis.yml`.

The pipeline performs the following steps:

1. Installs Python 3.13 and project dependencies.
2. Runs Django system checks.
3. Checks Python formatting using Black.
4. Checks code quality using Flake8.
5. Runs the Django unit test suite with Coverage.py.
6. Generates a code coverage report.
7. Uploads coverage information to Coveralls.
8. Deploys the application to AWS Elastic Beanstalk on successful builds of `main`.

### Black Formatting

Check formatting without modifying files:

```bash
black --check . --exclude '/(\.git|assignment_1|migrations)/'
```

Format the tests:

```bash
black polls/tests.py
```

### Flake8 Linting

```bash
flake8 .
```

The `.flake8` configuration is used to maintain compatibility with Black's formatting conventions.

### Automated Tests

Run the Django test suite:

```bash
python manage.py test polls
```

The project includes **16 automated tests** covering:

- Question model string representation.
- Recent, old, and future publication dates.
- Choice model representation, relationships, and default votes.
- Poll index, detail, and results views.
- Display of the latest five questions.
- Successful voting and vote count updates.
- Missing or invalid choice submissions.
- Invalid question handling.

### Code Coverage

Run the tests with Coverage.py:

```bash
coverage run --source=mysite,polls manage.py test
coverage report
```

Upload coverage results to Coveralls:

```bash
coveralls
```

### Verified CI Results

Travis CI Build #10 completed successfully on October 28, 2026.

| Metric | Result |
|---|---|
| Django Unit Tests | 16 passed |
| Black | Passed |
| Flake8 | Passed |
| Overall Code Coverage | 95% |
| Coveralls Upload | Completed |
| AWS Deployment | Successful |

Coverage results can change as the codebase evolves.

## Continuous Deployment — AWS Elastic Beanstalk

The Django application is deployed to AWS Elastic Beanstalk.

### Deployment Configuration

| Setting | Value |
|---|---|
| AWS Region | us-east-2 (Ohio) |
| Elastic Beanstalk Application | Individual_Assignment_1 |
| Environment | IndividualAssignment1-env |
| Platform | Python 3.13 on Amazon Linux 2023 |
| Environment Type | Single instance |
| WSGI Application | mysite.wsgi:application |

### Automated Deployment Workflow

A successful Travis CI build on `main` executes:

```bash
bash scripts/deploy_aws.sh
```

The deployment script:

1. Creates a ZIP archive of the Git commit.
2. Uploads the archive to the Elastic Beanstalk S3 bucket.
3. Checks whether the application version already exists.
4. Creates a new application version if necessary.
5. Requests an Elastic Beanstalk environment update.
6. Waits for the environment update to finish.
7. Verifies that the expected application version is running.

Deployment is marked successful only after the deployed version is verified.

The deployment also includes a platform post-deployment hook:

```text
.platform/hooks/postdeploy/01_migrate.sh
```

This runs Django database migrations during deployment.

### Deployment Security

- AWS credentials are configured as protected environment variables in Travis CI.
- AWS credentials are not stored in the repository.
- Deployment uses a dedicated IAM user with a custom policy.
- Production Django settings are supplied through environment configuration.
- Sensitive application values are kept outside source control.

### Live Application

[Django Polls — AWS Elastic Beanstalk](http://individualassignment1-env.eba-ttrk3qeu.us-east-2.elasticbeanstalk.com/polls/)

## GitHub Branch Protection

The repository uses a branch protection rule for `main`, configured to require the **Travis CI - Branch** status check before merging.

This helps prevent changes from being merged without successful CI validation.

Travis CI is configured to build repository changes and validate code quality. Automatic deployment is restricted to the `main` branch.

## Project Structure

```text
Individual_Assignment_1/
├── .ebextensions/
│   └── django.config
├── .platform/
│   └── hooks/
│       └── postdeploy/
│           └── 01_migrate.sh
├── mysite/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── polls/
│   ├── migrations/
│   ├── templates/
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── scripts/
│   └── deploy_aws.sh
├── .flake8
├── .gitignore
├── .travis.yml
├── manage.py
├── requirements.txt
├── requirements-dev.txt
└── README.md
```

## Assignment Requirements

| Requirement | Implementation |
|---|---|
| GitHub repository | Completed |
| Travis CI configuration | Completed |
| Automated CI on push | Verified |
| Black formatting checks | Verified |
| Flake8 linting checks | Verified |
| Django test suite | 16 passing tests |
| Coverage.py integration | Completed |
| Coveralls reporting | Completed |
| Travis and Coveralls README badges | Included |
| Automated AWS Elastic Beanstalk deployment | Verified |
| Branch protection and required CI status | Configured |

## Conclusion

This assignment demonstrates a working CI/CD pipeline for a Django web application. GitHub manages the source code, Travis CI automatically validates changes, Coverage.py and Coveralls report test coverage, and AWS Elastic Beanstalk hosts the deployed application.

The pipeline has been successfully validated with 16 passing Django unit tests, 95% overall code coverage, and an automated deployment to AWS Elastic Beanstalk.

---

**Author:** Shalini Gupta  
**Institution:** New York University, Tandon School of Engineering
