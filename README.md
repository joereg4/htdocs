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

### nginx.con
```
user www-data;
worker_processes auto;
pid /run/nginx.pid;
include /etc/nginx/modules-enabled/*.conf;

events {
        worker_connections 768;
        # multi_accept on;
}

http {

        ##
        # Basic Settings
        ##

        sendfile on;
        tcp_nopush on;
        types_hash_max_size 2048;
        # server_tokens off;

        # server_names_hash_bucket_size 64;
        # server_name_in_redirect off;

        include /etc/nginx/mime.types;
        default_type application/octet-stream;

        ##
        # SSL Settings
        ##

        ssl_protocols TLSv1 TLSv1.1 TLSv1.2 TLSv1.3; # Dropping SSLv3, ref: POODLE
        ssl_prefer_server_ciphers on;

        ##
        # Logging Settings
        ##

        access_log /var/log/nginx/access.log;
        error_log /var/log/nginx/error.log;

        ##
        # Gzip Settings
        ##

        gzip on;

        ##
        # Virtual Host Configs
        ##

        include /etc/nginx/conf.d/*.conf;
        include /etc/nginx/sites-enabled/*;
}

```

### sites-available
```
server {
        server_name joereg4.com www.joereg4.com 45.32.193.31;

        location / {
                include proxy_params;
                proxy_pass http://unix:/home/joe/site/website.sock;
        }

    listen 443 ssl; # managed by Certbot
    ssl_certificate /etc/letsencrypt/live/joereg4.com/fullchain.pem; # managed by Certbot
    ssl_certificate_key /etc/letsencrypt/live/joereg4.com/privkey.pem; # managed by Certbot
    include /etc/letsencrypt/options-ssl-nginx.conf; # managed by Certbot
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem; # managed by Certbot


}
server {
    if ($host = www.joereg4.com) {
        return 301 https://$host$request_uri;
    } # managed by Certbot


    if ($host = joereg4.com) {
        return 301 https://$host$request_uri;
    } # managed by Certbot


        listen 80;
        server_name joereg4.com www.joereg4.com 45.32.193.31;
    return 404; # managed by Certbot




}
```

