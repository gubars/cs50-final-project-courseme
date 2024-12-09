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

survey() is a much more complicated function, with a route to "/survey" naturally, and handles all of the survey functionality that allows the users relevant data to be inserted into the database. First, we get the users id as well as form a connection with the database. We then receive a list of all the concentrations, and a list of all the secondaries. Then, under a POST request method, we obtain all of the information from the form, validate our form fields, convert the "want_x" to booleans, and attempt to insert into the profiles table. After the data has been inserted into the profiles table, we then redirect to courses.html.

### parse_course_code

parse_course_code(catalog_number) was made quite late in the design process. I needed a function that could test if a person who is taking 22A would be recommended 22B. So I initially tried to use the previous split functionality to seperate this into a number, and a letter. However, this did not work, so I asked GPT-4o, and it recommended me to use re and match. From here, I then had from each catalog number a number and some letters, which I could then use to detect sequential courses.

### time_to_datetime

This was a function that just converted a time string in meeting patterns to a datetime object, which was useful for checking if times overlapped and whatnot.

### check_time_overlap

This function converted all of the time strings into datetimes and then returned a boolean as to whether the times overlapped or not. 

### course_meets_on_same_day_and_no_overlap

This function first detected if there were "common days" between each day, and if there are, then they checked if there was an overlap. If there was an overlap, using the check_time_overlap function, then it would return True. If not, it returns false, as there was no overlap on the day. If there were no common days, then it returns false anyways because it is impossible for them to overlap on different days.

### courses

courses() handles everything for courses.html. When I was originally thinking about the structure of my project, I was planning on having the algorithm separate to courses(), however I felt that given the complexity of my algorithm, it would make the most sense both complexity and time wise to have it in courses(). courses() gets all of the information from "profile" and then uses this information to assign a "course_score" to each course as the program iterates through the datebase. First, courses() gets the course ids from the courses that the user has completed, as well as additional details about the courses that the user has completed. If the user submits some number of courses that they want, then we also get all courses, randomizing the order of these each time to ensure there is some variety. I also have a flag, gened_selected, which allows us to only pick one gened. There is first an initial filtration process, with filtering out courses that the user has completed, 9ams if they dont want them, geneds if they dont want them, and graduate level courses if they dont want them. From here, a course_score is initialized. From here, we start to boost the score if they havent taken courses in their intended concentration, if its the same subject as their concentration, etc. There is also some additional functionality that boosts courses that are sequential (eg CS50 to CS51, CS61, CS161) as well as courses that are sequential by letter (eg Math 22A, 22B, 25A, 25B, Physics 15A, 15B, 15C, Ec10A, Ec10B, etc.). This means that the algorithm is ultimately optimized for people who are on some sort of course track, however there is more room to improve regarding making these courses actually optimal or not. From here, we sort the corses, filter out overlapping courses, and then filter out by the number of courses that the user wants!

### search_courses_route

This function receives a query, searches for courses using the search_courses function, converts to a list of dictionaries, and then uses jsonify() to convert it to a JSON for the client. Using JSON was recommended by GPT-4o and CoPilot, and I had no idea how to implement this with the JS in survey.html, so I used the JS and JSON documentation as well as GPT to help me learn and implement this.

# auth.py

This followed a very similar structure to the Flask documentation in terms of getting login.html and register.html setup.

### register

This is a classic register function, with a password and confirmation for said password. After all the checks, we generate a hash using the werkzeug.security library, then insert into the database as usual.

### login

This function allows the user to, naturally, login. It gets the username, password, checks if they are in the database, and if they are, we set the session id to the users id, and we go to index.

### load_logged_in_user

This function provides the implementation to have conditionals like if g.user to check if a logged in or not. Essentially, it sets up g.user, which was often used to get the users id, or to check if they were logged in or not on the HTML pages.

### logout

This function just clears the session to make sure that the user is no longer logged in, and then redirects the user to index, where they are of course, logged out.

