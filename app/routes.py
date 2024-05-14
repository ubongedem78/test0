from flask import render_template, request, jsonify, make_response
from app import app
from app.models import Attendance
from datetime import datetime
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
from flask import render_template


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/record_attendance', methods=['POST'])
def record_attendance():
    data = request.json
    name = data.get('name')
    id_number = data.get('id_number') 
    timestamp = datetime.now()

    if name and id_number:
        Attendance.record(name, id_number, timestamp)
        return jsonify({'message': 'Attendance recorded successfully'}), 201
    else:
        return jsonify({'error': 'Missing data'}), 400

@app.route('/attendance', methods=['GET'])
def view_attendance():
    attendance_data = Attendance.get_all()
    return jsonify(attendance_data), 200 

from flask import send_file

@app.route('/attendance/pdf')
def download_attendance_pdf():
    # Retrieve all attendance records from the database
    attendance_data = Attendance.get_all()

    # Prepare PDF data
    buffer = BytesIO()
    filename = f"attendance_{datetime.now().strftime('%Y-%m-%d')}.pdf"
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    table_data = [['Student Name', 'ID Number', 'Timestamp']]
    for record in attendance_data:
        table_data.append([record['name'], record['idNumber'], record['timestamp']])
    table = Table(table_data)
    table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                               ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                               ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                               ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                               ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                               ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                               ('GRID', (0, 0), (-1, -1), 1, colors.black)]))
    doc.build([table])

    # Create response
    response = make_response(buffer.getvalue())
    response.headers['Content-Disposition'] = f'attachment; filename="{filename}"'
    response.headers['Content-type'] = 'application/pdf'

    return response


@app.route('/record_new_attendance', methods=['DELETE'])
def record_new_attendance():
    # Delete all existing attendance records
    Attendance.delete_all()
    return jsonify({'message': 'Ready for New attendance record'}), 200