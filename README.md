# BENVENON


**BENVENON** a social media platform designed to support individuals relocating to Germany. The platform connects newcomers with local residents or experienced individuals who can help them overcome the challenges of starting a new life, such as language barriers, cultural differences, and navigating everyday tasks.

## Key Features

- **User Management**: Allows users to register, log in, and customize their profiles.
- **Post and Comment System**: Users can create posts, comment on others' posts, and like or interact with content.
- **Messaging**: Users can communicate via private messages



## Local development set-up

This project uses Poetry for dependency management. Follow the steps below to install Poetry and set up the project.

#### Prerequisites

- Python 3.7 or higher

#### Step 1: Clone the Repository

Clone this repository to your local machine using Git.

`git clone https://github.com/AGMS-Rocksters/social_club.git`

`cd social_club`


#### Step 2: Install Poetry

Poetry can be installed using the official installation script. Run the following command in your terminal:

`curl -sSL https://install.python-poetry.org | python3 -`

Alternatively, if you prefer using pip:

`pip install poetry`

Verify that Poetry has been installed by checking the version:

`poetry --version`

#### Step 3: Install Dependencies

Once Poetry is installed, navigate to the project directory and install the dependencies using the following command:

`poetry install --no-root`

#### Step 4: Set Up Environment Variables

The application requires a PostgreSQL database server to function properly (for how to provide connection details, see below).

In `src/` create an `.env` file with the following keys:

- SECRET_KEY (django secret key)
- SENDGRID_API_KEY (we use sendgrid as our email service)
- DEFAULT_FROM_EMAIL (verified email address on sendgrid)
- DB_NAME (database name)
- DB_USER (database user)
- DB_PASSWORD (database user password)
- DB_HOST (database server)
- DB_PORT (database port)
- STATIC_ROOT (where static files are ought to be stored)
- HOSTNAMES (in production, set it to "localhost,127.0.0.1")
- DEBUG (True in production, False otherwise)

**Hint**: make sure that the directory for static files exists if you intent to collect static files.

#### Step 5: Run Migrations

Apply the database migrations to set up the database schema:

`poetry run python manage.py runserver`

#### Step 6: Run the Development Server

Start the development server by running:

`python manage.py runserver`

The application will be available at http://127.0.0.1:8000/.


## Contribution

We welcome contributions to improve **BENVENON**! To contribute:

1. Fork the repository.
2. Create a new branch for your feature (git checkout -b feature-name).
3. Commit your changes (git commit -m 'Add new feature').
4. Push to the branch (git push origin feature-name).
5. Open a pull request for review.

Please make sure your code adheres to the project’s coding standards and includes appropriate tests.


## Contact

Created by the AGMS Rocksters team. Feel free to reach out for collaboration or questions!