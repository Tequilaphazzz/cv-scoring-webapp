import openai
import os
import streamlit as st
from parse_hh import extract_candidate_data, extract_vacancy_data
import requests
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Specify your OpenAI API key
openai.api_key = "OPENAI_API_KEY"  # Insert your API key here

SYSTEM_PROMPT = """
Evaluate the candidate and how well they fit this vacancy.

First, write a brief analysis explaining your evaluation.
Separately, assess the quality of the resume itself (is it clear what tasks the candidate faced and how they solved them?). This assessment should be factored into the final score - it is important for us to hire candidates who can clearly describe their work.
Finally, present the result as a score from 1 to 10.
""".strip()


def request_gpt(system_prompt, user_prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",  # Ensure you are using the correct model
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            max_tokens=1000,
            temperature=0,
        )
        return response.choices[0].message.content.strip() 
    except Exception as e:
        logger.error(f"Error calling OpenAI: {e}")
        return f"Error calling OpenAI: {e}"


def get_html_content(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        else:
            logger.error(f"Error retrieving HTML: {response.status_code}")
            logger.error(f"Response from server:\n{response.text}")  # Logging the HTML response
            return ''
    except Exception as e:
        logger.error(f"Error retrieving HTML: {e}")
        return ''


st.title("Candidate Resume Evaluation")

job_description_url = st.text_area("Enter the URL for the job description")
cv_url = st.text_area("Enter the URL for the candidate's resume")

if st.button("Evaluate Resume"):
    # Check if the URLs are valid
    if not (job_description_url.startswith("http://") or job_description_url.startswith("https://")):
        st.error("Please enter a valid URL for the job description.")
    elif not (cv_url.startswith("http://") or cv_url.startswith("https://")):
        st.error("Please enter a valid URL for the candidate's resume.")
    else:
        with st.spinner("Evaluating resume..."):
            # Get data from the vacancy and resume sites
            job_description_html = get_html_content(job_description_url)
            if not job_description_html:
                st.error("Failed to retrieve vacancy data.")
                st.stop()  # Stop execution

            job_description = extract_vacancy_data(job_description_html)

            cv_html = get_html_content(cv_url)
            if not cv_html:
                st.error("Failed to retrieve candidate resume data.")
                st.stop()  # Stop execution

            cv = extract_candidate_data(cv_html)

            st.write("Job Description:")
            st.write(job_description)
            st.write("Candidate Resume:")
            st.write(cv)

            # Formulate the request to GPT
            user_prompt = f"# VACANCY\n{job_description}\n\n# RESUME\n{cv}"
            response = request_gpt(SYSTEM_PROMPT, user_prompt)

            # Display the response
            st.write(response)