from django.http import JsonResponse
import sqlite3

def appointments(request):
    conn = sqlite3.connect("appointments.db")
    conn.row_factory = sqlite3.Row
    
    sql_query = """SELECT name FROM sqlite_master 
    WHERE type='table';"""
    cursor = conn.cursor()
    cursor.execute(sql_query)
    
    tabels = ([row['name'] for row in cursor.fetchall()])
    final_data = {} 
    
    try:
        cursor_obj = conn.cursor()
        for row in tabels: # 'row' here is the table name
            print("Table name: ", row)
            cursor_obj.execute(f'SELECT * FROM "{row}";')
            final_data[row] = [dict(r) for r in cursor_obj.fetchall()]
        return JsonResponse(final_data)
    finally:
        conn.close()