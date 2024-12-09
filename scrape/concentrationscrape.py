import requests
from bs4 import BeautifulSoup
import sqlite3

url = "https://college.harvard.edu/academics/liberal-arts-sciences/concentrations"

sqlite_file = r"C:\Users\gubar\cs50-final-project-courseme\instance\courseme.sqlite"

def scrape_concentrations():
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        titles = []
        for title in soup.find_all("span", class_="title"):
            clean_title = title.text.strip()
            titles.append(clean_title)
        return titles
    else:
        print(f"Failed to fetch the webpage. Status code: {response.status_code}")
        return []

def insert_concentrations_into_db(titles):
    conn = sqlite3.connect(sqlite_file)
    cursor = conn.cursor()

    for title in titles:
        cursor.execute("INSERT INTO concentrations (name) VALUES (?)", (title,))

    conn.commit()
    conn.close()
    print(f"Inserted {len(titles)} concentrations into the database.")

if __name__ == "__main__":
    concentrations = scrape_concentrations()

    if concentrations:
        insert_concentrations_into_db(concentrations)
    else:
        print("No concentrations were able to be inserted.")