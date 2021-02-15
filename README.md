
### Glishy API.

![Glishy API](https://github.com/Glishy/glishy-bend/workflows/Glishy%20API/badge.svg)

#### Api Documentation

- use this [link]({base-url}/api/v1/graphql/) to access the api documentation

> ## How to set up the project.

### Features.

- python 3
- postgreSQL as database engine
- pipenv
- redis

---

### Installation.

- clone the repository

```
$ https://github.com/Glishy/glishy-bend.git
```

- cd into the directory

```
$ cd glishy-bend
```

- Install dependencies

```
$ make install
```

- After dependencies are installed, run the virtual environment

```
$ pipenv shell
```

- create environment variables
  On Unix or MacOS, run:

```
$ touch .env
```

open .env file and enter your corresponding database details as follows

```
DB_NAME=<DB name>
DB_USER=<Db User>
DB_HOST=<DB host>
DB_PASSWORD=<DB Password>
SECRET_KEY=<very-secret-key>
DJANGO_SETTINGS_MODULE=app.settings.development


```

Note: There is no space next to '='

---

##### On terminal,

```
$ source .env
```

- make migrations

```
$ make makemigrations
$ make migrate
```

- Run the application

```
make run
```

- Testing the application

```
$ make test
```

---

**Running Redis server**

- You can install redis by running the command `bash redis.sh` in the root project directory, this will install redis for you (if not already installed) and also run/start the redis server for the first time on your local machine.

**Running Celery worker**
Please endevour to update the `.env` file with the following keys and the appropriate values(`redis_server_url`):
`export CELERY_BROKER_URL=<Your_Redis_Server_URL>`

---

- To run redis after it has been stopped run `redis-server`

- In a new terminal tab run the Celery Message Worker with:

  ```
    celery -A app worker -l info --pool=gevent --concurrency=1000
  ```

## API documentation
> For the API documentation, the url is:

```
{base-url}/api/v1/docs/
```

---
