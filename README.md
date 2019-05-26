# taskinfibeam
1)Download source code from git.
2)open project in editor
3)create virtual env
4)activate virtualenv
5)change the setting of database connectivity.
7) install database package
8)install crispy_forms - pip install django-crispy-forms
9) isntall image package -  pip install pillow
10) Install geoip2 package for ip to location - pip install geoip2
11) goto geoipdatabase download page copy link of GeoLite2 Country (https://dev.maxmind.com/geoip/geoip2/geolite2/)
	https://geolite.maxmind.com/download/geoip/database/GeoLite2-Country.tar.gz
	wget https://geolite.maxmind.com/download/geoip/database/GeoLite2-Country.tar.gz (in terminal)
  extact tar.gz using command  tar -xzf GeoLite2-Country.tar.gz (extract inside project)

12) Create superuser account admin account-
python manage.py createsuperuser (to login as admin user in web)

13) install axes package for blocking user inavlid attempt - pip install django-axes
		
Note - 3 Invalid login attempt code is commented in all module due to some issue in my code.
