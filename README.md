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

* copy (with sudo) 'scientificdev.ini' file to `/etc/uwsgi/sites`:  
```bash
sudo cp config-files/scientificdev.ini /run/uwsgi/sites
```

* be careful with the names of folders and project inside `scientificdev.ini` file:  
```bash
[uwsgi]
project = scientificdev
uid = ubuntu
base = /home/ubuntu/scientificdev

chdir = %(base)
home = /home/ubuntu/scientificdev/my_env
pythonpath = %(base)
env = DJANGO_SETTINGS_MODULE=settings.production
module = sd.wsgi:application

master = true
processes = 5

socket = /run/uwsgi/%(project).sock
chown-socket = %(uid):www-data
chmod-socket = 660
vacuum = true
```

* install uWSGI inside the virtual environment: `pip install uwsgi` and point to it in `uwsgi.service` file:  
```bash
[Unit]
Description=uWSGI Emperor service

[Service]
ExecStartPre=/bin/bash -c 'mkdir -p /run/uwsgi; chown ubuntu:www-data /run/uwsgi'
ExecStart=/home/ubuntu/scientificdev/my_env/bin/uwsgi --emperor /etc/uwsgi/sites
Restart=always
KillSignal=SIGQUIT
Type=notify
NotifyAccess=all

[Install]
WantedBy=multi-user.target
```  

* copy (with sudo) `uwsgi.service` file to `/etc/systemd/system/`
* The `uwsgi` service is managed by [systemd](https://www.digitalocean.com/community/tutorials/how-to-use-systemctl-to-manage-systemd-services-and-units), 
which is an init system and system manager (default for Ubuntu).  

### 4. Nginx configuration ###

* copy (with sudo) `scientificdev.conf` file to `/etc/nginx/sites-available/` (Nginx's directives),  
* create symlink (with sudo) to aforementioned file in `/etc/nginx/sites-enabled/`:  
```bash
sudo ln -s /etc/nginx/sites-available/scientificdev.conf scientificdev.conf
```
* remove old configuration file
* add default_server in listen section,  
* remove default files in 'sites-available' and 'sites-enabled' folders.
* to be more reliable we used [Let's Encrypt SSL/TLS certificates with Nginx](https://www.nginx.com/blog/using-free-ssltls-certificates-from-lets-encrypt-with-nginx/).  


### 5. Database configuration ###

### 5. Celery configuration ###

