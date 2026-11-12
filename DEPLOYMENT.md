# Production deployment

This delivery is source code and a frontend build. It has not been deployed to your existing GitHub Pages site or any public server.

Use a Linux host with Python 3.12, Node.js 22 for builds, PostgreSQL, a process supervisor and an HTTPS reverse proxy. Serve the frontend and Django API on **the same origin**, such as `https://portfolio.example.com/`. GitHub Pages cannot run Django; hosting only the frontend there will not provide the admin and inquiries.

## Prepare

1. Copy the project to the server and create a Python virtual environment.
2. Install `backend/requirements-lock.txt`; run `npm ci --prefix frontend` and `npm run build --prefix frontend`.
3. Copy `backend/.env.example` to `backend/.env`. Set `DEBUG=False`; generate a new secret using `python -c "import secrets; print(secrets.token_urlsafe(64))"`.
4. Set `ALLOWED_HOSTS` to your exact domain and `CSRF_TRUSTED_ORIGINS` to its exact HTTPS origin. Never set a wildcard.
5. Set all PostgreSQL environment values from `.env.example`. Never reuse the local SQLite file for a multi-worker public deployment.
6. Configure SMTP if email alerts are desired. Keep `.env` readable only by the service account.
7. Run migrations, seed projects, collectstatic and createsuperuser. Seed only initially or deliberately; it does not modify existing entries.
8. Run `python manage.py check --deploy` and `python manage.py test portfolio`.

Example service command, with working directory `backend`:

```sh
/path/to/backend/.venv/bin/gunicorn config.wsgi:application --bind 127.0.0.1:8000 --workers 2 --timeout 60
```

Django/WhiteNoise serves the compiled frontend and Django admin static assets. User-uploaded cover images need a media location in the reverse proxy.

## Nginx example

Replace the domain, paths and certificate locations. This example assumes Nginx terminates TLS directly. Redirect port 80 to HTTPS separately. Gunicorn must listen only on loopback.

```nginx
server {
    listen 443 ssl;
    server_name portfolio.example.com;
    ssl_certificate /etc/letsencrypt/live/portfolio.example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/portfolio.example.com/privkey.pem;
    client_max_body_size 6m;

    location /media/ {
        alias /srv/pranav-portfolio/backend/media/;
        add_header X-Content-Type-Options nosniff always;
        autoindex off;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 60s;
    }
}
```

Set `TRUST_PROXY=True` only for this controlled configuration, where Nginx overwrites these headers and users cannot directly reach Gunicorn. If you have another CDN/proxy in front, configure trusted IP restoration first; otherwise inquiry throttling will group visitors by the proxy's address. Do not trust arbitrary incoming forwarded IPs.

## Before publishing

- Replace the supplied résumé if needed; it is the original PDF.
- Confirm your current role, project contribution descriptions and permission to display screenshots.
- Add confirmed technology tags in admin if desired.
- Add your final canonical URL and an absolute `og:image` URL in `frontend/index.html`; rebuild.
- Configure backups for PostgreSQL and `backend/media`, plus a retention policy for inquiries.
- Run one periodic `retry_notifications` job; verify a real inquiry and SMTP delivery.
- Test admin login, logout, upload, draft visibility and mobile form behavior over HTTPS.

After frontend edits, rebuild and restart the application so WhiteNoise reloads the new files. Database project edits do not need a rebuild. Run migrations after model changes. Do not deploy the development server, test database, test accounts or a DEBUG=True environment.
