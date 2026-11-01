import sqlite3
from ..Blueprints.Student import Student
from ..helper.year import get_year_id
from ..helper.api import ZermeloAPIClient
from .ZermeloMain import ZermeloMain

def saveStudents(api_client=None):
    api_client = api_client or ZermeloAPIClient()
    zermelo = ZermeloMain(api_client)
    conn = sqlite3.connect('./database.db')
    c = conn.cursor()
    try:
        startYear, endYear, year_id = get_year_id(api_client)
        for year in range(startYear, endYear + 1):
            result = zermelo.studentsindepartments(year_id[year])
            if result is None:
                print("No students returned for year: ", year)
                continue

            # Identifiers can't be parameterized, so validate and quote them
            table_name = f"STUDENTS_{int(year_id[year])}"

            c.execute(f'DROP TABLE IF EXISTS "{table_name}"')
            c.execute(f"""
                CREATE TABLE "{table_name}" (
                    id INTEGER PRIMARY KEY,
                    student TEXT NOT NULL,
                    departmentOfBranch INTEGER NOT NULL,
                    mentorGroup INTEGER,
                    mainGroup INTEGER NOT NULL,
                    groupInDepartments TEXT,
                    fullName TEXT NOT NULL,
                    schoolInSchoolYear INTEGER NOT NULL,
                    firstName TEXT NOT NULL,
                    lastName TEXT NOT NULL,
                    departmentOfBranchCode TEXT NOT NULL,
                    mainGroupName TEXT NOT NULL,
                    prefix TEXT
                )
            """)

            rows = [Student(s).to_tuple() for s in result]
            c.executemany(
                f'INSERT INTO "{table_name}" VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)',
                rows,
            )
            print(f"Year {year}: saved {len(rows)} students")
        conn.commit()
    except Exception as e:
        conn.rollback()
        print("Error occurred while saving students: ", e)
    finally:
        conn.close()


