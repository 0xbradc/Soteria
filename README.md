# Soteria
This website was created as the final project for Harvard's CS50 in the fall of 2020 and was coded jointly with Jack Cogbill. I have made a [video demonstration](https://www.youtube.com/watch?v=86tvRU0rpKo) of the website and its common usage. 



# Compiling and Running Soteria

In order to compile and run our website, you will need to download a view dependencies. Assuming the user has Python3 installed (3.6+), these will get the application in working order. 

1. Installing Flask.
    ```
    % pip3 install flask
    ```
    
2. Installing CS50 SQL support.
    ```
    % pip3 install cs50
    ```
    
3. Installing requests.
    ```
    % pip3 install requests
    ```


# Technical Description

Soteria utilizes two APIs--Google Safe Browsing API and URLScan. Together, the site cross-checks security vulnerabilities from the URLs that are inputted.


# Website Description

When you first launch the Soteria website, you will be met with the user login page. If it is your first time using the website, there will
be a hyperlink below the login form that can bring you to the "Register" section of the website. You can then enter a desired username
and password for your account. If you leave any of these fields blank, your confimation doesn't match your password, or the username
you want to use is already in use, then you will be sent to an apology page that provides you with the error code, what the issue is, and a
wonderful picture of Brian Yu. Once you have registered for the website, then you will be sent to the login page again where you can log
into the website.

Once you have logged into the website, you will see another form where you can input a desired website to look up. This website search
function is one of the main purposes of Soteria: to analyze a website using multiple security APIs to evaluate if the given website poses
a cyber threat to its users. You can input any searchable website on the internet into our application on this page. However, if you input
an invalid website that Soteria catches, then you will be sent to the previously described apology page. Once you input a valid website,
then you will see a loading screen that will show the progress of the APIs. This loading screen currently has a 25-second timer to allow
for enough server response time. When the loading process is complete, you will be sent to the results page of the website that shows the
individual results of the APIs. If a single API deems a website invalid, then it will return a statement under its results section that
the website was not able to be used by the specific API.

If you look to the upper left hand corner of the website at any time, you will be a button that can extend a sidebar in the website.
This sidebar contains different links to parts of the website such as the register page, the home page, a page containing a
dictionary of possible vulnerabilities that you may encounter with a website, a page that contains a comprehensive user history overview
of the websites that you have previously searched and which (if any) vulnerabilities they present, a page that contains a txt file of our
sources we used when building the website, and finally a link to logout.

The aformentioned page that contains a dictionary of possible vulnerabilities is a page that simply contains hyperlinks to three different
pages in our website that give a description of different possible exploits a website may try to perform on a user. This dictionary can
also be accessed through a hyperlink at the bottom of the results page. This page represents another main goal of Soteria, education.
Through this page, we were able to educate our users on the many risks that they are taking on by using the internet. With our blue team
approach, we aimed to give the user better web safety and make them more aware of what threats look like.


