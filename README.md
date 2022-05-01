# Scientific Dev #

Settings, configurations, tips and other things related to [my site](https://scientificdev.net/).

### Settings of the project ###

* Instead single `settings.py` file I created separate folder named `settings` and settings for particular usages are there.  
* For example - if I'd like to run development project on my PC:  
```bash
        python manage.py runserver --settings=settings.titan
 ```
where `titan.py` (derives from `base.py`) file for my PC,

* Dependencies
* Database configuration
* How to run tests
* Deployment instructions

### Contribution guidelines ###

* Writing tests
* Code review
* Other guidelines

### Who do I talk to? ###

* Repo owner or admin
* Other community or team contact