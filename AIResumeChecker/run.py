from app import create_app, db
from flask_migrate import upgrade
import os

app = create_app()

def deploy():
    """Run deployment tasks."""
    # Create database tables
    with app.app_context():
        db.create_all()
        
        # Download spaCy model if not present
        try:
            import spacy
            spacy.load('en_core_web_sm')
        except OSError:
            print("Downloading spaCy model...")
            os.system('python -m spacy download en_core_web_sm')

if __name__ == '__main__':
    deploy()
    app.run(debug=True, host='0.0.0.0', port=5000)