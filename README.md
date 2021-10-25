# Password Manager
[![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)](https://travis-ci.org/joemccann/dillinger)

Web app designed to store and manage online credentials.

## Tech Stack
**Frontend**: HTML/CSS, JavaScript

**Backend**: Python 3.7, Flask, Flask-Limiter, bcrypt, pycryptodome, ...(all libs are in *requirements.txt*)

**Database**: PostgreSQL

**Others**: Docker, NGINX



## Features
- Login, register and reset forgotten password to Manager
- Add a new password
- Encrypt and store safely user passwords
- Decrypt stored passwords with master password
- Safely configured environment
- And many more


## Before Running
From root folder:
1. Go to */web* and rename **.env.example** file to **.env**
2. Go to */database* and rename **.env.example** file to **.env**
3. Go to */nginx/data/certs* and replace **safecert.crt.example** with your .crt. Be sure to name it **safecert.crt**
4. Go to */nginx/data/certs* and replace **safecert.key.example** with your .key. Be sure to name it **safecert.key**


## Docker
**(Before starting the application, make sure you did everything mentioned in the Before Running section)**
Run app using Docker with:
```sh
cd app
docker-compose up --build
```

It will create the docker container for a password manager app. 
Once done, launch your web browser and go to  **https://localhost/** .
That's it, enjoy checking it out.



_[Reupload]_
