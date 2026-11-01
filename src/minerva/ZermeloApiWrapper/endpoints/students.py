from django.http import JsonResponse
import sqlite3

def students(request):
    fields_param = request.GET.get('fields')
    
    requested_fields = fields_param.split(',') if fields_param else None

    connection_obj = sqlite3.connect("database.db")
    connection_obj.row_factory = sqlite3.Row
    
    sql_query = "SELECT name FROM sqlite_master WHERE type='table';"
    cursor = connection_obj.cursor()
    cursor.execute(sql_query)
    
    tabels = [row['name'] for row in cursor.fetchall()]
    final_data = {} 
    
    try:
        cursor_obj = connection_obj.cursor()
        for row in tabels:
            cursor_obj.execute(f'SELECT * FROM "{row}";')
            
            tabel_data = []
            for r in cursor_obj.fetchall():
                row_dict = dict(r)
                
                if requested_fields:
                    filtered_dict = {key: value for key, value in row_dict.items() if key in requested_fields}
                    tabel_data.append(filtered_dict)
                else:
                    tabel_data.append(row_dict)
            
            final_data[row] = tabel_data
            
        return JsonResponse(final_data)
    finally:
        connection_obj.close()