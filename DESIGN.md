# scrape

When it came to gaining the data for scraping, I consulted GPT-4o and CoPilot to help me use BeautifulSoup and PyMuPDF. I used BeautifulSoup to scrape all of the concentration names, and this is because I knew that these were easy to access with just HTML elements, so using BeautifulSoup made the most sense. I used PyMuPDF to scrape the secondary names, as these were only found in a PDF from the Harvard Concentrations handbook, so I used PyMuPDF to scrape all of these. For the courses, I initially tried to use Selenium, however I had some problems with these, so I asked for some help on how to do this. Thankfully, I got linked to a repo that already had all of the courses in JSON format, so I could ask GPT to help me to convert this and insert this into my SQLite database. After this, I had all of my data scraped and inserted into my database.

# schema.sql

In schema.sql, I followed the Flask documentation for setting up schema.sql in a clean way. First, I started with planning all of my relevant tables that I would need, trying to separate tables as much as possible to create relational databases that would become easier to use later on. For example, I started with courses and meeting patterns merged together, but this came to be difficult when I was implementing courses.py, so I separated them and used an id to relate them together. I repeated this for a lot of the other tables. 

# db.py

This python file has the relevant scripts to setup the database, and create connections to the database through get_db(). Initially, I only had what the Flask documentation recommended, however, when I was developing survey.py, I learned that I would need a search_courses(query) function. Hence, I added one, using GPT to help me work with these queries that were in the survey.html file, and then use these queries to provide an output for relevant courses for the user to take.

# courses.py

This was definitely the hardest to implement in this entire project, and it broke many times when I tried to submit, so there are still areas that could have improvement. This file handles everything in the courses folder, as in courses.html, index.html, and survey.html.

### index

index() is a very simple function, and just renders the template with a route to "/". This is typical of an index function, and I tried to make sure everything was outside of this main homepage to keep the website as clean and simple as possible.

### survey

survey() is a much more complicated function, and handles all of the survey functionality that allows the users relevant data to be inserted into the database. First, we get the users id as well as form a connection with the database. We then receive a list of all the concentrations, and a list of all the secondaries. Then, under a POST request method, we obtain all of the information from the form, validate our form fields, convert the "want_x" to booleans, and attempt to insert into the profiles table. After the data has been inserted into the profiles table, we then redirect to courses.html.

# auth.py

# __init__.py

# templates

## auth

### login.html

### register.html

## courses

### courses.html

### index.html

index.html is a little bit more complicated. Of course, the html file extends layout.html, with a block title of "Index". If the user is logged in (if g.user) then they see a message that welcomes them with their username, a message that thanks them, and two buttons that link to the onboarding survey, and the recommended courses page. If the user is not logged in, then there is a more general recommendation to the website, with two buttons that link to either registering a new account, or logging into an existing account.

### survey.html

# static