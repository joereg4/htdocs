# Site
## Update from Git
1. ssh joe@joereg4.com
2. cd /home/joe/site
3. git pull
4. sudo systemctl restart website
5. sudo systemctl status website


## website.service
```
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
```



## Python Venv
```
source ~/env/webenv/bin/activate
```

## NGINX
```
server {
        listen 80;
        server_name joereg4.com www.joereg4.com 45.32.193.31;

        location / {
                include proxy_params;
                proxy_pass http://unix:/home/joe/site/website.sock;
        }
 }
```

