from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from datetime import datetime
import os

class ReportGenerator:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.setup_custom_styles()
    
    def setup_custom_styles(self):
        """Setup custom paragraph styles."""
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            textColor=colors.HexColor('#2563EB')
        ))
        
        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=self.styles['Heading2'],
            fontSize=16,
            spaceAfter=12,
            textColor=colors.HexColor('#1F2937')
        ))
        
        self.styles.add(ParagraphStyle(
            name='ScoreText',
            parent=self.styles['Normal'],
            fontSize=14,
            spaceAfter=6
        ))
    
    def create_score_table(self, analysis_data: dict) -> Table:
        """Create a table showing analysis scores."""
        data = [
            ['Metric', 'Score', 'Rating'],
            ['Overall Match', f"{analysis_data['overall_score']}%", self.get_rating(analysis_data['overall_score'])],
            ['Technical Skills', f"{analysis_data['technical_score']}%", self.get_rating(analysis_data['technical_score'])],
            ['Soft Skills', f"{analysis_data['soft_skills_score']}%", self.get_rating(analysis_data['soft_skills_score'])],
            ['Keyword Match', f"{analysis_data['keyword_match_score']}%", self.get_rating(analysis_data['keyword_match_score'])]
        ]
        
        table = Table(data, colWidths=[2*inch, 1*inch, 1.5*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3B82F6')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        return table
    
    def get_rating(self, score: float) -> str:
        """Convert numeric score to rating."""
        if score >= 80:
            return "Excellent"
        elif score >= 70:
            return "Good"
        elif score >= 60:
            return "Fair"
        elif score >= 50:
            return "Poor"
        else:
            return "Very Poor"
    
    def create_skills_section(self, matched_skills: dict, missing_skills: dict) -> list:
        """Create skills analysis section."""
        elements = []
        
        # Matched Skills
        elements.append(Paragraph("Matched Skills", self.styles['SectionHeader']))
        
        if matched_skills['technical']:
            elements.append(Paragraph("<b>Technical Skills:</b>", self.styles['Normal']))
            skills_text = ", ".join(matched_skills['technical'])
            elements.append(Paragraph(skills_text, self.styles['Normal']))
            elements.append(Spacer(1, 6))
        
        if matched_skills['soft']:
            elements.append(Paragraph("<b>Soft Skills:</b>", self.styles['Normal']))
            skills_text = ", ".join(matched_skills['soft'])
            elements.append(Paragraph(skills_text, self.styles['Normal']))
            elements.append(Spacer(1, 12))
        
        # Missing Skills
        elements.append(Paragraph("Areas for Improvement", self.styles['SectionHeader']))
        
        if missing_skills['technical']:
            elements.append(Paragraph("<b>Missing Technical Skills:</b>", self.styles['Normal']))
            skills_text = ", ".join(missing_skills['technical'])
            elements.append(Paragraph(skills_text, self.styles['Normal']))
            elements.append(Spacer(1, 6))
        
        if missing_skills['soft']:
            elements.append(Paragraph("<b>Missing Soft Skills:</b>", self.styles['Normal']))
            skills_text = ", ".join(missing_skills['soft'])
            elements.append(Paragraph(skills_text, self.styles['Normal']))
        
        return elements
    
    def generate_report(self, analysis_data: dict, filename: str, job_title: str, output_path: str) -> str:
        """Generate comprehensive PDF report."""
        doc = SimpleDocTemplate(output_path, pagesize=letter)
        elements = []
        
        # Title
        title = Paragraph("Resume Analysis Report", self.styles['CustomTitle'])
        elements.append(title)
        elements.append(Spacer(1, 20))
        
        # Basic Info
        info_text = f"""
        <b>Resume:</b> {filename}<br/>
        <b>Job Title:</b> {job_title}<br/>
        <b>Analysis Date:</b> {datetime.now().strftime('%B %d, %Y')}<br/>
        """
        elements.append(Paragraph(info_text, self.styles['Normal']))
        elements.append(Spacer(1, 20))
        
        # Scores Table
        elements.append(Paragraph("Analysis Summary", self.styles['SectionHeader']))
        score_table = self.create_score_table(analysis_data)
        elements.append(score_table)
        elements.append(Spacer(1, 20))
        
        # Skills Analysis
        skills_elements = self.create_skills_section(
            analysis_data['matched_skills'],
            analysis_data['missing_skills']
        )
        elements.extend(skills_elements)
        elements.append(Spacer(1, 20))
        
        # Recommendations
        elements.append(Paragraph("Recommendations", self.styles['SectionHeader']))
        for i, recommendation in enumerate(analysis_data['recommendations'], 1):
            rec_text = f"{i}. {recommendation}"
            elements.append(Paragraph(rec_text, self.styles['Normal']))
            elements.append(Spacer(1, 6))
        
        # Build PDF
        doc.build(elements)
        return output_path