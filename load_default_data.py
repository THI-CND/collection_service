from django.db import connection
import os

cursor = connection.cursor()
cursor.execute('SELECT COUNT(*) FROM collection_service_user')
if cursor.fetchone()[0] == 0:
    print("No users found in database. Loading default data...")
    os.system('python manage.py loaddata default_database.json')
else:
    print("Users found in database. Skipping loading default data.")