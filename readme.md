# Minerva

Minerva is an importable Python library for interacting with the Zermelo API.
It provides an authenticated API client, convenience methods for common
Zermelo resources, appointment import utilities, and an optional Django API
wrapper.

You need access to the correct Zermelo school environment and a valid API token
to make requests.

## Installation

Minerva requires Python 3.10 or newer. Install it from the repository with:

Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```



Install the library:

```bash
pip install --upgrade pip
pip install minerva-zermelo
```


## Configuration

The library client can be configured directly in your application. This is the
recommended approach when credentials come from a settings page, secrets
manager, or command-line arguments:

```python
from minerva import ZermeloAPIClient

client = ZermeloAPIClient(
	school="your-school",
	authorization="Bearer your-api-token",
)
```



`your-school` is the school name used in the Zermelo URL, for example
`https://your-school.zportal.nl`. `AUTHORIZATION` must contain the full header
value, including `Bearer `. `SCHOOLYEAR` and `USER` are used by some parts of
the optional import helpers. `EMAIL` and `PASSWORD` are only needed when using
the automatic token helper.


## Library usage

`ZermeloAPIClient` exposes `get_endpoint(endpoint, parameters)` for direct
requests. The endpoint name is appended to the school API URL and parameters
are supplied as a query string:

```python
from minerva import ZermeloAPIClient

client = ZermeloAPIClient(
    school="your-school",
    authorization="Bearer your-api-token",
)

branches = client.get_endpoint(
	"branches",
	"fields=name,code,somCode,somUuid",
)
```

For common requests, use `ZermeloMain` convenience methods. It accepts an
already configured `ZermeloAPIClient`:

```python
from minerva import ZermeloAPIClient, ZermeloMain

client = ZermeloAPIClient(
    school="your-school",
    authorization="Bearer your-api-token",
)
zermelo = ZermeloMain(client)

branches = zermelo.branches()
holidays = zermelo.holidays()
students = zermelo.studentsindepartments(schoolYear=1234)
appointments = zermelo.appointments(
	schoolYear_id=1234,
	schoolYear=2026,
	user_id=5678,
)
```

The convenience layer also provides `branchesofschools()`,
`departmentsofbranches()`, `choosableindepartments()`, `groupindepartments()`,
`locationofbranches()`, `schoolsinschoolyears()`, `timeslotnames()`, and
`subjectselectionsubjects()`.

Successful calls return the API `data` value, usually a list of dictionaries.
Unauthorized or other API errors raise `ZermeloAPIError`; network errors from
`requests` are re-raised. A forbidden request returns `None`.

The main public exports are available directly from `minerva`:

```python
from minerva import (
	ZermeloAPIClient,
	ZermeloAPIError,
	ZermeloMain,
	Appointment,
	Student,
	saveAll,
	configure_api_wrapper,
)
```

### Optional token helper

The library requires a valid Zermelo API token to make requests. You can
provide one directly to `ZermeloAPIClient` or through the `AUTHORIZATION`
environment variable.

The optional `get_api_token` helper can retrieve a token through the Zermelo
login flow. Import it from the package:

```python
from minerva import get_api_token

token = get_api_token(
	school="your-school",
	email="your-email-address",
	password="your-password",
)
```

It requires the `token` extra, `EMAIL`,
`PASSWORD`, Google Chrome, and a compatible ChromeDriver. The helper currently
expects ChromeDriver at `/usr/bin/chromedriver` on Linux.

## Fill the database first

The database must be populated before using `saveAll` or starting the Django
API wrapper. The import process has this order:

1. `saveStudents()` requests students from Zermelo and creates the required
	`STUDENTS_<school-year-id>` tables in `database.db`.
2. `saveAll()` reads the newest student table and imports appointments for all
	students into `appointments.db`.
3. The Django API wrapper can then serve the imported students and appointments.

### Import students

Import `saveStudents` from the package and run it with the same configured API
client that you use for the other library calls:

```python
from minerva import ZermeloAPIClient, saveStudents

client = ZermeloAPIClient(
	 school="your-school",
	 authorization="Bearer your-api-token",
)

saveStudents(client)
```

This creates or replaces the student tables in `database.db`. Run this step
again when you need to refresh the student data.

### Import appointments

