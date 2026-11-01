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

On Windows, activate it with:

```powershell
\.venv\Scripts\Activate.ps1
```

On Linux, activate it with:

```bash
source .venv/bin/activate
```

Install the library:

```bash
python -m pip install --upgrade pip
python -m pip install -e .
```

For development, install the optional dependencies as needed:

```bash
python -m pip install -e ".[dev]"
python -m pip install -e ".[django]"
python -m pip install -e ".[token]"
```

The editable install makes the `minerva` package available to applications
running in the environment.

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

branches = client.get_endpoint(
	"branches",
	"fields=name,code,somCode,somUuid",
)
print(branches)
```

The values can come from a settings page, a secrets manager, command-line
arguments, or any other configuration source. A `.env` file is not required.

### Optional environment configuration

If your application uses environment variables, the client accepts these
values as a fallback:

Create a `.env` file in the root of the repository by copying
`.example.env`, then load it in your application with `python-dotenv` or your
preferred configuration library:

```bash
cp .example.env .env
```

```env
SCHOOL=your-school
SCHOOLYEAR=your-school-year-id
AUTHORIZATION=Bearer your-api-token
EMAIL=your-email-address
PASSWORD=your-password
USER=your-user-id
```

`SCHOOL` is the school name used in the Zermelo URL, for example
`https://your-school.zportal.nl`. `AUTHORIZATION` must contain the full header
value, including `Bearer `. `SCHOOLYEAR` and `USER` are used by some parts of
the optional import helpers. `EMAIL` and `PASSWORD` are only needed when using
the automatic token helper.

Do not commit or share `.env`. It contains credentials and API access data.
The repository already ignores this file through `.gitignore`.

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

The optional helper in `src/minerva/helper/get_api_token.py` can retrieve a
token through the Zermelo login flow. It requires the `token` extra, `EMAIL`,
`PASSWORD`, Google Chrome, and a compatible ChromeDriver. The helper currently
expects ChromeDriver at `/usr/bin/chromedriver` on Linux.

## Optional appointment imports

`src/minerva/ImportData/MassImportAppointments.py` contains utilities for
importing appointments for a range of student IDs. Before using them, make sure
that:

- `.env` contains a valid `SCHOOL` and `AUTHORIZATION` value;
- `database.db` exists and contains the required `STUDENTS` table;
- you run the command from the repository root.

The import functions use a configured `ZermeloAPIClient` and store imported
appointments in SQLite. They are additional utilities and are not required to
use the API client.

## Optional Django API wrapper

The package also includes a Django wrapper for exposing selected Zermelo data
through HTTP. It currently provides:

- `GET /api/students/`
- `GET /api/appointments/`

Start the development server from the repository root:

```bash
python src/minerva/manage.py runserver
```

The wrapper is available at `http://127.0.0.1:8000/`. The endpoint
implementation reads its data from the local SQLite databases and supports
field selection where implemented by the endpoint.

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