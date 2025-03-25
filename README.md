# Only Jobs

**Only Jobs** is a Django-based web application designed to create a trusted platform for job postings. It allows recruiters to upload authentic job posts while leveraging Large Language Models (LLM) to verify the authenticity of the uploader. Users can browse and view verified job listings with confidence.

This project is open-source and licensed under the [Apache 2.0 License](#license).

## Features

- **Job Posting**: Recruiters can upload job posts with details such as job title, description, location, and requirements.
- **Authenticity Check**: Utilizes a Large Language Model (LLM) to verify the authenticity of recruiters during the upload process.
- **Job Viewing**: Users can browse and view a curated list of verified job postings.
- **Database**: Uses Microsoft SQL Server (MSSQL) to securely store authentication details and job post data.
- **Logging**: Implements Python's logging module for troubleshooting and monitoring application behavior.
- **Scalable**: Built with Django, making it easy to extend and maintain.

## Tech Stack

- **Framework**: Django
- **Database**: Microsoft SQL Server (MSSQL)
- **Language**: Python
- **Logging**: Python Logging Module
- **Authenticity Verification**: Large Language Model (LLM) integration
- **License**: Apache 2.0

## Installation

### Prerequisites

- Python 3.8 or higher
- Django 4.x
- Python Gmail Module
- MSSQL Server
- Python packages (listed in `requirements.txt`)
- (Optional) Virtual environment

### Steps

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/only-jobs.git
   cd only-jobs
   Set Up a Virtual Environment (optional but recommended):
   python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate

    **Install Dependencies:**
    pip install -r requirements.txt

    python manage.py makemigrations
    python manage.py migrate

    python manage.py runserver

Open your browser and navigate to http://127.0.0.1:8000/ to see the app in action.

## Usage
- Register as a Recruiter: Create an account to start uploading job posts.
- Upload a Job: Submit job details; the LLM will verify your authenticity.
- Browse Jobs: View a list of verified job postings as a user.

## Future Enhancements
- Add user authentication for job seekers.
- Implement advanced search and filtering for job posts.
- Integrate email notifications for new job postings.
- Enhance LLM accuracy for authenticity checks.

## Contribution

Contributions are welcome! Fork this repository, submit pull requests, or report issues. Help improve functionality and make the system more robust.

## License

This project is licensed under the [Apache](https://www.apache.org/licenses/LICENSE-2.0) License. See the LICENSE file for details.

## Contact

For questions, suggestions, or support, reach out at 
- **sk0551460@gmail.com** 
- **shivam.hireme@gmail.com**.

## Support the Project

Help support continued development and improvements:

- **Follow on LinkedIn**: Stay connected for updates – [LinkedIn Profile](https://www.linkedin.com/in/shivam-hireme/)
- **Buy Me a Coffee**: Appreciate the project? [Buy Me a Coffee](https://buymeacoffee.com/shivamshane)
- **Visit my Portfolio**: [Shivam's Portfolio](https://shivam-portfoliio.vercel.app/)
