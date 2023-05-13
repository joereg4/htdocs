# htdocs

#website.service
[Unit]
Description=Gunicorn instance to server website Flask app
After=network.target

[Service]
User=joe
Group=www-data
WorkingDirectory=/var/www/htdocs
Environment="PATH=/home/joe/env/website/bin"
ExecStart=/home/joe/env/teton/bin/gunicorn --workers 3 --bind unix:website.sock -m 007 wsgi:app

[Install]
WantedBy=multi-user.target
