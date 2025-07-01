import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re
from collections import Counter
from config import Config

class NLPAnalyzer:
    def __init__(self):
        try:
            self.nlp = spacy.load(Config.SPACY_MODEL)
        except OSError:
            print(f"spaCy model '{Config.SPACY_MODEL}' not found. Installing...")
            import subprocess
            subprocess.run(['python', '-m', 'spacy', 'download', Config.SPACY_MODEL])
            self.nlp = spacy.load(Config.SPACY_MODEL)
        
        self.technical_skills = [skill.lower() for skill in Config.TECHNICAL_SKILLS]
        self.soft_skills = [skill.lower() for skill in Config.SOFT_SKILLS]
    
    def preprocess_text(self, text: str) -> str:
        """Clean and preprocess text."""
        # Remove extra whitespace and normalize
        text = re.sub(r'\s+', ' ', text.strip())
        # Remove special characters but keep important punctuation
        text = re.sub(r'[^\w\s\.\,\-\+\#]', ' ', text)
        return text.lower()
    
    def extract_skills(self, text: str) -> dict:
        """Extract technical and soft skills from text."""
        processed_text = self.preprocess_text(text)
        
        technical_found = []
        soft_found = []
        
        # Check for technical skills
        for skill in self.technical_skills:
            if skill in processed_text or skill.replace(' ', '') in processed_text.replace(' ', ''):
                technical_found.append(skill)
        
        # Check for soft skills
        for skill in self.soft_skills:
            if skill in processed_text:
                soft_found.append(skill)
        
        return {
            'technical': list(set(technical_found)),
            'soft': list(set(soft_found))
        }
    
    def extract_entities(self, text: str) -> dict:
        """Extract named entities from text."""
        doc = self.nlp(text)
        entities = {
            'organizations': [],
            'education': [],
            'locations': [],
            'technologies': []
        }
        
        for ent in doc.ents:
            if ent.label_ == "ORG":
                entities['organizations'].append(ent.text)
            elif ent.label_ in ["GPE", "LOC"]:
                entities['locations'].append(ent.text)
            elif ent.label_ in ["PRODUCT", "EVENT"]:
                entities['technologies'].append(ent.text)
        
        # Remove duplicates
        for key in entities:
            entities[key] = list(set(entities[key]))
        
        return entities
    
    def extract_keywords(self, text: str, top_n: int = 20) -> list:
        """Extract important keywords using TF-IDF."""
        processed_text = self.preprocess_text(text)
        doc = self.nlp(processed_text)
        
        # Filter meaningful tokens
        meaningful_tokens = []
        for token in doc:
            if (not token.is_stop and 
                not token.is_punct and 
                not token.is_space and 
                len(token.text) > 2 and
                token.pos_ in ['NOUN', 'ADJ', 'PROPN']):
                meaningful_tokens.append(token.lemma_)
        
        # Count frequency
        word_freq = Counter(meaningful_tokens)
        return [word for word, count in word_freq.most_common(top_n)]
    
    def calculate_similarity(self, resume_text: str, job_description: str) -> float:
        """Calculate similarity between resume and job description."""
        vectorizer = TfidfVectorizer(stop_words='english', max_features=1000)
        
        try:
            tfidf_matrix = vectorizer.fit_transform([
                self.preprocess_text(resume_text),
                self.preprocess_text(job_description)
            ])
            similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
            return float(similarity)
        except Exception as e:
            print(f"Error calculating similarity: {e}")
            return 0.0
    
    def analyze_resume_job_fit(self, resume_text: str, job_description: str) -> dict:
        """Comprehensive analysis of resume-job fit."""
        # Extract skills from both texts
        resume_skills = self.extract_skills(resume_text)
        job_skills = self.extract_skills(job_description)
        
        # Calculate skill matches
        tech_matched = set(resume_skills['technical']) & set(job_skills['technical'])
        soft_matched = set(resume_skills['soft']) & set(job_skills['soft'])
        
        tech_missing = set(job_skills['technical']) - set(resume_skills['technical'])
        soft_missing = set(job_skills['soft']) - set(resume_skills['soft'])
        
        # Calculate scores
        tech_score = len(tech_matched) / max(len(job_skills['technical']), 1) * 100
        soft_score = len(soft_matched) / max(len(job_skills['soft']), 1) * 100
        
        # Overall similarity
        similarity_score = self.calculate_similarity(resume_text, job_description) * 100
        
        # Weighted overall score
        overall_score = (tech_score * 0.4 + soft_score * 0.3 + similarity_score * 0.3)
        
        # Generate recommendations
        recommendations = self.generate_recommendations(
            tech_missing, soft_missing, overall_score
        )
        
        return {
            'overall_score': round(overall_score, 1),
            'technical_score': round(tech_score, 1),
            'soft_skills_score': round(soft_score, 1),
            'keyword_match_score': round(similarity_score, 1),
            'matched_skills': {
                'technical': list(tech_matched),
                'soft': list(soft_matched)
            },
            'missing_skills': {
                'technical': list(tech_missing),
                'soft': list(soft_missing)
            },
            'recommendations': recommendations,
            'resume_entities': self.extract_entities(resume_text),
            'job_entities': self.extract_entities(job_description)
        }
    
    def generate_recommendations(self, tech_missing: set, soft_missing: set, overall_score: float) -> list:
        """Generate improvement recommendations."""
        recommendations = []
        
        if overall_score < 50:
            recommendations.append("Consider significantly updating your resume to better align with this job description.")
        elif overall_score < 70:
            recommendations.append("Your resume shows good potential but could benefit from some improvements.")
        
        if tech_missing:
            top_missing_tech = list(tech_missing)[:5]
            recommendations.append(f"Consider highlighting these technical skills if you have them: {', '.join(top_missing_tech)}")
        
        if soft_missing:
            top_missing_soft = list(soft_missing)[:3]
            recommendations.append(f"Consider emphasizing these soft skills: {', '.join(top_missing_soft)}")
        
        if len(tech_missing) == 0 and len(soft_missing) == 0:
            recommendations.append("Excellent! Your resume aligns well with the job requirements.")
        
        recommendations.append("Quantify your achievements with specific numbers and metrics where possible.")
        recommendations.append("Tailor your resume summary to match the job description keywords.")
        
        return recommendations