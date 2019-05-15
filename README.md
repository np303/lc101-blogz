

<!-- Need to use USERNAME instead EMAIL -->

<!-- login with nonexistant username redirects to login -->

<!-- login with bad pass tells them password is incorrect -->

For /login page:

<!-- User enters a username that is stored in the database with the correct password and is redirected to the /newpost page with their username being stored in a session. -->


<!-- User enters a username that is stored in the database with an incorrect password and is redirected to the /login page with a message that their password is incorrect. -->


<!-- User tries to login with a username that is not stored in the database and is redirected to the /login page with a message that this username does not exist. -->


<!-- User does not have an account and clicks "Create Account" and is directed to the /signup page. -->


For /signup page:

<!-- User enters new, valid username, a valid password, and verifies password correctly and is redirected to the '/newpost' page with their username being stored in a session. -->


<!-- User leaves any of the username, password, or verify fields blank and gets an error message that one or more fields are invalid. -->


<!-- User enters a username that already exists and gets an error message that username already exists. -->


<!-- User enters different strings into the password and verify fields and gets an error message that the passwords do not match. -->


<!-- User enters a password or username less than 3 characters long and gets either an invalid username or an invalid password message. -->

<!-- Now that users can login, we want to allow them to log out. To do so, you'll implement the same functionality you did in Get It Done and you'll add a link to your navigation in base.html with href="/logout" and a route handler function to main.py to handle that request. It should delete the username from the session and redirect to /blog. -->

<!-- User is logged in and adds a new blog post, then is redirected to a page featuring the individual blog entry they just created (as in Build-a-Blog). -->

<!-- User visits the /blog page and sees a list of all blog entries by all users. -->

<!-- User clicks on the title of a blog entry on the /blog page and lands on the individual blog entry page. -->

User clicks "Logout" and is redirected to the /blog page and is unable to access the /newpost page (is redirected to /login page instead).



Basic requirements complete! 





