## landfillrehab
EveryULB

### https://www.digitalocean.com/community/tutorials/how-to-serve-django-applications-with-apache-and-mod_wsgi-on-ubuntu-16-04

python3, pip3, django-11.1, bootstrap4 beta, mysql, mysqlclient(for the python-mysql connection), geopy, apache2, django-mathfilters

###### sudo apt-get install libmysqlclient-dev
###### sudo -H pip3 install mysqlclient
###### Add server to allowed hosts in settings.py
###### python3 manage.py runserver IP_ADDR:PORT


# While Installing in Foreign Computer:
###### 1. Create Databse, Change Database Settings
###### 2. makemigrations and then migrate
###### 3. Change Google Maps Key
###### 4. Install geopy
###### 5. Create Super User
###### 6. python3 manage.py collectstatic (FOR collecting all the static files to static/)
###### 7. go to this website to add states and databases -> populate_states_districts_data

### Set ServerName for apache2 in /etc/apache2/apache2.conf
### Change the sudo nano /etc/apache2/sites-available/000-default.conf file
### check sudo apache2ctl configtest
### sudo service apach2 restart
### go to landfillrehab and change the media folder permission so that apache2 can upload files to
### sudo chown -R www-data:www-data media
### enable gzip encoding for json and geojson in apache-enabled/deflate.conf
### go to /etc/mime.types and add a new mime type for geojson


#Use help.md for converting files to geojson

sudo apt-get update
sudo apt-get upgrade
sudo apt-get dist-upgrade
sudo apt autoremove
sudo apt install python3
sudo apt install python3-pip
sudo apt install mysql-client mysql-server mysql-common
sudo -H pip3 install django
sudo -H pip3 install --upgrade pip
sudo -H pip3 install geopy
sudo apt-get install libmysqlclient-dev
sudo -H pip3 install mysqlclient
sudo -H pip3 install django-mathfilters
git clone https://github.com/roshandash411/landfillrehab

cd landfillrehab
mysql -u root -p
create database landfillrehab;
python3 manage.py makemigrations gMapsIntegration
python3 manage.py migrate
python3 manage.py createsuperuser
sudo python3 manage.py runserver 138.68.234.118:80
