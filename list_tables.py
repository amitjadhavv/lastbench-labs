import os
import django
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lastbench_project.settings')
django.setup()

from django.db import connection

def list_tables():
    with connection.cursor() as cursor:
        cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
        tables = cursor.fetchall()
        print("\n--- CURRENT TABLES ---")
        for table in tables:
            print(f" - {table[0]}")
        print("----------------------\n")

def cleanup():
    # ONLY these two specific non-Django tables
    extra_tables = ['users', 'applications']
    
    with connection.cursor() as cursor:
        print("--- CLEANING UP EXTRA TABLES ---")
        for table in extra_tables:
            try:
                cursor.execute(f"DROP TABLE IF EXISTS {table} CASCADE")
                print(f" [SUCCESS] Dropped table: {table}")
            except Exception as e:
                print(f" [ERROR] Could not drop {table}: {e}")
        print("--- CLEANUP COMPLETE ---\n")

if __name__ == "__main__":
    if "--cleanup" in sys.argv:
        cleanup()
    list_tables()
