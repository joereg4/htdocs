# htdocs

#website.service
[Unit]
Description=Gunicorn instance to server website Flask app
After=network.target

[Service]
User=joe
Group=www-data
WorkingDirectory=/home/joe/site
Environment="PATH=/home/joe/env/webenv/bin"
ExecStart=/home/joe/env/webenv/bin/gunicorn --workers 3 --bind unix:website.sock -m 007 wsgi:app

[Install]
WantedBy=multi-user.target




#Source
source ~/env/webenv/bin/activate

#NGINX
server {
        listen 80;
        server_name 45.32.193.31;

        location / {
                include proxy_params;
                proxy_pass http://unix:/home/joe/site/website.sock;
        }
 }

