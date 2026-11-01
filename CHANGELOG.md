# Project Change Log

This file records the complete committed Git history of the project in chronological order. It does not include uncommitted working-tree changes.

## 2026-10-14 - Initial project

- Created the initial `main.py` file.
- Commit: `098fa75` (`Init`)

## 2026-10-16 - API base

- Added the first Zermelo API client configuration.
- Added environment variable loading with `python-dotenv`.
- Added school, authorization, base URL, and request header configuration.
- Added the first school-year and appointment request logic.
- Commit: `06daec5` (`base`)

## 2026-10-16 - Data folder setup

- Added initial `.gitignore` configuration.
- Added a data folder reference to the project.
- Commit: `40a62b7` (`data folder`)

## 2026-10-18 - Base features and fixes

- Added more API functionality and fixed initial bugs.
- Added school-year ID and user retrieval.
- Expanded appointment retrieval and response handling.
- Commit: `9407664` (`added more base features and bug fixes`)

## 2026-10-18 - Helper module and README

- Added `helper/helper.py` for shared API configuration and school-year helpers.
- Refactored the main script to use helper functionality.
- Added the first project README.
- Updated `.gitignore`.
- Commit: `f34721a` (`added a readme`)

## 2026-10-18 - Endpoint expansion

- Created the `ImportData` package and moved the main API workflow into it.
- Added appointment import support.
- Added endpoint functions for appointments, branches, users, departments, holidays, jobs, locations, school years, time slots, and students.
- Added a shared endpoint request helper.
- Added logging and automatic creation of the `logs/messages` directories.
- Removed the old root `main.py` implementation.
- Commit: `369ea9d` (`added more enpoints`)

## 2026-10-19 - Parameterized requests

- Updated endpoint functions to accept school-year IDs, school years, and user IDs.
- Improved request construction and endpoint parameters.
- Updated helper functionality for the expanded endpoint workflow.
- Commit: `279b221` (`MOREEE ENDPONTS`)

## 2026-10-20 - More API fields

- Added more appointment fields, including teachers, subjects, locations, online details, capacity, and modification information.
- Added student retrieval support.
- Improved helper and endpoint data handling.
- Commit: `b4ac960` (`more fields for endpoints and better helper script`)

## 2026-10-23 - Database and API wrapper

- Added SQLite-backed `Student` and `Appointment` blueprints.
- Added student and appointment import scripts.
- Added automatic Zermelo API token retrieval through Selenium and the login flow.
- Added school-year and API message logging helpers.
- Added Django project scaffolding with settings, URLs, WSGI, and ASGI entry points.
- Added a student API endpoint.
- Added `main.py` and `manage.py` for the database/API application.
- Updated the README and `.gitignore`.
- Commit: `ed3e3c5` (`added database for the students and a api wrapper`)

## 2026-10-23 - Devlog update

- Updated `DEVLOG.md` with the project history through the database and API wrapper work.
- Commit: `a5fab31` (`updated dev log`)

## 2026-10-25 - Mass appointment import

- Added `ImportData/MassImportAppointments.py` for importing appointments across a range of student IDs.
- Expanded appointment import and storage in `appointments.db`.
- Added shared API and school-year helpers in `helper/api.py` and `helper/year.py`.
- Removed duplicate older helper modules.
- Added `.example.env` and `requirements.txt`.
- Expanded the README with installation, environment, token, API, and mass-import instructions.
- Updated the student API route to `/api/students/`.
- Commit: `d641363` (`Implemented massImportAppointments`)

## 2026-10-25 - Devlog update

- Updated `.gitignore`.
- Added the latest mass-import work to `DEVLOG.md`.
- Commit: `017e0f5` (`Updated devlog`)

## 2026-10-26 - Appointment API wrapper

- Added appointments to the Django API wrapper.
- Added `zermeloAPI/endpoints/Appointments.py`.
- Expanded the students endpoint and improved student import behavior.
- Made small bug fixes in the import and API code.
- Updated URL routing for the appointment endpoint.
- Commit: `e4a2a49` (`some small bugfixses and add the Apointments to the api wrapper`)

## 2026-10-28 - API and authentication fixes

- Fixed appointment import and mass-import behavior.
- Improved school-year handling.
- Corrected the appointments API endpoint implementation.
- Added API authentication middleware.
- Updated Django settings for the middleware.
- Commit: `614557a` (`More small bugfixes`)

## 2026-10-29 - Documentation updates

- Expanded the README with more project documentation.
- Added an additional documentation update describing project usage and behavior.
- Commits: `d41e8df` (`More documentair`), `20d2381` (`More documentair`)

## 2026-10-30 - First library packaging

- Added the `pyproject.toml` package configuration.
- Added the `LICENSE` file.
- Added the first distributable package archive.
- Moved the project into the `scr/Minerva` package layout.
- Moved the API, helper, import, blueprint, and Django files into the package.
- Added package documentation in `scr/Minerva/readme.md`.
- Added and cleaned up ignored files and generated Python cache files.
- Commit: `6a83d1d` (`Libary test`)

## 2026-10-30 - Move to `src/minerva`

- Moved the Minerva package from `scr/Minerva` to `src/minerva`.
- Moved import scripts, blueprints, helpers, and Django wrapper files into the new source layout.
- Preserved the package contents while changing the project structure.
- Commit: `a7d6078` (`small fixes`)

## 2026-10-30 - Cleanup and wrapper rename

- Expanded `.gitignore` to exclude generated files and build artifacts.
- Removed tracked Python cache files and the old package archive.
- Renamed `zermeloAPI` to `ZermeloApiWrapper`.
- Cleaned up the old root-level structure.
- Commit: `b2a93b5` (`small fixes`)

## 2026-10-30 - Library refactor

- Refactored `ZermeloMain` into a reusable package API.
- Reworked API helper functions and request handling.
- Simplified the year helper.
- Updated package initialization and environment configuration.
- Removed obsolete import code.
- Commit: `1f607e7` (`small fixes + big refactor`)

## 2026-11-01 - Library packaging refactor

- Completed the library refactor in the `src/minerva` layout.
- Updated `pyproject.toml` package metadata and build configuration.
- Updated the README with expanded installation, usage, API, import, and library documentation.
- Updated import scripts and mass appointment importing for the refactored package.
- Updated the `ZermeloApiWrapper` Django package, authentication middleware, settings, URLs, and WSGI/ASGI files.
- Improved API token, API request, and school-year helper implementations.
- Updated `.gitignore` for the final package structure.
- Commit: `7de39cc` (`libary refactor`)
