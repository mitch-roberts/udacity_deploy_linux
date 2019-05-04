# Project: Item Catalog

"OTR Program Catalog" is a Flask web application with a SQLite back end that provides an interface for browsing and managing a catalog of Old Time Radio (OTR) genres and programs. It is written in Python 2 and leverages Google oauth for user login.

### OTR
OTR (also known as the Golden Age of Radio) typically refers to scripted radio programs which aired from the early 1920s through the early 1950s when television replaced radio as the dominant broadcast medium. Since this definition is considered by some to be overly strict and as such is controversial, this application will accept information about radio programs which aired between 1920 until 1980. 

### To run the application:
1. Install Vagrant and VirtualBox.
2. Clone the fullstack-nanodegree-vm.
3. Launch the Vagrant VM (vagrant up) and SSH into the shell (vagrant ssh).
4. Download the project from GitHub (https://github.com/mitch-roberts/udacity_catalog_proj.git) and place code in the "vagrant" directory.
5. Run application.py to start the web server (i.e., "python application.py").
6. Navigate to "http://localhost:5000/" in a browser.

Note: The SQLite database file ("otrCatalog.db") contains some basic initial content. To begin with an empty database, stop the web server, delete otrCatalog.db and then run "models.py" (i.e., "python models.py").

### Usage
The homepage shows the 10 most recently added programs. The user may browse programs by genre using the navigation bar on the left side of the page. To get details about a program the user may click the linked program name.

A login link is provided below the banner. Users must log in using a Google account. After logging in, a link to log out appears in its place. Once logged in, users may add, edit and delete genres and programs with the following restrictions:
- Users may view all content without being logged in.
- To add or alter information, users must log in using their Google credentials.
- Any logged-in user can create a new OTR genre. 
- Any logged-in user can add a program to any existing genre.
- Only the user that created a genre may delete it or edit its name.
- No user is permitted to delete a genre which contains programs.
- Only the user that created a program may delete or edit it.
- Add, edit and delete links are generally hidden when the user is not permitted to perform these functions.


### JSON Endpoints

Endpoints are provided for retrieving genre and program information in JSON format:
#### /genres/JSON
This endpoint will return a list of all OTR genres. For example:
```
{
  "Genres": [
    {
      "id": 1, 
      "name": "Comedy"
    }, 
    {
      "id": 3, 
      "name": "Drama"
    }, 
    {
      "id": 4, 
      "name": "Mystery"
    }
  ]
}
```
#### /genre/<int:genre_id>/programs/JSON
This endpoint will return a list of programs belonging to the genre specified with "genre_id". For example, "/genre/1/programs/JSON" might return the following:
```
{
  "Programs": [
    {
      "description": "TBD", 
      "genre_id": 1, 
      "id": 2, 
      "name": "Duffy's Tavern", 
      "yearBegan": 1939, 
      "yearEnded": 1952
    }, 
    {
      "description": "TBD", 
      "genre_id": 1, 
      "id": 1, 
      "name": "Fibber McGee and Molly", 
      "yearBegan": 1935, 
      "yearEnded": 1951
    }, 
    {
      "description": "TBD", 
      "genre_id": 1, 
      "id": 3, 
      "name": "The Abbot and Costello Show", 
      "yearBegan": 1946, 
      "yearEnded": 1949
    }
  ]
}
```

