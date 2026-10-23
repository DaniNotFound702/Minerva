# Zermelo API client

This project interacts with the Zermelo API for a school. It builds requests
for selected API endpoints and currently provides a command-line workflow for
downloading the responses as a JSON file. The available data includes:

- Appointments
- Choosable departments
- Branches of schools
- Users
- Departments of branches
- Branches
- and a lot more

## Terra-specific project

This project was created specifically for Terra schools and is intended to
communicate with Terra's Zermelo API. It is not a general-purpose client that
can be used by anyone without additional configuration.

### API token required

You need a valid Zermelo API token to use this project. The token is required to
authenticate requests to the Zermelo API and to retrieve data for the correct
school environment. Without a token, the requests cannot be authenticated, so
the project cannot be run or properly tested. Thats why i will make a vid for each week!

#### Terra prepweek 3 demo vid:
https://youtu.be/EDJ7mm9nUns

### Current functionality

The project currently provides a command-line workflow for requesting data
from selected Zermelo API endpoints and saving the responses as a JSON file.
The available data includes:

- Appointments
- Choosable departments
- School branches
- Users
- Departments of branches
- Branches
- Additional data exposed by the API

# Credits
A lot of code is inspirrated from [ZermeloUtils](https://github.com/electricsteve/ZermeloUtils) by electricsteve! 

# How was AI used
I used AI to explain stuff and it help compleating the `get_api_token.py` and writing this readme and devlog!