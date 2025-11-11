"""
PDF generation service.
Following Single Responsibility Principle - handles PDF generation business logic only.
"""
from io import BytesIO
from typing import Dict, Any, List
from django.http import HttpResponse
import xhtml2pdf.pisa as pisa
from core.services.base import BaseService
from core.exceptions import RoutineGenerationError


class PDFGenerationService(BaseService):
    """
    Service for PDF generation operations.
    Following Single Responsibility Principle - handles PDF creation only.
    """
    
    def generate_pdf_from_schedule(self, schedule_data: Dict[str, Any]) -> BytesIO:
        """
        Generate PDF from schedule data.
        
        Args:
            schedule_data: Dictionary containing schedule information
            
        Returns:
            BytesIO object containing PDF data
            
        Raises:
            RoutineGenerationError: If PDF generation fails
        """
        try:
            schedule = schedule_data.get('schedule', [])
            
            # Generate HTML from schedule data
            html_content = self._generate_html(schedule)
            
            # Convert HTML to PDF
            result = BytesIO()
            pdf = pisa.pisaDocument(
                BytesIO(html_content.encode("UTF-8")),
                result
            )
            
            if pdf.err:
                self.log_error(f"PDF generation error: {pdf.err}")
                raise RoutineGenerationError("Error generating PDF")
            
            result.seek(0)
            return result
        except Exception as e:
            self.log_error("Error generating PDF", error=e)
            raise RoutineGenerationError(f"Failed to generate PDF: {str(e)}")
    
    def _generate_html(self, schedule: List[Dict[str, Any]]) -> str:
        """
        Generate HTML content from schedule data.
        
        Args:
            schedule: List of class schedule items
            
        Returns:
            HTML string
        """
        html = """
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>Class Routine</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    margin: 20px;
                }
                h1 {
                    text-align: center;
                    color: #333;
                }
                table {
                    width: 100%;
                    border-collapse: collapse;
                    margin-top: 20px;
                }
                th, td {
                    border: 1px solid #ddd;
                    padding: 8px;
                    text-align: left;
                }
                th {
                    background-color: #4CAF50;
                    color: white;
                }
                tr:nth-child(even) {
                    background-color: #f2f2f2;
                }
            </style>
        </head>
        <body>
            <h1>Class Routine</h1>
            <table>
                <thead>
                    <tr>
                        <th>Section</th>
                        <th>Department</th>
                        <th>Course</th>
                        <th>Room</th>
                        <th>Instructor</th>
                        <th>Day</th>
                        <th>Time</th>
                    </tr>
                </thead>
                <tbody>
        """
        
        for item in schedule:
            html += f"""
                    <tr>
                        <td>{item.get('section', 'N/A')}</td>
                        <td>{item.get('department', 'N/A')}</td>
                        <td>{item.get('course_name', 'N/A')} ({item.get('course_number', 'N/A')})</td>
                        <td>{item.get('room_number', 'N/A')} (Capacity: {item.get('room_capacity', 'N/A')})</td>
                        <td>{item.get('instructor_name', 'N/A')} ({item.get('instructor_uid', 'N/A')})</td>
                        <td>{item.get('meeting_day', 'N/A')}</td>
                        <td>{item.get('meeting_time', 'N/A')}</td>
                    </tr>
            """
        
        html += """
                </tbody>
            </table>
        </body>
        </html>
        """
        
        return html
    
    def create_pdf_response(self, schedule_data: Dict[str, Any], filename: str = 'routine.pdf') -> HttpResponse:
        """
        Create HTTP response with PDF content.
        
        Args:
            schedule_data: Dictionary containing schedule information
            filename: Name of the PDF file
            
        Returns:
            HttpResponse with PDF content
        """
        pdf_buffer = self.generate_pdf_from_schedule(schedule_data)
        
        response = HttpResponse(pdf_buffer.read(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        
        return response

