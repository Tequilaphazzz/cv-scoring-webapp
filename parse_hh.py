# parse_hh.py

from bs4 import BeautifulSoup
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def extract_vacancy_data(html):
    soup = BeautifulSoup(html, "html.parser")

    def get_text_or_default(tag, default="Not specified"):
        return tag.get_text(strip=True) if tag else default

    # Extracting vacancy data
    title = get_text_or_default(soup.find("h1", {"data-qa": "vacancy-title"}), "Title not found")
    salary = get_text_or_default(soup.find("span", {"data-qa": "vacancy-salary"}), "Salary not specified")
    experience = get_text_or_default(soup.find("span", {"data-qa": "vacancy-experience"}), "Experience not specified")
    employment_mode = get_text_or_default(soup.find("p", {"data-qa": "vacancy-view-employment-mode"}), "Employment type not specified")
    company = get_text_or_default(soup.find("a", {"data-qa": "vacancy-company-name"}), "Company not specified")
    location = get_text_or_default(soup.find("p", {"data-qa": "vacancy-view-location"}), "Location not specified")
    description = get_text_or_default(soup.find("div", {"data-qa": "vacancy-description"}), "Description not specified")

    skills_tags = soup.find_all("span", {"data-qa": "bloko-tag__text"})
    skills = [skill.get_text(strip=True) for skill in skills_tags] if skills_tags else []

    # Formatting the string in Markdown
    markdown = f"""
# {title}

**Company:** {company}  
**Salary:** {salary}  
**Work Experience:** {experience}  
**Employment Type and Schedule:** {employment_mode}  
**Location:** {location}  

## Job Description
{description}

## Key Skills
- {'\n- '.join(skills)}
"""
    return markdown.strip()

def extract_candidate_data(html):
    soup = BeautifulSoup(html, 'html.parser')

    def get_text_or_default(tag, default="Not specified"):
        return tag.get_text(strip=True) if tag else default

    name = get_text_or_default(soup.find('span', {'data-qa': 'resume-personal-name'}), "Name not specified")
    gender_age = get_text_or_default(soup.find('span', {'data-qa': 'resume-personal-gender-age'}), "Gender and age not specified")
    location = get_text_or_default(soup.find('span', {'data-qa': 'resume-personal-address'}), "Location not specified")
    job_title = get_text_or_default(soup.find('span', {'data-qa': 'resume-block-title-position'}), "Position not specified")
    job_status = get_text_or_default(soup.find('span', {'data-qa': 'resume-block-job-search-status'}), "Status not specified")

    experiences = []
    experience_section = soup.find('div', {'data-qa': 'resume-block-experience'})
    if experience_section:
        experience_items = experience_section.find_all('div', {'data-qa': 'resume-block-item'})
        for item in experience_items:
            period = get_text_or_default(item.find('div', {'data-qa': 'resume-experience-dates'}))
            company = get_text_or_default(item.find('div', {'data-qa': 'resume-experience-company'}), "Company not specified")
            position = get_text_or_default(item.find('div', {'data-qa': 'resume-experience-position'}), "Position not specified")
            description = get_text_or_default(item.find('div', {'data-qa': 'resume-experience-description'}), "Description not specified")

            experiences.append(f"**{period}**\n\n*{company}*\n\n**{position}**\n\n{description}\n")
    else:
        experiences.append("Work experience not specified")

    skills_section = soup.find('div', {'data-qa': 'skills-content'})
    skills = [skill.get_text(strip=True) for skill in skills_section.find_all('span', {'data-qa': 'bloko-tag__text'})] if skills_section else []

    markdown = f"# {name}\n\n"
    markdown += f"**{gender_age}**\n\n"
    markdown += f"**Location:** {location}\n\n"
    markdown += f"**Position:** {job_title}\n\n"
    markdown += f"**Status:** {job_status}\n\n"
    markdown += "## Work Experience\n\n"
    for exp in experiences:
        markdown += exp + "\n"
    markdown += "## Key Skills\n\n"
    markdown += ', '.join(skills) + "\n"

    return markdown.strip()