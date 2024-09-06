## Local Set-Up

In `src/` create an `.env` file with the following keys:

- SECRET_KEY (consider regular key rotation)
- DB_NAME
- DB_USER
- DB_PASSWORD
- DB_HOST
- DB_PORT
- STATIC_ROOT (where static files are ought to be stored)
- HOSTNAMES
- DEBUG (False or True)

Hint: make sure that the directory for static files exists if you intent to collect static files.
