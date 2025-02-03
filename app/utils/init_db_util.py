from app import create_app, db

def recreate_database():
    try:
        db.drop_all()
        db.create_all()

        return {"message": "Database reset successfully"}
    
    except Exception as e:
    
        return (f"Error: {e}")