The `saveAll` helper imports appointments for students from the local database.
Import it directly from the package:

```python
from minerva import ZermeloAPIClient, saveAll

client = ZermeloAPIClient(
	school="your-school",
	authorization="Bearer your-api-token",
)
saveAll(".", client)
```

Before using it, make sure that:

- the `ZermeloAPIClient` receives valid `school` and `authorization` values;
- `saveStudents(client)` has already created a `STUDENTS_<school-year-id>`
	table in `database.db`;
- `database.db` and `appointments.db` are writable;
- the current working directory contains the appointment database files.

`saveAll` uses a configured `ZermeloAPIClient` and stores imported appointments
in SQLite. It is an additional utility and is not required to use the API
client.

## Optional Django API wrapper

After the database import steps have completed, the package can expose the
stored Zermelo data through a Django wrapper. It currently provides:

- `GET /api/students/`
- `GET /api/appointments/`

Install the optional Django dependencies:

```bash
python -m pip install -e ".[django]"
```

The wrapper can be used in two ways:

- Start the included development server for local use.
- Include the package URL patterns in an existing Django project.

### Use in an existing Django project

Add the Minerva API routes to the host project's `urls.py`:

```python
from django.urls import include, path

urlpatterns = [
	path("", include("minerva.ZermeloApiWrapper.urls")),
]
```

Configure the API key during application startup:

```python
from minerva import configure_api_wrapper

configure_api_wrapper("your-wrapper-key")
```

The URL configuration is also available through the public package API when
the host application needs to build its routes programmatically:

```python
from minerva import get_api_urlpatterns

urlpatterns = get_api_urlpatterns()
```

Set an API key in the process environment before starting the server:

```bash
export API_WRAPPER_KEY="your-wrapper-key"
```


Start the development server from the repository root:

```bash
DJANGO_SETTINGS_MODULE=minerva.ZermeloApiWrapper.settings django-admin runserver
```

The wrapper is available at `http://127.0.0.1:8000/`. It reads its data from
the local SQLite databases, so start it from the directory containing those
files. Use `--noreload` if your host application configures the wrapper key in
Python and you do not want Django's development reloader:

```bash
DJANGO_SETTINGS_MODULE=minerva.ZermeloApiWrapper.settings django-admin runserver --noreload
```

When embedding the wrapper in another Django application, call
`configure_api_wrapper("your-wrapper-key")` during application setup instead
of using `API_WRAPPER_KEY` in the environment.

### API-key authentication

Every request whose path starts with `/api/` must include an `X-Api-Key`
header. The key must match the value configured by the host application with
`configure_api_wrapper()`:

```python
from minerva import configure_api_wrapper

configure_api_wrapper("your-wrapper-key")
```

For deployment, generate a strong key and store it securely:

```bash
openssl rand -hex 32
```

Send the generated value directly as the header value. Do not add a
`Bearer` or `Api-Key` prefix:

```bash
curl \
	-H "X-Api-Key: your-wrapper-key" \
	http://127.0.0.1:8000/api/students/
```

Requests with a missing or incorrect key receive HTTP `401`. If no wrapper
key is configured, API requests receive HTTP `500`. Non-API paths do not
require the key.

### Students fields

The students endpoint supports these fields:

| Field | Type |
| --- | --- |
| `id` | Integer |
| `student` | Integer |
| `departmentOfBranch` | Integer |
| `mentorGroup` | Integer |
| `mainGroup` | Integer |
| `groupInDepartments` | String |
| `fullName` | String |
| `schoolInSchoolYear` | Integer |
| `firstName` | String |
| `lastName` | String |
| `departmentOfBranchCode` | String |
| `mainGroupName` | String |
| `prefix` | String |

## Testing

Run the test suite from the repository root:

```bash
python -m pytest
```

The middleware tests verify accepted and rejected API keys, missing keys, and
that non-API paths remain accessible.

## Current functionality

Available API data includes:

- Appointments
- Choosable departments
- School branches
- Users
- Departments of branches
- Branches
- Holidays and school years
- Students and subjects

## Credits

Parts of this project are inspired by
[ZermeloUtils](https://github.com/electricsteve/ZermeloUtils) by electricsteve.

AI was used to help explain code, complete parts of `get_api_token.py`, and
write documentation.