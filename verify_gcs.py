import os
from dotenv import load_dotenv
from google.cloud import storage

# Load env from backend/.env
load_dotenv(os.path.join(os.path.dirname(__file__), 'backend', '.env'))

def verify_gcs(bucket_name, project_id):
    print(f"\nVerifying GCS Bucket: {bucket_name}...")
    try:
        client = storage.Client(project=project_id)
        bucket = client.bucket(bucket_name)
        if not bucket.exists():
            print(f"❌ Bucket {bucket_name} does not exist.")
            print(f"   Create it with: gcloud storage buckets create gs://{bucket_name} --location=us-central1")
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
        print("✅ GCS verification passed!")
        return True
    except Exception as e:
        print(f"❌ GCS Verification Failed: {e}")
        return False

if __name__ == "__main__":
    PROJECT_ID = os.getenv("PROJECT_ID", "walletgenie-hackathon")
    BUCKET_NAME = os.getenv("GCS_BUCKET", f"walletgenie-bucket-{PROJECT_ID}")
    
    print("--- GCS Verification Script ---")
    print("Ensure you have run 'gcloud auth application-default login' first!")
    print(f"Project ID: {PROJECT_ID}")
    print(f"Bucket: {BUCKET_NAME}")
    
    verify_gcs(BUCKET_NAME, PROJECT_ID)
