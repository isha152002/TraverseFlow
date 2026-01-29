# backend/services/document_processor.py
import PyPDF2
from docx import Document
import io
from typing import Optional

class DocumentProcessor:
    """Process different document formats"""
    
    @staticmethod
    def extract_text_from_pdf(file_content: bytes) -> str:
        """Extract text from PDF bytes"""
        try:
            pdf_file = io.BytesIO(file_content)
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n\n"
            
            return text.strip()
        except Exception as e:
            raise ValueError(f"Error processing PDF: {str(e)}")
    
    @staticmethod
    def extract_text_from_docx(file_content: bytes) -> str:
        """Extract text from DOCX bytes"""
        try:
            docx_file = io.BytesIO(file_content)
            doc = Document(docx_file)
            
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            
            return text.strip()
        except Exception as e:
            raise ValueError(f"Error processing DOCX: {str(e)}")
    
    @staticmethod
    def extract_text_from_txt(file_content: bytes) -> str:
        """Extract text from TXT bytes"""
        try:
            return file_content.decode('utf-8')
        except Exception as e:
            raise ValueError(f"Error processing TXT: {str(e)}")
    
    
    @staticmethod
    def process_file(file_content: bytes, file_type: str) -> str:
        """Process file based on type and returns file content"""
        try: 
            extension = file_type.lower().lstrip('.')

    
            if extension == 'pdf':
                return DocumentProcessor.extract_text_from_pdf(file_content)
        
            elif extension == 'docx':
                return DocumentProcessor.extract_text_from_docx(file_content)
        
            elif extension == 'txt':
                return DocumentProcessor.extract_text_from_txt(file_content)
        
            else:
                raise ValueError(f"Unsupported file type: {file_type}")
            
        except ValueError as ve:
            return f"Input error: {str(ve)}"
        
        except Exception as e:
            return f"Processing Error: An unexpected error occured while reading the file"
    
    