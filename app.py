from flask import Flask, request, jsonify
from flask_cors import CORS
import os, json
from pyresparser import ResumeParser

app = Flask(__name__)
CORS(app)

# Configure the upload folder
DEF_UPLOAD = 'uploads/'
app.config['UPLOAD_FOLDER'] = DEF_UPLOAD

# File upload endpoint
@app.route('/upload', methods=['POST'])
def upload():
    if 'resume' not in request.files:
        return jsonify({'error': 'No file uploaded.'}), 400

    resume = request.files['resume']

    if resume.filename == '':
        return jsonify({'error': 'Invalid file name.'}), 400

    # Save the uploaded file
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], resume.filename)
    resume.save(file_path)

    # Resume Parsing Logic
    data = ResumeParser(file_path).get_extracted_data()
    # Create .json file
    base_filename = os.path.splitext(os.path.basename(file_path))[0]
    output_file_path = f'{base_filename}.json'

    with open(DEF_UPLOAD+output_file_path, 'w') as output_file:
        json.dump(data, output_file)

    # Determine file extension
    file_extension = resume.filename.rsplit('.', 1)[1].lower()

    if file_extension in ['pdf', 'docx']:
        # Extracted resume data/keywords can be put here to send over...
        resume_data = {'name': 'John Doe', 'email': 'johndoe@example.com', 'skills': ['Python', 'JavaScript']}
        
        # We will send this over to render on the client-side in this format OK
        response_data = {
            'results': [
                {
                    'id': 1,
                    'title': 'Software Engineer',
                    'company': 'ABC Inc.',
                    'description': 'Lorem ipsum dolor sit amet.',
                    'joblink': 'https://sg.linkedin.com/jobs/view/full-stack-developer-at-capgemini-3615331602?refId=8YO9aiK%2BimUDH%2FPStwJj1Q%3D%3D&trackingId=SQ8UmzgL1M0%2FvEk18QxIxg%3D%3D&position=14&pageNum=0&trk=public_jobs_jserp-result_search-card',
                    'compatibility': 80
                },
                {
                    'id': 2,
                    'title': 'Frontend Developer',
                    'company': 'XYZ Corp.',
                    'description': 'Lorem ipsum dolor sit amet.',
                    'joblink': 'https://sg.linkedin.com/jobs/view/full-stack-developer-at-capgemini-3615331602?refId=8YO9aiK%2BimUDH%2FPStwJj1Q%3D%3D&trackingId=SQ8UmzgL1M0%2FvEk18QxIxg%3D%3D&position=14&pageNum=0&trk=public_jobs_jserp-result_search-card',
                    'compatibility': 90
                }
            ]
        }

        # Add the resume data to the response data
        response_data['resume_data'] = resume_data
        
        # Send the response back to the client-side
        return jsonify(response_data)
    
    else:
        return jsonify({'error': 'Invalid file type. Only PDF and DOCX files are allowed.'}), 400

# Run the server
if __name__ == '__main__':
    app.run(port=3001)
