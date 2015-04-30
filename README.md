# GBEER
## Gene Block Evolution, Evaluation, and Research

This repository is a project that analyzes gene block conservation in terms of their 
operons at certain operon events. To install the project, please do the following:

## Aptitude

The following will need to be installed on the server running the application:
-RabbitMQ: follow [Install RabbitMQ on Debian](http://www.rabbitmq.com/install-debian.html)
-apache2
-libapache2-mod-wsgi
-python-pip

There is an additional file in the `setup' folder called pkglist which contains all packages 
needed to run the system. You can install those via apt-get as well.

## Pip

This uses virtualenv. To setup virtualenv take the following steps:

- <code>sudo pip install virtualenv</code>
- <code>sudo pip install virtualenvwrapper</code>
- Paste this is your  ~/.bashrc:

```
# Python virtualenv stuff
export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python
export WORKON_HOME=/virtualenvs
source "$(which virtualenvwrapper.sh)"
```

- Create and change the owner of /virtualenvs to you: <code>sudo chown $USER:$USER /virtualenvs/</code>

- Source your new ~/.bashrc: <code>source ~/.bashrc</code>

- Create the virtualenv flask: <code>mkvirtualenv flask</code>

Either use the requirements.txt in the repository to download all dependencies at once or install individually.

To install all at once run: <code>pip install -r requirements.txt/code>.

## Apache

- Edit the file <code>$APP/operonevodb.conf</code> by replacing all occurrences of $APP in the file
with the value of $APP i.e. /vagrant/GBEER.

- Move $APP/setup/gbeer-apache.conf to /etc/apache2/sites-available/.
<code>mv $APP/setup/gbeer-apache.conf /etc/apache2/sites-available/</code>

- Edit

- Disable the default site, <code>sudo a2dissite default</code>

- Enable the operonevodb site, <code>sudo a2ensite operonevodb.conf</conf>

## Celery

Celery is how we run our service code asynchronously on the server. But in order for this to work, 
we need to create a Daemon process that will run this on startup.

- Edit the file <code>$APP/setup/celeryd-config</code> and <code>$APP/setup/celeryd-initd</code> by replacing all occurrences of $APP in the file
with the value of $APP i.e. /vagrant/GBEER.

- Move $APP/setup/celeryd-config to /etc/defualt/celeryd. It is important that it is named `celeryd`.
<code>mv $APP/setup/celeryd-config /etc/defualt/celeryd</code>

- Move $APP/setup/celeryd-initd to /etc/init.d/celeryd. It is important that it is named `celeryd`.
<code>mv $APP/setup/celeryd-initd /etc/init.d/celeryd</code>
