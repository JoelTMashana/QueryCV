# Project Name

## System Requirements
- Windows: Visual C++ Redistributable for Visual Studio 2015-2022 (x64 version).
- Python 3.9.1 or higher.

## Installation
1. Clone the repository: `git clone <repository-url>`
2. Navigate to the project directory: `cd <project-name>`
3. Install dependencies: `pip install -r requirements.txt`
   - Note: If you encounter issues with `bcrypt`, install it using `pip install bcrypt==3.1.7`.

## Running the Application
- Start the server: `uvicorn main:app --reload`
- Access the application at `http://localhost:8000`

## Testing
- Set environment var TESTING=1
- For Unix systems TESTING=1 pytest
- Windows $env:TESTING = "1"  pytest
- $env:SECRET_KEY = "<seceret-key>"


## Contact
- For issues not covered in this guide, contact me at: `<joeltmashana@gmail.com>`

## Note to self
- Migrations 
- Create Migration Script: alembic revision --autogenerate -m "<Purpose of script>"
- Run the mgiration: alembic upgrade head
