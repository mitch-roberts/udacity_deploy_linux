# Project: Item Catalog

"OTR Program Catalog" is a Flask web application with a SQLite back end that provides an interface for browsing and managing a catalog of Old Time Radio (OTR) genres and programs. It is written in Python 2 and leverages Google oauth for user login.

### OTR
OTR (also known as the Golden Age of Radio) typically refers to scripted radio programs which aired from the early 1920s through the early 1950s when television replaced radio as the dominant broadcast medium. Since this definition is considered by some to be overly strict and as such is controversial, this application will accept information about radio programs which aired between 1920 until 1980. 

### To run the application:
1. Install Vagrant and VirtualBox.
2. Clone the fullstack-nanodegree-vm.
3. Launch the Vagrant VM (vagrant up) and SSH into the shell (vagrant ssh).
4. Download the project from GitHub (https://github.com/mitch-roberts/udacity_catalog_proj.git) and place in a folder in the "vagrant" directory.
5. Run application.py to start the web server (i.e., "python application.py").
6. Navigate to "http://localhost:5000/" in a browser.

Note: The SQLite database file ("otrCatalog.db") contains some basic initial content. To begin with an empty database, stop the web server, delete otrCatalog.db and then run "models.py" (i.e., "python models.py").

### Usage
The homepage shows the 10 most recently added programs. The user may browse programs by genre using the navigation bar on the left side of the page. To get details about a program the user may click the linked program name.

A login link is provided below the banner. Users may log in using a Google account. After logging in, a link to log out appears in its place. Once logged in, users may add, edit and delete genres and programs with the following restrictions:
- Users may view all content without being logged in.
- To add or alter information, users must log in using their Google credentials.
- Any logged-in user can create a new OTR genre. 
- Any logged-in user can add a program to any existing genre.
- Only the user that created a genre may delete it or edit its name.
- No user is permitted to delete a genre which contains programs.
- Only the user that created a program may delete or edit it.
- Add, edit and delete links are generally hidden when the current user is not permitted to perform these functions.


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
      "id": 5, 
      "name": "Drama"
    }, 
    {
      "id": 4, 
      "name": "Game Show"
    }, 
    {
      "id": 3, 
      "name": "Horror"
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
      "description": "The Abbott and Costello Show is a comedy program from the era of old-time radio in the United States. It was broadcast first on NBC and later on ABC, beginning July 3, 1940, and ending June 9, 1949.\r\n\r\nFilm stars Bud Abbott and Lou Costello adapted their talents to radio for this 30-minute weekly comedy program. Vincent Terrace, in his book, Radio Programs, 1924-1984: A Catalog of More Than 1800 Shows, wrote, \"Many of the skits revolved around Bud and Lou's efforts to succeed in some sort of business venture.\" The skits were often ones that they had used in their vaudeville act.\r\n\r\nPopular culture scholar J. Fred MacDonald, in his book, Don't Touch That Dial!: Radio Programming in American Life, 1920-1960, wrote that the pair formed \"one of the leading radio comedy acts throughout the 1940s.\" He noted that Abbott was the straight man, with Costello \"the comedic force of the act.\"", 
      "genre_id": 1, 
      "id": 9, 
      "name": "Abbott and Costello", 
      "yearBegan": 1940, 
      "yearEnded": 1949
    }, 
    {
      "description": "Duffy's Tavern was an American radio situation comedy that ran for a decade on several networks (CBS, 1941\u201342; NBC-Blue Network, 1942\u201344; and NBC, 1944\u201351), concluding with the December 28, 1951, broadcast.\r\n\r\nThe program often featured celebrity guest stars but always hooked them around the misadventures, get-rich-quick schemes and romantic missteps of the title establishment's malaprop-prone, metaphor-mixing manager, Archie, portrayed by Ed Gardner, the writer/actor who co-created the series. Gardner had performed the character of Archie, talking about Duffy's Tavern, as early as November 9, 1939, when he appeared on NBC's Good News of 1940.", 
      "genre_id": 1, 
      "id": 12, 
      "name": "Duffy's Tavern", 
      "yearBegan": 1941, 
      "yearEnded": 1951
    }, 
    {
      "description": "Fibber McGee and Molly was an American radio comedy series. A staple of the NBC Red Network for the show's entire run and one of the most popular and enduring radio series of its time, the prime time situation comedy ran as a standalone series from 1935 to 1956, then continued as a short-form series as part of the weekend Monitor from 1957 to 1959. The title characters were created and portrayed by Jim and Marian Jordan, a real-life husband and wife team that had been working in radio since the 1920s.\r\n\r\nFibber McGee and Molly, which followed up the Jordans' previous radio sitcom Smackout, followed the adventures of a working-class couple, the habitual storyteller Fibber McGee and his sometimes terse but always loving wife Molly, living among their numerous neighbors and acquaintances in the community of Wistful Vista. As with most radio comedies of the era, Fibber McGee and Molly featured an announcer, house band and vocal quartet for interludes.", 
      "genre_id": 1, 
      "id": 11, 
      "name": "Fibber McGee and Molly", 
      "yearBegan": 1935, 
      "yearEnded": 1956
    }
  ]
}
```

### Future Improvements
In order to make the application more useful, I would like to allow logged-in users to add resource links for individual programs. These links would be sources of additional information, images, audio recordings, etc. The application will allow a logged-in user to add URLs for any program, not just those programs they added themselves.
