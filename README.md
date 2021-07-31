This is a simple Anonymous Voting Webapp named Votacion, written in python using the Flask framework and using PostgreSQL as a RDBMS.

The app is hosted at https://votacion-web-app.herokuapp.com 

After creating an account, users can then proceed to create a poll with multiple choices. Users can also set a deadline for voting. After creating the poll, the user will recieve a URL for the poll which he/she can then share with friends and ask them to cast their votes. Voters will be asked to enter a valid email id and only one vote can be cast for a particular poll from an email id. 

In the profile tab, users can update their account information, see all their polls or delete their account. When a user account is deleted all the polls created by that user will also be deleted.