import fitz
import re
import sqlite3

# References
# - Used GPT 4o to help me learn and work with PyMuPDF

# Path to the Harvard Concentrations Handbook PDF to scrape the secondaries
pdf_path = "scrape/fields.pdf"

# Path to my SQLite database (might need to change if on a different computer)
sqlite_file = r"C:\Users\gubar\cs50-final-project-courseme\instance\courseme.sqlite"

# Typical lowercase exceptions to clean up the secondary name
lowercase_exceptions = {"and", "or", "the", "for", "in", "on", "of", "to", "by", "a", "an", "nor", "but", "with"}

# Properly capitalizes the secondary title
def capitalize_title(title):
    # Splits the secondary title into separate words
    words = title.split()
    
    # Capitalize each word, but leaves the exceptions in lowercase
    capitalized_title = " ".join([word.capitalize() if word.lower() not in lowercase_exceptions else word.lower() for word in words])
    
    return capitalized_title

conn = sqlite3.connect(sqlite_file)
cursor = conn.cursor()

# Opens up the PDF file
doc = fitz.open(pdf_path)

# Extracts the text from the PDF
full_text = ""
for page_num in range(doc.page_count):
    page = doc.load_page(page_num)
    full_text += page.get_text()

# Start and stop markers to show where the secondary titles are in the PDF
start_marker = "SECONDARY FIELDS"
end_marker = "CERTIFICATE FOR CIVIC ENGAGEMENT"

start_index = full_text.find(start_marker)
end_index = full_text.find(end_marker)

if start_index != -1 and end_index != -1:
    section_text = full_text[start_index + len(start_marker):end_index].strip()

    lines = section_text.split("\n")

    cleaned_lines = []
    for line in lines:
        line = re.sub(r'\d+', '', line)

        line = re.sub(r'\s*\.+\s*$', '', line)
        
        line = re.sub(r'\s+', ' ', line).strip()
        
        if line.strip():
            cleaned_lines.append(capitalize_title(line.strip()))

    for field in cleaned_lines:
        cursor.execute("SELECT * FROM secondaries WHERE name = ?", (field,))
        existing = cursor.fetchone()
        
        if not existing:
            cursor.execute("INSERT INTO secondaries (name) VALUES (?)", (field,))
    
    conn.commit()

    print("Secondary Fields inserted into the database.")

else:
    print("Markers not found in the document.")

conn.close()