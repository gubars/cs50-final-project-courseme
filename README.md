# cs50-final-project-courseme
A website that provides you with a course schedule for next semester given the semester you're in, your concentration, and any preferences you have, built as the final project for CS50. Users can log in and receive a course schedule. Built with HTML, CSS, JavaScript, Bootstrap, Python, Flask, and SQL.

To use the website, register for an account, take the onboarding survey, and then receive your recommended courses! If you are unhappy with your recommended courses, then please refresh the page. Below is some information on how to navigate the repo incase there are any issues with the files or getting the webpage setup on your computer.

https://youtu.be/H-qGSnYY0tM

### .venv

In .venv is the virtual environment. In case this does not work, please consult the Flask documentation in terms of how to set this up

### courseme

In the courseme folder you can find all of the relevant files for the website. In static is the styles.css file, which has all of the relevant CSS for the dropdown. In templates, you can find the auth folder, courses folder, and layout.html. Layout.html is the layout that the other html files extend, and has the navbar with logged in/logged out functionality, as well as other css. 

In auth, you can find login.html and register.html, which are html files that handle logging in and registering. In courses, you have courses.html, index.html, and survey.html. Index.html is, of course, the main webpage of the website, and contains a basic card that redirects you to the other links in the website, and has a basic description of the website. Survey.html has the onboarding survey where the user inputs their information, and this information then updates the database for courses.html. Courses.html displays all of the courses that the website recommends, as well as allowing for functionality to reload the websites that have been recommended.

### instance

In the instance folder is the courseme.sqlite database, which is the SQLite 3 database that holds all of the relevant data.

### scrape

In the scrape folder is the relevant files used to scrape the data. Concentrationscrape.py has the python needed to scrape the concentrations from Harvard's website using BeautifulSoup. The json file and pdf are used to get information for the SQLite database. Insertcourses.py and secondaryscrape.py insert the courses into the database and scrape the secondaries to the database respectively.
