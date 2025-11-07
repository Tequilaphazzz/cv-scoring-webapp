# Candidate Resume Evaluation

This project is a **Streamlit** web application that evaluates how well a candidate's resume matches a specific job's requirements using OpenAI's **GPT-4** model.

## Functionality

  - **Data Input**: The user inputs the URL for the job description and the URL for the candidate's resume.
  - **Data Extraction**: The application retrieves the HTML content from the specified URLs using the `requests` library.
  - **Data Analysis**: Using the `BeautifulSoup` library, information from the job description and the candidate's resume is extracted.
  - **Match Assessment**: The application sends a request to the GPT-4 model to assess how well the candidate's resume matches the job description.
  - **Displaying Results**: The assessment results are displayed on the web interface using the Streamlit library.

## Technology Stack

  - **Python**
  - **Streamlit**
  - **BeautifulSoup** for HTML parsing
  - **OpenAI** for natural language processing
  - **Requests** for HTTP requests

## How to Use

1.  Install the required dependencies:

```bash
pip install -r requirements.txt
```

2.  Run the application:

```bash
streamlit run streamlit_app.py
```

3.  Enter the URL for the job description and the URL for the candidate's resume in the respective fields.
4.  Click the "Evaluate Resume" button to start the assessment process.

## Note

To use the candidate resume evaluation feature, an OpenAI API key is required, which you must provide in the `streamlit_app.py` file.