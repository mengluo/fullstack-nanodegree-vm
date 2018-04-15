# UdacityProject4
Catalog App

## Intro
> This is a RESTful web application that provides a list of games within a variety > of game genres as well as provide a user registration and authentication system.
> Registered users will have the ability to post, edit and delete their own games.
> The app is using the Python framework Flask along with implementing third-party > (google api) OAuth authentication.
> Various HTTP methods are used to implement CRUD (create, read, update and > delete)operations.

## Requirements
  - [Python 3](https://www.python.org/downloads/) installed on your Mac/Windows
  - Add python.exe to PATH environmental variable if you are using Windows
  - Install Vagrant and VirtualBox
  - Setup database schema for catalog app to use, using `database_setup.py` script
  - Create initial dataset for catalog app to use, using `CatalogDataLoad.py`

## Download and Run
  - Download/Clone the project folder `fullstack-nanodegree-vm` from [GitHub](https://github.com/mengluo/fullstack-nanodegree-vm)
  - Launch the Vagrant VM (vagrant up)
  - Open root folder and go to folder `vagrant` and then open folder `catalog`, there should be five files and two folders.
  - Five files include `database_setup.py`, `CatalogDataLoad.py`, 'CatalogApp.py', 'client_secrets.json' and 'README.txt'
  - Two folders include 'templates' and 'static'
  - 'templates' folder contains all html files and 'static' folder contains all css and js files
  - Within VM, run command *"python database_setup.py"* to create three objects mapping to corresponding tables in database (User, GameGenre and Game)
  - Within VM, run command *"python CatalogDataLoad.py"* to import default game genres and example games for each game genre for User 1 (default user)
  - You only need to above two steps once when setting up the database for the first time
  - `CatalogApp.py` is the script you should use to run the app on web server (localhost:8000), the web server should be local machine and the app should be using port 8000.
  - Within VM, run command *"python CatalogApp.py"* to run the application and you can see the status of the app outputting content in console.
  - `client_secrets.json` is data used among google api oAuth, web browser and the catalog app for user authentication purposes

## User Manual
* The homepage displays all game genres along with the latest added items.
* Selecting a specific game genre shows you all the games available for this category.
* Selecting a specific game shows you specific information of that game, including the title, description and game genre it belongs to.
* After logging in (top right login button), a user has the ability to add, update, or delete game but not the game genre.
* Only user 1 who creates all default game genres and games can delete all the example game genres and games.
* Users have to login with their google credentials in order to add/edit/delete their own games.
* If it is the first time for user to login, a new user info will be created and stored in local system.
* One user is not allowed to delete/edit games added by other users, a warning dialog will popup if a user tries to do it and will be instructed to add his/her own game first
* whenever an user wants to add a game to a specific game genre, go to the home page by clicking `Catalog App` on top left corner and use `Add a New Game` button
* Add, delete and edit game operations always consider authorization status prior to execution
* Log out button (showing up after logging in on top right corner) helps user revoke the token for current session

* The application provides JSON endpoints for users to view game genre info and game info in json format as below,
    > **Get all game genres info** --- 'localhost:8000/gamegenres/JSON'
    > **Get all info for a game genre by specifying the game genere id** --- 'localhost:8000/gamegenres/<game_genre_id>/JSON'
    > **Get all info for a game by specifying the game genre id it belongs to and its game id** --- 'localhost:8000/gamegenres/<game_genre_id>/games/<game_id>/JSON'
