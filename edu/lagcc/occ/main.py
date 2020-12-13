
from edu.lagcc.occ.cls.search_criteria import SearchCriteriaPage
from datetime import datetime
from bs4 import BeautifulSoup

dt = datetime.now()

if __name__ == "__main__":

    term = "2021 Spring Term"
    term_value = "1212"
    subject_code = "VETE"
    session_code = "1"

    print(datetime.now()-dt)
    results = SearchCriteriaPage().search_criteria_response(term, term_value, subject_code, session_code)
    print(datetime.now()-dt)
    soup = BeautifulSoup(results.text, 'html.parser')
    class_names = soup.find_all("span", {"class": "cunylite_LABEL"})
    for i in class_names:
        print(i.text.strip())
    print(datetime.now()-dt)
