from django.http import JsonResponse
import sqlite3



def students(request):
    connection_obj = sqlite3.connect("database.db")
    connection_obj.row_factory = sqlite3.Row
    try:
        cursor_obj = connection_obj.cursor()
        cursor_obj.execute("SELECT * FROM students;")
        rows = [dict(row) for row in cursor_obj.fetchall()]
        return JsonResponse(rows, safe=False)
    finally:
        connection_obj.close()


