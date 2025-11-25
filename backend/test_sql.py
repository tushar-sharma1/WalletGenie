#!/usr/bin/env python3
"""
Simple Cloud SQL connection test using cloud-sql-python-connector.
This tests if we can connect to the Cloud SQL instance.
"""
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

SQL_CONNECTION = os.getenv("SQL_CONNECTION")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_NAME = os.getenv("DB_NAME")

print("=" * 60)
print("Cloud SQL Connection Test")
print("=" * 60)
print(f"Instance: {SQL_CONNECTION}")
print(f"Database: {DB_NAME}")
print(f"User: {DB_USER}")
print("=" * 60)

try:
    from google.cloud.sql.connector import Connector
    import sqlalchemy
    import pg8000
    
    print("\n✓ Dependencies loaded successfully")
    
    # Create connector
    connector = Connector()
    
    def getconn():
        conn = connector.connect(
            SQL_CONNECTION,
            "pg8000",
            user=DB_USER,
            password=DB_PASS,
            db=DB_NAME,
        )
        return conn
    
    # Create SQLAlchemy engine
    pool = sqlalchemy.create_engine(
        "postgresql+pg8000://",
        creator=getconn,
    )
    
    print("\n✓ Connection pool created")
    
    # Test connection
    with pool.connect() as db_conn:
        result = db_conn.execute(sqlalchemy.text("SELECT version()")).fetchone()
        print(f"\n✓ Connection successful!")
        print(f"✓ PostgreSQL version: {result[0][:50]}...")
        
        # Test create table
        db_conn.execute(sqlalchemy.text(
            "CREATE TABLE IF NOT EXISTS test_table (id SERIAL PRIMARY KEY, name VARCHAR(50))"
        ))
        db_conn.commit()
        print("✓ Table creation successful")
        
        # Test insert
        db_conn.execute(sqlalchemy.text(
            "INSERT INTO test_table (name) VALUES ('test')"
        ))
        db_conn.commit()
        print("✓ Insert successful")
        
        # Test select
        result = db_conn.execute(sqlalchemy.text("SELECT COUNT(*) FROM test_table")).fetchone()
        print(f"✓ Read successful (rows: {result[0]})")
        
        # Cleanup
        db_conn.execute(sqlalchemy.text("DROP TABLE test_table"))
        db_conn.commit()
        print("✓ Cleanup successful")
    
    connector.close()
    
    print("\n" + "=" * 60)
    print("✅ All Cloud SQL tests passed!")
    print("=" * 60)
    
except ImportError as e:
    print(f"\n❌ Missing dependency: {e}")
    print("\nPlease install: pip install google-cloud-sql-connector pg8000 sqlalchemy")
    sys.exit(1)
except Exception as e:
    print(f"\n❌ Connection failed: {e}")
    sys.exit(1)
