def github() -> str:
    """
    my github repo
    """

    return "https://github.com/nandsra21/Econ481/blob/main/Problem_Set_5.py"

import requests
from bs4 import BeautifulSoup

def scrape_code(lecture_url):
    response = requests.get(lecture_url, headers={'Accept-Encoding': 'utf-8'})
    
    soup = BeautifulSoup(response.content, 'html.parser')

    code_snippets = soup.find_all('code')

    code_lines = []
    for code_snippet in code_snippets:
        lines = code_snippet.get_text().split('\n')
        lines = [line.strip() for line in lines if line.strip() and not line.strip().startswith('%')]
        code_lines.extend(lines)

    formatted_code = '\n'.join(code_lines)

    return formatted_code

lecture_url = "https://lukashager.netlify.app/econ-481/01_intro_to_python"
code = scrape_code(lecture_url)

lecture_url = "https://lukashager.netlify.app/econ-481/02_numerical_computing_in_python"
code = scrape_code(lecture_url)

lecture_url = "https://lukashager.netlify.app/econ-481/05_web_scraping"
code = scrape_code(lecture_url)


