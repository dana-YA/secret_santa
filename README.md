# Secret Santa Gift Exchange

## Overview
This is an application built to organize and manage Secret Santa gift exchanges. It allows users to:
- Add and manage participants.
- Set exclusion rules for participants.
- Generate random gift pairings while respecting exclusion rules.
- Track the history of past gift exchanges.

The application consists of:
- **Backend**: Built with Flask (Python) for handling API requests and business logic.
- **Database**: Uses SQLAlchemy for database interactions.

---

## Features
### Core Functionality
1. **Participant Management**:
   - Add Participants & Manage their Preferences 

2. **Create Secret Santa Events**:
   - Generate random pairings while respecting exclusions.
   - Ensure each participant gives and receives exactly one gift.

3. **History Tracking**:
   - Store results of previous gift exchanges.

---

## Technical Stack
- **Backend**: Flask (Python)
- **Database**: SQLAlchemy (SQLite/PostgreSQL)
- **API Documentation**: Swagger
- **Testing**: Unit tests with `unittest` and `unittest.mock`

---

## Setup Instructions

### Prerequisites
- Python 3.8+
- PostgreSQL (optional, SQLite is used by default)

### Backend Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/secret-santa-app.git
   cd secret-santa-app/backend

2. Create a virtual environment and install dependencies:


   ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    pip install -r requirements.txt

3. Create the database:
    
4. setup .env file

    ```bash
    SWAGGER_SCHEME=http
    JWT_KEY=
    DB_NAME=secret_santa_db
    DB_HOST=
    DB_USER=secret_santa_user
    DB_PASSWORD=
    DB_PORT=5432


5. Run your application
    ```bash
    export PYTHONPATH=. && flask run 

6. To view the APIs
    ```bash
    http://localhost:5000/api
    

7. To Run Tests
    ```bash
    python -m unittest discover -s tests


---

### **Pending Things to implement**
1. Database Versioning: Add Alembic for database schema migrations.
2. Infrastructure as Code: Use Terraform to manage AWS Elastic Beanstalk infrastructure.
3. CI/CD Pipeline: Implement GitLab CI with unit tests, Docker image creation, and deployment scripts.
4. Missing Features:
    - Add proper response Models that can be used in the frontend
    - Get All Events
    - User Management (PUT/DELET/GET User ,  Change Password, etc)
    - Complete CRUD operations (Edit Partificpants , Preferences)
    - Unit Test Coverage: Expand test coverage
    - Enhanced Matching Algorithm
    - Add more gifting preference: Prioritize gifting preferences.
    - Upload pariticpants via excel
    - Review DB Structure and add proper indexing
    - Frontend Development (Build with React.js and Vue framework with core functionality (Register, Login/Logout, Add Event, Add Participants, generate matched)
    - Email Notifications: Integrate email service for event updates and pairing assignments.
5. Add a monitoring Dashboard maybe via Grafana to monitor how well the app is doing (KPI Metrics) , and integrate it with AWS to monitor any server issues     

