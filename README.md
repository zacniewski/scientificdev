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
sudo cp config-files/scientificdev.ini /etc/uwsgi/sites
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

* install uWSGI inside the virtual environment: `pip install uwsgi` and point to it in `uwsgi.service` file, in the `ExecStart` line:    
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
which is an init system and system manager (default for Ubuntu),  
* to enable service to start automatically at boot:  
```bash
sudo systemctl enable uwsgi
```    
* check logs with `sudo journalctl -u uwsgi`.

* to apply changes without rebooting:  
```bash
sudo systemctl restart uwsgi
```

### 4. Nginx configuration ###

* copy (with sudo) `scientificdev.conf` file to `/etc/nginx/sites-available/` (Nginx's directives),  
* create [symlink](https://www.freecodecamp.org/news/symlink-tutorial-in-linux-how-to-create-and-remove-a-symbolic-link/) (with sudo) to aforementioned file in `/etc/nginx/sites-enabled/`:  
```bash
sudo ln -s /etc/nginx/sites-available/scientificdev.conf scientificdev.conf
```
* remove old configuration file and its symlink,  
* add default_server in listen section,  
* remove default files in 'sites-available' and 'sites-enabled' folders.
* to be more reliable we used (old version) - [Let's Encrypt SSL/TLS certificates with Nginx](https://www.nginx.com/blog/using-free-ssltls-certificates-from-lets-encrypt-with-nginx/),  
* newer versio (June 2022) for Ubuntu 20.04 is [here](https://www.digitalocean.com/community/tutorials/how-to-secure-nginx-with-let-s-encrypt-on-ubuntu-20-04),  
* in newer version there's no need to renew certificate manually, it is done by `certbot` service two times a day,  
* to enable service to start automatically at boot:  
```bash
sudo systemctl enable nginx
```  

* to apply changes without rebooting:  
```bash
sudo systemctl restart nginx
```
* to check syntax errors:  
```bash
sudo nginx -t
``` 

### 5. Database configuration ###
* the PostgreSQL database is used, so `psycopg2` package must be installed in active virtual environment:  
```bash
pip install psycopg2-binary
```  
* PostgreSQL must be [installed](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-postgresql-on-ubuntu-20-04) before in order to install `psycopg2` package.

### 6. Celery configuration ###
* Celery worker and beat are managed by [Supervisor](https://www.digitalocean.com/community/tutorials/how-to-install-and-manage-supervisor-on-ubuntu-and-debian-vps),  
* The per-program configuration files for Supervisor programs are located in the `/etc/supervisor/conf.d` directory, typically running one program per file and ending in `.conf`,  
* In the `command` line of aforementioned files we have to point location of celery process inside our virtual environment:  
    * for Celery worker (in scientific-celery-worker.conf file):  
    ```bash
    command=/home/ubuntu/scientificdev/my_env/bin/celery -A sd worker --loglevel=INFO
    ```
    * and for Celery beat (in scientific-celery-beat.conf file):  
    ```bash
    command=/home/ubuntu/scientificdev/my_env/bin/celery -A sd beat --loglevel=INFO
    ```  
* Useful commands of Supervisor are:  
    * `sudo systemctl status supervisor` (status of supervisor service),  
    * `sudo supervisorctl reread` (look for any new or changed program configurations in the `/etc/supervisor/conf.d` directory),  
    * `sudo supervisorctl update` (to confirm changes).  
* Don't forget to delete your old configuration files (if exist) in the `/etc/supervisor/conf.d` directory!  

### 7. Dump and restore of PostgreSQL database ###
* Dump your database on remote machine:  
```bash
pg_dump -U dbartur scientificdevdb > sdexport.sql
```
* Copy file with dumped database to your local machine:  
```bash
 scp root@www.scientificdev.net:/home/ubuntu/sdexport.sql sdexport.sql
```
* Don't forget to create `postgres` user on [Linux system](https://linuxhint.com/postgresql_installation_guide_ubuntu_20-04/) with the safe password,  

* Before you must create database with the same name and the same user like was on your remote machine,

* Sometimes you may need to edit `sudo nano /etc/postgresql/12/main/pg_hba.conf` file (check your version of PostgreSQL first, on Ubuntu 22.04 it's 14), 
and change  `# Database administrative login by Unix domain socket` or/and `# "local" is for Unix domain socket connections only` from `peer` to `md5`:    

```bash
# Database administrative login by Unix domain socket
local   all             postgres                                md5

# TYPE  DATABASE        USER            ADDRESS                 METHOD

# "local" is for Unix domain socket connections only
local   all             all                                     md5
```
* To restore database objects from file:  
```bash
psql -U dbartur -d scientificdevdb -f sdexport.sql
```

* To restart PostgreSQL service:  
```bash
sudo service postgresql restart
```

### 8. Fresh installation of the VPS's system (June 2022) ###
* Change Ubuntu 18.04 into [Ubuntu](https://ubuntu.com/about/release-cycle) 20.04 LTS,  
* change password for the `root` user: `passwd`,  
* remove [snap](https://www.debugpoint.com/2022/04/remove-snap-ubuntu/) and its packages,  
* install dependencies for OpenCV (scripts are in `config-files` folder),  
* my domain is already configured under IP given from OVH vendor,  
* install web server [Nginx](https://www.digitalocean.com/community/tutorials/how-to-install-nginx-on-ubuntu-20-04),  
* generate new [SSH key](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent) and [add](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account) it to your git account,  
* clone the repo to your remote machine,  
* install Certbot and [configure](https://www.digitalocean.com/community/tutorials/how-to-secure-nginx-with-let-s-encrypt-on-ubuntu-20-04) Let's Encrypt Certificate Authority (CA),  
* jump to #4 for more details about configuring Nginx,  
* create virtual environment inside project's folder,  
* activate it and install dependencies from `requirements.txt` file:  
 ```bash
   pip install -r requirements.txt
 ```
* install PostgreSQL (look into #7) and create database with proper name and the owner,  
* create `.env` file with credentials
* make migrations,  
* create superuser,  
* install [Supervisor](https://www.digitalocean.com/community/tutorials/how-to-install-and-manage-supervisor-on-ubuntu-and-debian-vps),  
* copy Celery files (look into #6) to Supervisor's folder,  
* create `logs` directory for logs from Celery worker and beat,  
* install message broker, in my case it's [Rabbit MQ](https://www.rabbitmq.com/),  
* update/add your SSH keys:  
```bash
ssh-keygen -f "/home/artur/.ssh/known_hosts" -R "www.scientificdev.net"
```
* and then connect via SSH with the domain name instead of IP address,  
* for greater security install following packages and allow SSH connections:  
```bash
sudo apt install fail2ban iptables ufw
sudo ufw enable
sudo ufw allow ssh
```
* restart your VPS :smiley: