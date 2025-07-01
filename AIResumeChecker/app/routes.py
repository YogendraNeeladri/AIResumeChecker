from flask import Blueprint, render_template, request, jsonify, send_file, flash, redirect, url_for
from werkzeug.utils import secure_filename
import os
from datetime import datetime
from app import db
from app.models import ResumeAnalysis
from app.resume_parser import ResumeParser
from app.nlp_analyzer import NLPAnalyzer
from app.report_generator import ReportGenerator

bp = Blueprint('main', __name__)

ALLOWED_EXTENSIONS = {'pdf', 'docx', 'doc'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.route('/')
def index():
    """Main page with upload form."""
    return render_template('index.html')

@bp.route('/analyze', methods=['POST'])
def analyze_resume():
    """Analyze uploaded resume against job description."""
    try:
        # Validate form data
        if 'resume' not in request.files:
            flash('No resume file uploaded', 'error')
            return redirect(url_for('main.index'))
        
        file = request.files['resume']
        job_title = request.form.get('job_title', '').strip()
        job_description = request.form.get('job_description', '').strip()
        
        if file.filename == '':
            flash('No file selected', 'error')
            return redirect(url_for('main.index'))
        
        if not job_title or not job_description:
            flash('Job title and description are required', 'error')
            return redirect(url_for('main.index'))
        
        if not allowed_file(file.filename):
            flash('Invalid file format. Please upload PDF or DOCX files only.', 'error')
            return redirect(url_for('main.index'))
        
        # Save uploaded file
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{timestamp}_{filename}"
        file_path = os.path.join('uploads', filename)
        file.save(file_path)
        
        # Parse resume
        resume_text, metadata = ResumeParser.parse_resume(file_path, filename)
        
        if not resume_text:
            flash(f"Error processing file: {metadata.get('error', 'Unknown error')}", 'error')
            os.remove(file_path)  # Clean up
            return redirect(url_for('main.index'))
        
        # Analyze with NLP
        analyzer = NLPAnalyzer()
        analysis_results = analyzer.analyze_resume_job_fit(resume_text, job_description)
        
        # Save to database
        analysis = ResumeAnalysis(
            filename=filename,
            job_title=job_title,
            job_description=job_description,
            resume_text=resume_text,
            overall_score=analysis_results['overall_score'],
            technical_skills_score=analysis_results['technical_score'],
            soft_skills_score=analysis_results['soft_skills_score'],
            keyword_match_score=analysis_results['keyword_match_score']
        )
        
        analysis.set_matched_skills(analysis_results['matched_skills'])
        analysis.set_missing_skills(analysis_results['missing_skills'])
        analysis.set_recommendations(analysis_results['recommendations'])
        analysis.set_extracted_entities(analysis_results['resume_entities'])
        
        db.session.add(analysis)
        db.session.commit()
        
        # Clean up uploaded file
        os.remove(file_path)
        
        return render_template('results.html', 
                             analysis=analysis, 
                             analysis_data=analysis_results)
    
    except Exception as e:
        flash(f'An error occurred during analysis: {str(e)}', 'error')
        return redirect(url_for('main.index'))

@bp.route('/download_report/<int:analysis_id>')
def download_report(analysis_id):
    """Generate and download PDF report."""
    try:
        analysis = ResumeAnalysis.query.get_or_404(analysis_id)
        
        # Prepare analysis data
        analysis_data = {
            'overall_score': analysis.overall_score,
            'technical_score': analysis.technical_skills_score,
            'soft_skills_score': analysis.soft_skills_score,
            'keyword_match_score': analysis.keyword_match_score,
            'matched_skills': analysis.get_matched_skills(),
            'missing_skills': analysis.get_missing_skills(),
            'recommendations': analysis.get_recommendations()
        }
        
        # Generate PDF
        report_generator = ReportGenerator()
        report_filename = f"resume_analysis_report_{analysis_id}.pdf"
        report_path = os.path.join('uploads', report_filename)
        
        report_generator.generate_report(
            analysis_data,
            analysis.filename,
            analysis.job_title,
            report_path
        )
        
        return send_file(report_path, as_attachment=True, download_name=report_filename)
    
    except Exception as e:
        flash(f'Error generating report: {str(e)}', 'error')
        return redirect(url_for('main.index'))

@bp.route('/history')
def analysis_history():
    """View analysis history."""
    analyses = ResumeAnalysis.query.order_by(ResumeAnalysis.created_at.desc()).limit(20).all()
    return render_template('history.html', analyses=analyses)

@bp.route('/api/analyze', methods=['POST'])
def api_analyze():
    """API endpoint for resume analysis."""
    try:
        data = request.get_json()
        resume_text = data.get('resume_text', '')
        job_description = data.get('job_description', '')
        
        if not resume_text or not job_description:
            return jsonify({'error': 'Resume text and job description are required'}), 400
        
        analyzer = NLPAnalyzer()
        results = analyzer.analyze_resume_job_fit(resume_text, job_description)
        
        return jsonify(results)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500