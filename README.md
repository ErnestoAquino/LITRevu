# LITRevu: A Book and Literature Review Platform
_Project 9 of the "Parcours Developper d'Application Python" series._

## Overview
LITRevu is a dynamic platform that empowers users to:
- **Request Reviews**: Create a request (billet) for book or literature article reviews.
- **Read and Publish Reviews**: Engage with the community by reading and sharing reviews on literature.
- **Stay Updated**: Keep track of reviews and billets from followed users in a real-time feed.
- **User Engagement**: Follow users, manage your billets and reviews, and interact with your followers.


## Technical Specifications
- **Framework**: Built on Django.
- **Database**: Local SQLite database (db.sqlite3 included in the repository).
- **Design**: User Interface in line with provided wireframes, with a clean and minimalistic design.
- **Code Standards**: Adheres to PEP8 guidelines.

## Installation

---

**Download the project:**
```
git clone https://github.com/ErnestoAquino/LITRevu.git
```

**Navigate to the directory:**
```
cd LITRevu
```

**Create a virtual environment:**
```
python3 -m venv env
```

**Activate the virtual environment:**
For macOS and Linux:
```
source env/bin/activate
```
For Windows:
```
env\Scripts\activate
```

**Install the requirements:**
```
pip install -r requirements.txt
```

**Start the server with:**
```
python litrevu/manage.py runserver
```

**Visit the following URL in your browser:**
[http://localhost:8000/](http://localhost:8000/)

**You can use the following credentials to log in:**
- **Username:** anabantha
- **Password:** N5*M-zARN.b6aqw

---


## Reports:

The security of the application has been analyzed using the Safety and Bandit tools. We've also used Flake8 to ensure the code complies with PEP 8 style standards.

**To generate a new Bandit report, you can use the following command:**
```
bandit -r litrevu/ -o analysis_reports/report_bandit.txt -f txt
```
This will produce a new report located in the analysis_reports folder named report_bandit.txt.

**For a new Safety report, use the command below:**
```
safety check -r requirements.txt --full-report > analysis_reports/report_safety.txt
```
This will generate a new report in the analysis_reports folder named report_safety.txt.

**You can analyze the code using Flake8 with:**
```
flake8 litrevu/
```

**Or generate a new report with:**
```
flake8 litrevu > analysis_reports/report_flake8.txt
```
However, consider that the file will be empty if there are no warnings.