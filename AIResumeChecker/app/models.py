from app import db
from datetime import datetime
import json

class ResumeAnalysis(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    job_title = db.Column(db.String(255), nullable=False)
    job_description = db.Column(db.Text, nullable=False)
    resume_text = db.Column(db.Text, nullable=False)
    
    # Analysis results
    overall_score = db.Column(db.Float, nullable=False)
    technical_skills_score = db.Column(db.Float, nullable=False)
    soft_skills_score = db.Column(db.Float, nullable=False)
    keyword_match_score = db.Column(db.Float, nullable=False)
    
    # JSON fields for detailed results
    matched_skills = db.Column(db.Text)  # JSON string
    missing_skills = db.Column(db.Text)  # JSON string
    recommendations = db.Column(db.Text)  # JSON string
    extracted_entities = db.Column(db.Text)  # JSON string
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def set_matched_skills(self, skills_list):
        self.matched_skills = json.dumps(skills_list)
    
    def get_matched_skills(self):
        return json.loads(self.matched_skills) if self.matched_skills else []
    
    def set_missing_skills(self, skills_list):
        self.missing_skills = json.dumps(skills_list)
    
    def get_missing_skills(self):
        return json.loads(self.missing_skills) if self.missing_skills else []
    
    def set_recommendations(self, recommendations_list):
        self.recommendations = json.dumps(recommendations_list)
    
    def get_recommendations(self):
        return json.loads(self.recommendations) if self.recommendations else []
    
    def set_extracted_entities(self, entities_dict):
        self.extracted_entities = json.dumps(entities_dict)
    
    def get_extracted_entities(self):
        return json.loads(self.extracted_entities) if self.extracted_entities else {}