# Final Project: Item Catalog

### Deployment Details:

#### IP Address: 54.213.237.120

#### SSH Port: 2200

#### Web Application URL: 54.213.237.120.xip.io

### Software Installed:
- apache2
- flask
- flask-sqlalchemy
- httplib2
- libapache2-mod-wsgi
- libpq-dev
- oauth2client
- postgresql
- python-psycopg2
- requests
- sqlalchemy

### Configuration Changes
- Add "grader" and "catalog" user accounts
- Change SSH port from 22 to 2200
- Add public keys to "ubuntu" and "grader" user accounts
- Set permissions on .ssh directory (700) and authorized_keys file (644) for above users
- Disable password-based logins for all users
- Configure firewall to allow only tcp (port 2200), www and ntp incoming traffic and allow all outgoing traffic
- Confirm that local timezone is set to UTC
- In /etc/apache2/sites-enabled/000-default.conf, uncomment WSGIScriptAlias and set its value to: "/ /var/www/flaskapp/udacity_deploy_linux/otrcatalog.wsgi"
- Note: The actual database user password and application secret key have been removed from "db_creds.py" and "otrcatalog.wsgi" files, respectively, in the GitHub repository.  

### Postgresql Changes
- Create "otrcatalog" database
- Create "otrcatalogrole" role
- Create "app" schema in "otrcatalog" database
- Set search path on "otrcatalog" database to "app" schema
- Grant the following privileges to "otrcatalogrole":
-- Connect to "otrcatalog" database
-- Usage and create on "app" schema
-- Select, insert, update and delete on tables (as default)
-- Use sequences in "app" schema
- Create user "catalog" and grant it "otrcatalogrole" role
- Revoke all rights to "otrcatalog" database from "public" role

### Other Third-Party Resources Used (not a comprehensive list)
- Digital Ocean community (https://www.digitalocean.com/community) (information about Apache and PSQL)
- Amazon AWS article - https://aws.amazon.com/blogs/database/managing-postgresql-users-and-roles/ (very useful info about PSQL roles/users)
- developers.google.com (OAuth provider for user login)
- Stack Overflow (stackoverflow.com)


"OTR Program Catalog" is a Flask web application with a PostgreSQL back end that provides an interface for browsing and managing a catalog of Old Time Radio (OTR) genres and programs. 
It is written in Python 2 and leverages Google oauth for user login.

### OTR
OTR (also known as the Golden Age of Radio) typically refers to scripted radio programs which aired from the early 1920s through the early 1950s when television replaced radio as the dominant broadcast medium. Since this definition is considered by some to be overly strict and as such is controversial, this application will accept information about radio programs which aired between 1920 until 1980. 


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

#### /genre/<int:genre_id>/program/<int:program_id>/JSON
This endpoint returns data for a single program specified with "genre_id" and "program_id". For example, "/genre/1/program/13/JSON" might return the following:
```
{
  "description": "The Fred Allen Show was a popular and long-running American old-time radio comedy program starring comedian Fred Allen and his wife Portland Hoffa. Over the course of the program's 17-year run, it was sponsored by Linit Bath Soaps, Hellmann's, Ipana, Sal Hepatica, Texaco and Tenderleaf Tea. The program ended in 1949 under the sponsorship of the Ford Motor Company.\r\n\r\nThe most popular period of the program was the few years of sponsorship under the Texaco Gas Company. During this time, the program was known as Texaco Star Theatre with Fred Allen. On the December 6, 1942 episode of the program, Allen premiered his first in a series of segments known as \"Allen's Alley\". The segments would have Allen strolling through an imaginary neighborhood, knocking on the \"doors\" of various neighbors, including average-American John Doe (played by John Brown), Mrs. Nussbaum (Minerva Pious), pompous poet Falstaff Openshaw (Alan Reed), Titus Moody (Parker Fennelly), and boisterous southern senator ...", 
  "genre_id": 1, 
  "id": 13, 
  "name": "The Fred Allen Show", 
  "yearBegan": 1932, 
  "yearEnded": 1949
}
```

### Future Improvements
In order to make the application more useful, I would like to allow logged-in users to add resource links for individual programs. These links would be sources of additional information, images, audio recordings, etc. The application will allow a logged-in user to add URLs for any program, not just those programs they added themselves.
