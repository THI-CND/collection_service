from django.db import connection
import os

cursor = connection.cursor()
cursor.execute('SELECT COUNT(*) FROM collection_service_collection')
if cursor.fetchone()[0] == 0:
    print("No collections found in database. Loading default data...")
    os.system('python manage.py loaddata default_database.json')
else:
    print("Collections found in database. Skipping loading default data.")