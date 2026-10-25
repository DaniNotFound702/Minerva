# Development Log

This log is based on the committed Git history of the project.

## 2026-10-14 - Initial setup

- Created the initial `main.py` file as the starting point for the project.
- Commit: `098fa75` (`Init`)

## 2026-10-16 - Zermelo API base

- Added the first Zermelo API client setup.
- Added environment variable loading with `python-dotenv`.
- Added configuration for the school, API authorization, base URL, and request headers.
- Added the first school-year lookup and appointment retrieval logic.
- Added `.gitignore` entries and a data directory reference.
- Commits: `06daec5`, `40a62b7`

## 2026-10-18 - Base features and documentation

- Added more API functionality and fixed initial bugs.
- Added retrieval of users and school-year IDs.
- Created `helper/helper.py` for shared API configuration and school-year helpers.
- Added the first `readme.md` with project information and setup requirements.
- Commit: `9407664`, `f34721a`

## 2026-10-18 - ImportData structure and endpoint expansion

- Reorganized the application into the `ImportData` package.
- Added `ImportData/ZermeloMain.py` as the main API module.
- Added `ImportData/ImportAppointments.py` as the appointment import entry point.
- Added package initialization files for `ImportData` and `helper`.
- Replaced the original root `main.py` implementation with the new package structure.
- Added logging and automatic creation of `logs/messages` directories.
- Added endpoint functions for appointments, branches, users, departments, holidays, jobs, locations, school years, time slots, and students.
- Added a shared endpoint request helper.
- Commit: `369ea9d` (`added more enpoints`)

## 2026-10-19 - Parameterized endpoint requests

- Updated endpoint functions to accept school-year IDs, school years, and user IDs where needed.
- Improved request construction through the shared endpoint helper.
- Updated helper code to support the expanded endpoint workflow.
- Commit: `279b221` (`MOREEE ENDPONTS`)

## 2026-10-20 - More fields and student retrieval

- Added more appointment response fields, including teachers, subjects, locations, online details, capacity, and modification information.
- Added a student retrieval function.
- Improved the helper script and endpoint data handling.
- Commit: `b4ac960` (`more fields for endpoints and better helper script`)

## 2026-10-21 - Added dev log
- Added a dev log file

## 2026-10-23 - Database and API wrapper

- Added SQLite-backed student and appointment data models through the `Blueprints` modules.
- Added student and appointment import scripts that fetch API data and store it in the local database.
- Added a Selenium-based helper for obtaining the Zermelo API authorization token through the login flow.
- Added a helper for retrieving school-year IDs and a helper for logging API messages.
- Refactored the API helper functions and expanded the import workflow.
- Added Django project scaffolding, including settings, URL configuration, WSGI/ASGI entry points, and a student API endpoint.
- Added a root `main.py` and `manage.py` for the database/API application.
- Updated the README and `.gitignore` for the new project structure.
- Commit: `ed3e3c5` (`added database for the students and a api wrapper`)

## 2026-10-25 - Mass appointment import

- Added `ImportData/MassImportAppointments.py` to import appointments for a range of student IDs.
- Expanded the appointment importer to fetch, convert, and store appointment data in `appointments.db`.
- Added shared API and school-year helpers in `helper/api.py` and `helper/year.py`.
- Removed the older duplicate helper modules and moved their functionality into the new helpers.
- Added an `.example.env` file and a `requirements.txt` file for setup and dependencies.
- Expanded the README with installation instructions, environment configuration, token setup, and mass-import usage.
- Updated the student API route to `/api/students/`.
- Commit: `d641363` (`Implemented massImportAppointments`)