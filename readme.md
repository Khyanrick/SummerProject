Resume Ranker - Python GUI Application
---------------------------------------

Description:
------------
This Python application provides a simple graphical interface to rank resumes (PDF format) against a provided job description. 
It uses natural language processing (NLP) techniques such as TF-IDF vectorization and cosine similarity to evaluate and 
score each resume based on its relevance to the job description.

Features:
---------
- GUI built with Tkinter for ease of use.
- Supports multiple PDF resume uploads.
- Displays ranked results with match percentages.
- Visualizes resume scores using a horizontal bar chart.
- Lightweight and does not require internet access after installation.

Requirements:
-------------
To run this application, the following Python packages must be installed:

1. PyPDF2           - for extracting text from PDF files
2. scikit-learn     - for TF-IDF vectorization and cosine similarity
3. matplotlib        - for generating the result chart

How to Use:
-----------
1. Run the Python script:

       python resume_ranker.py

2. Enter or paste the job description into the provided text area.
3. Click on the "📂 Upload Resumes and Rank" button to select one or more PDF files.
4. The application will analyze and display:
   - A ranked list of resumes with match percentages.
   - A bar chart showing the comparative scores.

Folder Structure:
-----------------
- resume_ranker.py        → Main Python script with GUI code
- readme.txt              → This instruction file
- [optional resumes]      → PDF files to test ranking

Notes:
------
- Ensure that all resumes are in standard PDF text format (not scanned images).
- This application is designed for academic and basic demonstration purposes.

