import fitz  # PyMuPDF
import re  # For regex-based text cleaning
import sqlite3  # For interacting with SQLite

pdf_path = "fields.pdf"  # Replace with the correct path
sqlite_file = r"C:\Users\gubar\cs50-final-project-courseme\instance\courseme.sqlite"

# List of words to keep lowercase, typically short words in titles
lowercase_exceptions = {"and", "or", "the", "for", "in", "on", "of", "to", "by", "a", "an", "nor", "but", "with"}

# Function to properly capitalize the title
def capitalize_title(title):
    # Split the title into words
    words = title.split()
    
    # Capitalize each word, but leave exceptions in lowercase
    capitalized_title = " ".join([word.capitalize() if word.lower() not in lowercase_exceptions else word.lower() for word in words])
    
    return capitalized_title

# Connect to the SQLite database
conn = sqlite3.connect(sqlite_file)
cursor = conn.cursor()

# Open the PDF file
doc = fitz.open(pdf_path)

# Extract all the text from the PDF
full_text = ""
for page_num in range(doc.page_count):
    page = doc.load_page(page_num)  # Load the page
    full_text += page.get_text()  # Append text from the current page

# Define the start and stop markers
start_marker = "SECONDARY FIELDS"
end_marker = "CERTIFICATE FOR CIVIC ENGAGEMENT"

# Find the start and end positions of the section
start_index = full_text.find(start_marker)
end_index = full_text.find(end_marker)

# Check if both markers are found
if start_index != -1 and end_index != -1:
    # Extract the content between the markers
    section_text = full_text[start_index + len(start_marker):end_index].strip()

    # Optionally, split the content into lines (if needed)
    lines = section_text.split("\n")

    # Clean the text: Remove dots, random numbers, and extra spaces between lines
    cleaned_lines = []
    for line in lines:
        # Remove random numbers (e.g., page numbers or any isolated numbers) using regex
        line = re.sub(r'\d+', '', line)  # Removes all digits
        
        # Remove trailing dots and sequences of dots followed by space (e.g., ".......... ")
        line = re.sub(r'\s*\.+\s*$', '', line)  # Remove trailing dots and spaces after them
        
        # Remove extra spaces between words
        line = re.sub(r'\s+', ' ', line).strip()  # Replace multiple spaces with one space
        
        # If the line is non-empty after cleaning, capitalize it and add to the list
        if line.strip():
            cleaned_lines.append(capitalize_title(line.strip()))

    # Insert the cleaned secondary fields into the existing table
    for field in cleaned_lines:
        # Check if the field already exists in the database to avoid duplicates
        cursor.execute("SELECT * FROM secondaries WHERE name = ?", (field,))
        existing = cursor.fetchone()
        
        if not existing:  # Only insert if the field does not already exist
            cursor.execute("INSERT INTO secondaries (name) VALUES (?)", (field,))
    
    # Commit the changes and close the connection
    conn.commit()

    print("Secondary Fields inserted into the database.")

else:
    print("Markers not found in the document.")

# Close the database connection
conn.close()