### login_required

This function allows for the functionality to call login_required for pages like survey and courses. This is directly from the Flask documentation.

# __init__.py

This entirely follows from the flask documentation. It creates the app, has a test page, imports the database, imports auth, imports courses, and then returns the app.

# templates

This folder contains all of the relevant HTML files used in this webpage, each under a specific folder, but layout.html is outside of this folder.

### layout.html

When it came to designing the general layout of the website, I knew that using Bootstrap would make this process as easy as possible. I started with a general dynamic navbar that changed as to whether you were logged in or logged out. There was also a general section for the flashed messages, and a block to contain the main section of the html. I went with a red and black colour scheme to easily integrate with Bootstrap, as well as matching the CS50 and Harvard general colour scheme.

## auth

Under the auth folder, we have both login.html and register.html. 

### login.html

This is a very basic login.html page, of course extending layout.html, having a title of Log In, and having a form to input a username and password, which then links to auth.py and login().

### register.html

This is also a very basic register.html page, extending layout.html, having a title of Register, and having a form to input a username, password, and confirmation, then linking to auth.py and register().

## courses

The courses folder contains courses.html, index.html, and survey.html. These are the main HTML pages of the project, as they contain the survey, course recommendation page, as well as the homepage, index.

### courses.html

This is a pretty simple HTML file, having a card with a general message telling the user thanks for filling out the survey, as well as some additional information on how to use the courses page. Underneath, depending on how many courses were recommended (how many the users wanted), a card is created for each course, that contains the courses description, catalognumber, title, and description. From here, the user can reload the page to generate new courses. The cards are made with a basic for loop, and the row dimension dynamically changes with the row-cols-md-{{ num_courses_want  }} allowing for the class to dynamically change with the number of classes that the user wants to take next semester.

### index.html

index.html is a little bit more complicated. Of course, the html file extends layout.html, with a block title of "Index". If the user is logged in (if g.user) then they see a message that welcomes them with their username, a message that thanks them, and two buttons that link to the onboarding survey, and the recommended courses page. If the user is not logged in, then there is a more general recommendation to the website, with two buttons that link to either registering a new account, or logging into an existing account.

### survey.html

When it came to making survey.html, I knew I wanted to integrate Bootstraps cards to implement each section of the survey/form. I then used the classes to make the borders for each card seamless, so the inputs looked like you were typing directly into the card, and made the overall survey a lot more clean in my opinion. I used concentrationslist and secondarieslist in a for loop to generate a list of all concentrations and a list of all secondaries so that the user can select from them. I then added some JavaScript functionality so that when a user selected their concentration type, it would create a new section of the card for the second concentration, or a new section of the card for their secondary. I also wanted functionality that could dynamically create semester cards depending on how many semesters the user inputs. I used JavaScript and help from GPT and CoPilot to solve this issue, creating a function that would create a new card, add 4 courses by default using a for loop, add search functionality to each one, and add a button to add extra courses on the bottom of each card. This button called a function to add a course, which essentially had very similar functionality to the card creating function, except I only had to create a "li" element. For each course, I needed search functionality that would search directly from the database that I had setup earlier. With the help of GPT and CoPilot, I set up a dropdown menu that could have an input (query) that would be fed into the search_courses function, receive an output, and then display the first 5 of these outputs, dynamically changing when necessary. After this, I then fetched the input to the number of courses wanted section that would dynamically create the relevant number of semester cards. I also ended up having a problem with some inputs like "Math 22" not appearing, so I added a note at the top of the page to warn anyone of this issue.

# static

This contains styles.css, my own custom CSS.

### styles.css

This mainly affects survey.html, as styles.css is entirely to do with the dropdown that appears in survey.html and how that dropdown looks, as I had a lot of problems with making not only the dropdown look good, but also make the dropdown appear in the first place. The CSS adds a white background to the dropdown with black font text, and when hovering over the dropdown, it goes grey to show that it can be selected.