# Flashcards
Python Flashcard Project. <br>
Webbased Flashcard Learning App written with Flask.

## Features
You can 
* Register an User Account
* Each User could create their own Flashcard Collections
* Create Flashcards in that Collections
* Learn the Collection
* Mark the Flashcard as Wrong or Right answered
* Only learn the Wrong Answered Flashcards
* Question and Answer of the Flashcards allow Markdown Text


## Installation
1. Install the Requirements

<code>pip3 install -r requriements/common.txt</code>

2. Setup the Database

<code>python3 manage.py db init</code>

<code>python3 manage.py db migrate</code>

<code>python3 manage.py db upgrade</code>

3. Run the Application

<code>python3 manage.py runserver</code>

The Application was created and tested with Python Version 3.5

To run the tests execute

<code>python3 manage.py test</code>

To open a shell within the App Context run

<code>python3 manage.py shell</code>

## Screenshots of the Application

