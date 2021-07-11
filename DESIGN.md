DESIGN.md Submission for Soteria

Overall:
    Our project was designed using many of the frameworks and technologies that the CS50 course introduced to us.
    It uses Flask, Jinja, HTML, CSS, JavaScript, JSON, SQL, and two APIs. We decided to use these frameworks/languages because we were
    most familiar with them after the weeks we learned them in CS50.

Flask:
    We utilized Flask to organize the flow and navigation of the site. Using distribution code from Week 9 Finance, we implemented a
    registration, login, and logout method with hashed passwords stored in an SQL database. Flask was useful because it opened many doors
    for our work with the data of the free APIs we pulled from. The dictionary and list datatypes of Python were especially useful in this.
    Flask was also useful for organizing our functions and utilizing the many quick methods of Python. Overall, we encountered little to
    no problems with Flask and enjoyed the error outputs it provided.

Jinja:
    We utilized Jinja for creating layout HTML files and for displaying information efficiently. In creating layout files, we were able to
    use the "extends" and "block" functions of Jinja to create files that were free from homogeneity. Our main layout file, layout.html,
    was used in all HTML files in order to create a consistent title bar, footer, content body, and drawer menu. We utilized a second
    layout file, dictionary_layout.html, that extends the original layout.html file while adding the links for our various pages of the
    vulnerability dictionary. We utilized block functions for displaying information. The "| safe" call within the {{}} elements was useful
    in directly displaying HTML code returned from various functions and/or APIs. We also utilized the for loop function of Jinja to display
    information of variable size, like with the User History page.

HTML:
    Our HTML was relatively straight forward but added many styling elements and small features to create a good looking user interface.
    One interesting element was the loading bar. This was done because the URLscan.io API requires ~25 seconds for a full response (detailed
    further in the "API" section below). It was challenge to create a loading bar that allowed the API calls to continue running in the
    background. Using the hidden tag of HTML, we hid information and ran the loading bar script while the Python was continuing to run in
    the background. Our HTML also includes the use of favicon to decorate the website a bit. We chose to use the shield emoji to convey
    the website"s protective nature. We also used a digital color meter to use the exact blue color of the shield.

CSS:
    A fair portion of our CSS was derived from the Week 9 Finance problem set. However, we also utilized CSS from other sources such as
    Stackoverflow.com and W3Schools.com. While our initial code featured a deep red color, we decided on a blue color scheme to convey the
    "blue team" mentality of the website. Variations of blue can be seen throughout the website. One important part of our CSS was the
    placement of items with respect to flexibility. It was challenging to get items to stay in the spot that we envisioned. One particularly
    difficult element of the site was the footer. We wanted to create a footer that sat at the bottom of the screen by default yet flexed if
    the screen featured more information. We were successful in using the "position" element with the attributes "relative" and "absolute"
    to accomplish this goal.

JavaScript:
    Our JavaScript usage was mainly for HTML elements involving animations. For our loading bar, we utilized a script that created a time
    interval, increased the width of the bar, set the percentage of loading, and more. It should be noted that the loading bar feature is
    not functional in the Safari browser, but is functional in the Google Chrome browser. Another use of JavaScript was with the drawer menu
    on the left side of the screen. Using starter code from W3Schools.com, we implemented a "checkNav()" function that opened and closed the
    menu in the correct way. Both scripts can be found in the <head> of the layout.html file.

JSON:
    JSON was very important for our API utilization. Both of our APIs outputted JSONs, so we became comfortable with taking that data
    and transforming it into readable and storable information. Python makes this process much easier than other languages, so this was just a
    matter of making sure that the current type and index was correct. Our helpers.py file was full of code that converted JSON information
    into Python lists and dictionaries.

SQL:
    SQL became an essential aspect in the Soteria website in terms of being able to store user information for the login and
    registration process and being able to effectively store a history of which websites users have searched for in the past.
    The SQL database in our program consists of five tables, three of which, "users", "websites", and "vulnerabilities", are specifically
    designed to store information on users, websites, and possible vulnerabilities to the user, respectively. The other two tables,
    "users_websites" and "websites_vulnerabilities" support two many-to-many relationships between the users and the different websites that
    they have previously looked up and between the different websites and any vulnerabilities that the APIs have tagged them with. By using a
    many-to-many relationship between the users, websites, and vulnerabilities, it prevents our website's database from creating duplicate
    information in the tables. This allows for more efficient data processing and faster load times.
    Specifically, we use SQL in the register() and login() functions of applications.py to access user information to make sure a username is not
    already in use or to confirm a user is entering the correct password (which is stored as a hash for security purposes) for their account.
    Another use of SQL code is found in the results() function of application.py. The results() function uses SQL SELECT calls to see if a
    website that the user has entered is already in the database, and if not it is entered into the database. It also makes the relationship
    between the user and the searched website in the users_websites table (many-to-many relationship) if it is not already present.
    Lastly, for the sake of optimization and better code readability, we created a function called connect() that is used twice in results().
    This function uses a series of SQL calls to see if the relationship between a given website and any vulnerabilities that the APIs have
    identified exists, and if it does not, then it adds it to its respective table. The connect() function streamlines the process of
    connecting vulnerabilities to websites so that if we decide to add more APIs in the future, all it takes is one more line of code to
    establish the relationship between the vulnerabilities that the new API identifies and a given website.

API:
    After researching various APIs for our specific use, we decided to use the Google Safe Browsing API and the API from URLScan.io. The Google
    API was extremely easy to use and did not present many problems for us. The URLScan API was more labor intensive than the Google one. It
    had a strange format and required over 20 seconds to load. Once it did finally compile the website security report together, it was in
    a JSON file that was thousands of lines. While the information was thorough, it was not useful with the exception of about 20 lines.
    However, we did appreciate that both APIs were free to use and have relatively large usage limits.

Optimization:
    We worked hard to create functions that were optimized for good peformance. In many cases we abstained from over-using standard function
    calls and SQL selections in pursuit of faster run time. While this may not be very important for a small-scale project, it will become
    more important as the amount of users, and therefore information, increases.

Error Checking:
    Throughout the project, we utilized the same "apology()" format as the Week 9 Finance pset. It is worth noting the exact picture we
    used for our apologies--it is very fun!This proved useful for certain mistakes that the user could make on the webpage. However, we
    decided to use more direct error coding for problems with out API. Using the try-exception format, we caught errors in the APIs and
    sent red error codes that were specific to that exact API. This was useful because it ensured that the failure of one API does not bring
    the program to a hault.

Citing Sources:
    On the left menu bar, we have included the navigation to a page for sources. After clicking on the available txt file, the user can
    view the plethora of sources we used throughout this project. This was done using a text file so that future iterations can add new
    sources.

Title Explanation:
    In exploring names for our website we wanted to convey protection from harm. After some research we found that the Greek god Soteria is
    the goddess of safety and salvation, deliverance, and preservation from harm. Her name flowed well and was simple, so we made
    the decision to use Soteria.
