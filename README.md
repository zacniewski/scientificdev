# Scientific Dev #

Settings, configurations, tips and other things related to [my site](https://scientificdev.net/).

### 1. Settings of the project ###

* Instead single `settings.py` file I created separate folder named `settings` and settings for particular usages are there.  
* For example - if I'd like to run development project on my PC:  
```bash
        python manage.py runserver --settings=settings.titan
 ```
where `titan.py` (derives from `base.py`) is the settings file for my PC,

### 2. Switching working directories of my [Scientific Dev](https://scientificdev.net/) website ###

* Old project was named `ModernBusiness` (due to name of the free Bootstrap template :smiley:),  
* The new one is called `ScientificDev`,  
* Names of the folders are the same as names of the aforementioned projects (with lowercase),  
* The newer project was cloned next to old one, the latter will be removed after changes.  


### 3. uWSGI configuration ###

* copy (with sudo) `scientificdev.conf` file to `/etc/nginx/sites-available/` (Nginx's directives),


### 4. Nginx configuration ###

* copy (with sudo) `scientificdev.conf` file to `/etc/nginx/sites-available/` (Nginx's directives),


### 5. Nginx configuration ###

* copy (with sudo) `scientificdev.conf` file to `/etc/nginx/sites-available/` (Nginx's directives),  
* create symlink (with sudo) to aforementioned file in `/etc/nginx/sites-enabled/`:  
```bash
ln -s /etc/nginx/sites-available/scientificdev.conf scientificdev.conf
```
* remove old configuration file
* add default_server in listen section,  
* remove default files in 'sites-available' and 'sites-enabled' folders.