# Let's Goal!
## Description
Let's Goal is an app that allows you to set goals, add steps to them to track your progress until you've accomplished them. Users can like Goals posted by other users to get some inspiration.
Their User Profile gives them a quick overview of all the Goals they have created, the ones that are _not started_, _in progress_ and _accomplished_.

## File Contents
### Python files
- admin.py (extended)
    Rather than only registering models to view in the admin panel, I'va also made use of admin.ModelAdmin in order to create List views of different models.
- api_views.py
    In this file I've been able to set up the API useing Django Restframework. I'm proud I got it to actually work and could create some goals using curl commands,  but unfortunately haven't had the time to put it to use in the app. that's the next step I want to take to really upgrade my skills and I'm super excited to put this into practice!
- error.py
    This file contains a little function called 'catch(*args)' that I use to print things in a nice and readable format so I can find items quickly and in a structured way in the terminal. I use it mainly to debug, when I don't want to shut down the server and enter the shell to test things. Little gimmick but I like it :)
- forms.py
    In this file you will find all the forms used in the app. django-crispy-forms comes in to make everything look nicely by adding bootstrap classes after multiple attempts to modify widgets.
- serializers.py
    Here I've created a goal-serializer using the rest_framework. I'm proud about the fact that I could create properties in some models to send more complex data to the serializer

### HTML Templates
- goal.html
    This file displays individual goals. This is where you can also add steps to your goals and view all information about it
- index.html
    The 'home' template where the user can see all his goals
- layout.html
    the layout in which all other templates' body is displayed
- login.html
    The page where the user can login once he created an account
- register.html
    Here the user can register an account
- trending.html
    All goals ordered by number of likes in descending order. (I'm proud of this, too because I've spend a couple day's trying to figure out how to aggregate a manytomany field until I found the correct resoucres.)
- user_profile.html
    All user related information lives and can be modified here

### Styling
- styles.scss
    This is where all the styling lives. Once compiled it creates the style.css file

### JavaScript
- index.js
    Here is all the front-end manipulation. I've used mostly jQuery to handle for example 'like' functions, by changing the svg's color, fetching the number of likes and inserting them into the DOM. I've also made a successful attempt to fetch the rest api to return a json object. I'm very fond of jQuery since I've learned about it but I'm also aware that I should practice plain JavaScript more often.

### Git and Virtual Environments
I've finally leared how to use git and github to create a local and remote repository. I've actaully practiced by doing some work on my personal computer, pushing it to github and pulling it onto my work computer to continue working. This way I wasable to get the hang of version control, branches etc.
The goals_env folder has been included in the .gitignore file but I'm super proud I've finally successfully created and used this. I had gotten into the habit of doing everything on a global scale but foudn myself stuck with incorrect package versions for various projects (the reason why virtual ennvironments are used in the first place)


## What I have learned with this project
With this final project I have attempted to use more in depth Django features, as well as other practices such as:
- Creating and using a virtual environment 
- Learning to use Git, adding, committing, pushing and pulling
- Creating a Django REST API using the Django REST Framework
- Creating Serializers in a seperate file
- Uploading files (mostly images) to the Database
- Using SVG for items such as Like buttons and manipulate their style
- Making use of jQuery to manipulate the DOM
- Learing and using Sass
- Customizing the Admin panel
