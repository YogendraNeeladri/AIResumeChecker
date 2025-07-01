import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///resume_analyzer.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = 'uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    
    # NLP Model settings
    SPACY_MODEL = 'en_core_web_sm'
    
    # Skills database (can be expanded)
    TECHNICAL_SKILLS = [
        'python', 'javascript', 'java', 'c++', 'c#', 'react', 'angular', 'vue',
        'node.js', 'express', 'django', 'flask', 'spring', 'laravel', 'ruby',
        'php', 'go', 'rust', 'kotlin', 'swift', 'typescript', 'html', 'css',
        'sass', 'less', 'bootstrap', 'tailwind', 'jquery', 'ajax', 'json',
        'xml', 'sql', 'mysql', 'postgresql', 'mongodb', 'redis', 'elasticsearch',
        'docker', 'kubernetes', 'aws', 'azure', 'gcp', 'jenkins', 'git',
        'github', 'gitlab', 'jira', 'agile', 'scrum', 'devops', 'ci/cd',
        'machine learning', 'ai', 'data science', 'tensorflow', 'pytorch',
        'pandas', 'numpy', 'scikit-learn', 'jupyter', 'tableau', 'power bi'
    ]
    
    SOFT_SKILLS = [
        'leadership', 'communication', 'teamwork', 'problem solving',
        'critical thinking', 'creativity', 'adaptability', 'time management',
        'project management', 'analytical thinking', 'collaboration',
        'presentation', 'negotiation', 'mentoring', 'coaching'
    ]