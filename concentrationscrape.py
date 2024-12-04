import requests
from bs4 import BeautifulSoup
import sqlite3

# URL of the Harvard concentrations page
url = "https://college.harvard.edu/academics/liberal-arts-sciences/concentrations"

# SQLite database file
sqlite_file = r"C:\Users\gubar\cs50-final-project-courseme\instance\courseme.sqlite"


# Function to scrape concentration titles from the webpage
def scrape_concentrations():
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        titles = []
        for title in soup.find_all("span", class_="title"):  # Adjust selector if needed
            clean_title = title.text.strip()  # Clean and normalize the title
            titles.append(clean_title)
        return titles
    else:
        print(f"Failed to fetch the webpage. Status code: {response.status_code}")
        return []

# Function to insert concentrations into the existing database table
def insert_concentrations_into_db(titles):
    # Connect to the SQLite database (no need to create the table since it exists)
    conn = sqlite3.connect(sqlite_file)
    cursor = conn.cursor()

    # Insert titles into the existing table
    for title in titles:
        cursor.execute("INSERT INTO concentrations (name) VALUES (?)", (title,))

    conn.commit()  # Save changes
    conn.close()  # Close the connection
    print(f"Inserted {len(titles)} concentrations into the database.")

# Main script execution
if __name__ == "__main__":
    # Step 1: Scrape the concentrations
    concentrations = scrape_concentrations()

    # Step 2: Insert into the existing database table
    if concentrations:
        insert_concentrations_into_db(concentrations)
    else:
        print("No concentrations were found to insert.")
