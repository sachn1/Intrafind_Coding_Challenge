# Intrafind Coding Challenge

This repository is part of the coding challenge provided by Intrafind

As the first version it includes a REST API implemented using Flask that helps one to create a user and update/delete an existing user.
Currently the user details are stored in the RAM.

The program can be run with the following script

    > python routes.py
    This should automatically start the Flask server on your localhost:2827
    
Use Docker Service:
   Build docker image:
 
    > docker build -t intrafindapp:latest .

   Run docker:
   
    > docker run -p 2827:2827 intrafindapp
    This should automatically start the Flask server on your localhost:2827
