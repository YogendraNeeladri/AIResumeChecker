import PyPDF2
import docx
import re
from typing import Optional, Tuple

class ResumeParser:
    @staticmethod
    def extract_text_from_pdf(file_path: str) -> Optional[str]:
        """Extract text from PDF file."""
        try:
            with open(file_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                text = ""
                for page in reader.pages:
                    text += page.extract_text() + "\n"
                return text.strip()
        except Exception as e:
            print(f"Error extracting PDF text: {e}")
            return None
    
    @staticmethod
    def extract_text_from_docx(file_path: str) -> Optional[str]:
        """Extract text from DOCX file."""
        try:
            doc = docx.Document(file_path)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text.strip()
        except Exception as e:
            print(f"Error extracting DOCX text: {e}")
            return None
    
    @staticmethod
    def extract_contact_info(text: str) -> dict:
        """Extract contact information from resume text."""
        contact_info = {}
        
        # Email extraction
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, text)
        contact_info['emails'] = emails
        
        # Phone number extraction
        phone_pattern = r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
        phones = re.findall(phone_pattern, text)
        contact_info['phones'] = [phone for phone in phones if phone]
        
        # LinkedIn profile extraction
        linkedin_pattern = r'linkedin\.com/in/[\w-]+'
        linkedin = re.findall(linkedin_pattern, text.lower())
        contact_info['linkedin'] = linkedin
        
        return contact_info
    
    @classmethod
    def parse_resume(cls, file_path: str, filename: str) -> Tuple[Optional[str], dict]:
        """Parse resume file and extract text and metadata."""
        file_extension = filename.lower().split('.')[-1]
        
        if file_extension == 'pdf':
            text = cls.extract_text_from_pdf(file_path)
        elif file_extension in ['docx', 'doc']:
            text = cls.extract_text_from_docx(file_path)
        else:
            return None, {'error': 'Unsupported file format'}
        
        if not text:
            return None, {'error': 'Could not extract text from file'}
        
        # Extract additional metadata
        contact_info = cls.extract_contact_info(text)
        metadata = {
            'contact_info': contact_info,
            'file_type': file_extension,
            'text_length': len(text)
        }
        
        return text, metadata