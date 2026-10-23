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