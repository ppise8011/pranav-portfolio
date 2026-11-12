# Pranav Pise — Portfolio v3

React + GSAP portfolio with a Python/Django backend. Updated to 4 years of experience, with Python, WWC CRM and the 11 newly supplied websites. The ten original website projects are preserved: 22 project entries in total, including WWC CRM.

## Start on your Windows 10 PC

1. Install **Python 3.12** (include the Python launcher) and **Node.js 22 LTS**.
2. Extract the entire ZIP. Keep `frontend` and `backend` together.
3. Double-click **SETUP_WINDOWS.bat**. Internet is needed to install dependencies. Create your own admin username and password when asked. Password typing is invisible; this is normal.
4. Double-click **START_WINDOWS.bat** and keep the terminal open.
5. Open the portfolio at **http://127.0.0.1:8000/**.
6. Open the admin at **http://127.0.0.1:8000/admin/**.

No demo password is included. No payment service or paid database is required for local use. SQLite is used locally; PostgreSQL is supported for deployment.

If setup reports that an admin already exists, you can skip creating another account. To reset a password:

```bat
backend\.venv\Scripts\python.exe backend\manage.py changepassword YOUR_USERNAME
```

## Manage projects

In admin, open **Projects**. Add or edit:

- Name, category, tagline, description and project details.
- Website link, your role, technologies and status.
- Cover image: JPG, PNG or WebP, up to 5 MB. Suggested size: 1440 × 1000.
- Background colour, Featured, Published and ordering number.

Technology names use a JSON list, for example `["WordPress", "PHP", "Elementor"]`.

**Published** controls public visibility. **Featured** controls the initial homepage selection. Lower ordering numbers appear first. Uploaded covers override bundled images. Reload the portfolio after saving; no rebuild is needed for admin changes.

For new categories, edit the choices in `backend/portfolio/models.py` and the frontend filters together, then make/apply migrations.

The initial seed command only creates missing projects and never overwrites admin edits. To remove an initial project permanently, unpublish it; rerunning the seed command can recreate a deleted seed entry.

## Inquiries and email

The form saves real inquiries to the database. It uses validation, CSRF protection, consent, a honeypot, a shared database rate limit and duplicate-submission protection. It reports a success only after the server accepts the inquiry.

Open **Inquiries** in admin to read messages, add private notes and mark them New, Contacted or Closed. Inquiries cannot be read through the public API. Keep database/media backups; these contain private data.

**Email setup is required for email alerts.** Edit `backend/.env` with your SMTP provider's host, port, username, password and authorized sender address. Restart the server. The recipient is `pranavpise8011@gmail.com` by default.

```dotenv
EMAIL_HOST=smtp.your-provider.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-smtp-username
EMAIL_HOST_PASSWORD=your-smtp-password-or-app-password
EMAIL_USE_TLS=True
DEFAULT_FROM_EMAIL=your-verified-sender@example.com
INQUIRY_NOTIFY_EMAIL=pranavpise8011@gmail.com
```

Without SMTP, inquiries still save successfully and remain visible in admin. Failed notifications remain pending; use the admin **Retry email notifications** action or:

```bat
backend\.venv\Scripts\python.exe backend\manage.py retry_notifications
```

For production, schedule that command every five minutes with a single scheduler. It also deletes expired throttle records. Do not run simultaneous retry jobs: email delivery is not exactly-once across a process crash. The form does not auto-email visitors.

## What changed

- New dark violet and lime visual design with responsive layouts.
- GSAP hero entrance, scroll reveals, moving project columns, pointer tilt and a motion toggle with reduced-motion support.
- Project filters, accessible native-dialog case studies and live website links.
- Local project previews with brand-coloured frames; existing archive previews retained.
- Python and 4 years of experience in the hero/about/expertise sections.
- WWC CRM case study, clearly labelled as in development. Its illustration is a concept and contains no real company data.
- Django admin, project publishing, image uploads and inquiry tracking.
- SEO page metadata, social cover image, favicon and labelled navigation controls.
- Actual error states, local assets and no fake form success.

Descriptions intentionally avoid invented commercial results, traffic statistics or conversion claims. Project technologies are left unassigned where the supplied information did not establish the implementation. Add confirmed stacks in admin.

**Résumé:** the PDF from your original ZIP is preserved unchanged. Replace `frontend/public/Pranav_Pise_.pdf` with your latest résumé before publishing if its content is outdated, then rebuild.

## Develop locally

Start Django in one terminal:

```bat
backend\.venv\Scripts\python.exe backend\manage.py runserver 127.0.0.1:8000
```

Start React in another:

```bat
cd frontend
npm run dev
```

Open http://127.0.0.1:5173/. Vite proxies `/api/` and `/media/` to Django. Use `127.0.0.1` consistently. The admin runs on port 8000. For frontend code changes, rebuild before using the single-server port-8000 view:

```bat
npm run build --prefix frontend
```

For macOS/Linux, use `python3 -m venv backend/.venv`, replace `backend\.venv\Scripts\python.exe` with `backend/.venv/bin/python`, and run the same install/build/migrate/seed/collectstatic commands shown in the Windows script.

## Verification

```bat
backend\.venv\Scripts\python.exe backend\manage.py collectstatic --noinput
backend\.venv\Scripts\python.exe backend\manage.py test portfolio
npm run build --prefix frontend
```

See `VALIDATION.md` for the checks performed on this delivery. See `DEPLOYMENT.md` before publishing; the local development server is not a production server.

## Project structure

- `frontend/src/` — React views, GSAP and styles.
- `frontend/public/` — project previews, local fonts, original résumé, initial project data.
- `frontend/dist/` — included production frontend build; regenerate after frontend changes.
- `backend/portfolio/` — models, APIs, admin, tests and commands.
- `backend/config/` — Django settings and URLs.
- `backend/.env.example` — local settings template; no credentials.

A frontend-only preview can use `VITE_STATIC_PREVIEW=true` at build time to read the initial bundled project list. This mode is not the live admin-managed portfolio and still needs a backend to send inquiries. Full-stack builds default to false, so a server outage cannot resurrect projects you have unpublished.
