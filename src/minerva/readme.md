# Zermelo API client

This project communicates with the Zermelo API. It can request data from
selected API endpoints, import appointments, and save data in JSON or SQLite
databases.

The project was developed as part of the Terra hackathon. You need access to the correct school environment and a valid API token before you
can run or test it. So thats why i will make an showcase video for each week where i will showcase new features. 

Terra prepweek 3 demo vid:

https://youtu.be/EDJ7mm9nUns

Terra week 1 demo vid:

https://youtu.be/EyiI8oIQkUc

# Why Minerva?

Minerva is the Roman goddess of wisdom, learning, and strategic thinking. She
represents the purpose of this project: turning complex school data into
useful knowledge and helping users find the information they need.

## Installation

Clone or download this repository and open a terminal in the project folder.
Python 3.10 or newer is recommended.

Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

On Windows, activate it with:

```powershell
.venv\Scripts\Activate.ps1
```
On linux with 
```bash
source .venv/bin/activate
```

Install the required Python packages:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Environment configuration

Create a `.env` file in the root of the repository by copying
`.example.env`:

```bash
cp .example.env .env
```

Fill in the values in `.env`:

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
the project. `EMAIL` and `PASSWORD` are only needed when using the automatic
token helper.

Do not commit or share `.env`. It contains credentials and API access data.
The repository already ignores this file through `.gitignore`.

### Getting an API token

The project cannot work without a valid Zermelo API token. Without one, API
requests will be rejected and the scripts cannot be properly tested. A token
can be entered manually in `.env` as `AUTHORIZATION=Bearer your-api-token`.

The helper in `helper/get_api_token.py` can also retrieve a token through the
Zermelo login flow. This requires `EMAIL`, `PASSWORD`, Google Chrome, and a
compatible ChromeDriver. The helper currently expects ChromeDriver at
`/usr/bin/chromedriver` on Linux.

## Using the command-line client

Run the main interactive client from the repository root:

```bash
python main.py
```

The menu lets you request appointments, branches, departments, holidays,
students, and other data from the Zermelo API. The results are printed as JSON.

## Importing appointments for students

`ImportData/MassImportAppointments.py` imports appointments for a range of
student IDs. Before using it, make sure that:

- `.env` contains a valid `SCHOOL` and `AUTHORIZATION` value;
- `database.db` exists and contains the required `STUDENTS` table;
- you run the command from the repository root.

Use this command:

```bash
python ImportData/MassImportAppointments.py students FirstId LastId
```

This imports appointments for student IDs `FirstId` through `LastId`, including
both the first and last ID. The imported appointments are stored in
`appointments.db`. The script commits the data when the import finishes.

To import appointments for all students in the latest students table, use:

```bash
python ImportData/MassImportAppointments.py allDatabase
```

## Local api wrapper
I also build a api wrapper with django, it runs on `http://localhost:8000` You can request fields or everything, supported enpoints are:
`/api/students` and `/api/appointments/`.

### Supported students field
with the `/api/students` the following fields are supported:

| Field | Type |
| ---|----|
|id|Int|
|student|String|
|departmentOfBranch|Int|
|MmentorGroup|Int|
|mainGroup|Int|
|groupInDepartments|String|
|fullName|String|
|schoolInSchoolYear|Int|
|firstName|String|
|lastName|String|
|departmentOfBranchCode|String|
|mainGroupName|String|
|prefix|String|

The api requird an api key definned in `.env` as `API_WRAPPER_KEY` generage this key with 
 ```bash
openssl rand -hex 32  
```
And put it in the reqeust header as `X-Api-Key: Api-Key`

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