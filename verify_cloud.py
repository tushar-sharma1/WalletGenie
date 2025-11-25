import os
from dotenv import load_dotenv
from google.cloud import storage
from google.cloud.sql.connector import Connector, IPTypes
import pg8000
import sqlalchemy

# Load env from backend/.env
load_dotenv(os.path.join(os.path.dirname(__file__), 'backend', '.env'))

def verify_gcs(bucket_name):
    print(f"\nVerifying GCS Bucket: {bucket_name}...")
    try:
        client = storage.Client()
        bucket = client.bucket(bucket_name)
        if not bucket.exists():
            print(f"❌ Bucket {bucket_name} does not exist.")
            return False
        
        # Try writing
        blob = bucket.blob("verification_test.txt")
        blob.upload_from_string("Verification successful!")
        print("✅ Successfully wrote to bucket.")
        
        # Try reading
        content = blob.download_as_string()
        print(f"✅ Successfully read from bucket: {content.decode()}")
        
        # Cleanup
        blob.delete()
        return True
    except Exception as e:
        print(f"❌ GCS Verification Failed: {e}")
        return False

def verify_sql(connection_name, db_user, db_pass, db_name):
    print(f"\nVerifying Cloud SQL: {connection_name}...")
    try:
        def get_conn():
            with Connector() as connector:
                conn = connector.connect(
                    connection_name,
                    "pg8000",
                    user=db_user,
                    password=db_pass,
                    db=db_name,
                    ip_type=IPTypes.PUBLIC,
                )
                return conn
        
        pool = sqlalchemy.create_engine(
            "postgresql+pg8000://",
            creator=get_conn,
        )
        
        with pool.connect() as db_conn:
            result = db_conn.execute(sqlalchemy.text("SELECT 1")).fetchone()
            print(f"✅ Successfully connected to SQL. Result: {result[0]}")
            
            # Create table test
            db_conn.execute(sqlalchemy.text("CREATE TABLE IF NOT EXISTS verification_test (id SERIAL PRIMARY KEY, name VARCHAR(50))"))
            db_conn.commit()
            print("✅ Successfully created/verified table.")
            
        return True
    except Exception as e:
        print(f"❌ Cloud SQL Verification Failed: {e}")
        return False

if __name__ == "__main__":
    # Load from .env or manual input
    # For this script, we expect user to set these or edit the script
    PROJECT_ID = os.getenv("PROJECT_ID", "<YOUR_PROJECT_ID>")
    BUCKET_NAME = os.getenv("GCS_BUCKET", f"walletgenie-bucket-{PROJECT_ID}")
    SQL_CONNECTION = os.getenv("SQL_CONNECTION", "<PROJECT:REGION:INSTANCE>")
    DB_USER = os.getenv("DB_USER", "postgres")
    DB_PASS = os.getenv("DB_PASS", "password123")
    DB_NAME = os.getenv("DB_NAME", "walletgenie")
    
    print("--- Cloud Verification Script ---")
    print("Ensure you have run 'gcloud auth application-default login' first!")
    
    verify_gcs(BUCKET_NAME)
    verify_sql(SQL_CONNECTION, DB_USER, DB_PASS, DB_NAME)
