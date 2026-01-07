## Quick context

- This is a small Flask-based QR attendance app implemented in a single main module: `app.py`.
- Static HTML pages (login, student, teacher, admin, account creation) live in the repository root and are served directly via Flask's `send_file` (not Jinja templates). Example: `index.html`, `accountcreate.html`, `admin.html`, `teacher.html`, `student.html`.
- Styles are under the `CSS/` folder (e.g. `CSS/stuff.css`).
- Dependencies are listed in `pyproject.toml` (Flask, Flask-Login, Flask-Bcrypt, Flask-SQLAlchemy, qrcode, etc.).

## High-level architecture / important invariants

- Single-process Flask app (`app.py`) is the authoritative server. It instantiates SQLAlchemy with a custom DeclarativeBase and calls `db.create_all()` on startup.
- Database: default is SQLite file `attendance.db` unless `DATABASE_URL` environment variable is provided. No migration framework is present.
- Models of interest: `Student`, `Teacher`, `Attendance` (all defined in `app.py`). Important fields and behavior:
  - `Student.get_id()` returns `student_{id}` and `Teacher.get_id()` returns `teacher_{id}`; the login loader splits `user_id` by underscore. Many flows rely on this exact format.
  - `Student.generate_qr_code()` creates PNG bytes stored in `student.qr_code` (LargeBinary) using the `qrcode` package. QR payloads look like `STUDENT_{id}_{email}` and are parsed by `/api/attendance/scan`.

## Key routes and patterns (copy these examples when writing or modifying code)

- Serving pages (static): GET `/` or `/index.html` -> `send_file('index.html')` (no template rendering).
- Signup: POST `/api/signup` accepts form or JSON fields `full_name`, `email`, `password`, `confirm_password` (or some alternative keys like `fullname`, `cpwd`). Returns JSON `{ success: true/false, message, redirect }`.
- Login: POST `/api/login` expects `email`, `pwd` (or `password`) and `user_type` (`student` or `teacher`). Special admin: `admin@teacher` / `system123` creates/logs in an admin `Teacher` account.
- Attendance scan: POST `/api/attendance/scan` with JSON `{ qr_data: 'STUDENT_123_email' }`. The endpoint toggles `check_in` / `check_out` based on today's last record.
- Student QR endpoints: `/api/student/<id>/qr-code` (download) and `/api/student/<id>/qr-image` (base64 payload).

## Conventions & gotchas an agent should know

- Many endpoints accept either JSON (application/json) or `application/x-www-form-urlencoded` form data; handlers use `request.get_json() if request.is_json else request.form`.
- Login accepts multiple field names (`pwd` or `password`) and the signup form also tolerates `fullname` / `full_name` and `cpwd` / `confirm_password` — preserve that flexibility when changing handlers or UI.
- Role checks: use `is_teacher(current_user)` or isinstance(current_user, `Student`) because `UserMixin` is used for both models. Do not assume `current_user` is a simple user table row.
- The `login_manager.user_loader` encodes type and id by splitting the stored id string; avoid changing `get_id()` or loader format unless you update all call sites.
- The app uses `app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'dev-secret-key-change-in-production')`. For production, set `FLASK_SECRET_KEY` and `DATABASE_URL`.

## How to run locally (PowerShell example)

1. Create and activate a virtual env:

   ```powershell
   python -m venv .\venv
   .\venv\Scripts\Activate.ps1
   ```

2. Install runtime deps (explicit list from `pyproject.toml`):

   ```powershell
   pip install flask flask-bcrypt flask-login flask-sqlalchemy psycopg2-binary python-dotenv "qrcode[pil]"
   ```

3. Run the app:

   ```powershell
   $env:FLASK_SECRET_KEY = 'dev' ; python .\app.py
   ```

Notes: app runs on port 5000 by default and will create `attendance.db` in the project root when first run.

## Tests, CI, and developer workflows

- No test framework or CI configuration was found. Be conservative when changing model schemas because no migrations are employed.
- For small changes, run the server and exercise the JSON endpoints via the browser UI (index uses `fetch`) or with PowerShell's `Invoke-RestMethod`/`curl`.

## Example API snippets (use same keys as the frontend)

- Login (PowerShell):

  ```powershell
  Invoke-RestMethod -Method Post -Uri http://localhost:5000/api/login -ContentType 'application/json' -Body (@{ email='user@example.com'; pwd='pass'; user_type='student' } | ConvertTo-Json)
  ```

- Scan attendance (teacher only):

  ```powershell
  Invoke-RestMethod -Method Post -Uri http://localhost:5000/api/attendance/scan -ContentType 'application/json' -Body (@{ qr_data='STUDENT_1_user@example.com' } | ConvertTo-Json)
  ```

## Files worth inspecting when coding

- `app.py` — all server logic, models, and routes (single source of truth).
- `index.html`, `accountcreate.html`, `admin.html`, `teacher.html`, `student.html` — static front-end pages that the Flask server serves with `send_file`.
- `CSS/*` — styles referenced by the static HTML.
- `pyproject.toml` — dependency list; use these names when installing packages.

## Quick security reminders for changes

- Don't leave `debug=True` or the default secret in production. The `__main__` block runs with `debug=True` currently.
- The admin bootstrap password `system123` is hard-coded in the login flow — if you change admin provisioning, update the logic accordingly.

If any part is unclear or you'd like the file to include more specific examples (tests, CI commands, or deployment notes), tell me which area to expand and I'll iterate.

## Developer manual (detailed)

See `MANUAL.txt` at the repository root for a full, step-by-step developer and operator manual. Key highlights here:

- Quick start (dev):
  1. Create a venv and activate (PowerShell):

     ```powershell
     python -m venv .\venv
     .\venv\Scripts\Activate.ps1
     pip install -r requirements.txt
     $env:FLASK_SECRET_KEY = 'dev' ; python .\app.py
     ```

- Use `run.ps1` (provided) to automate venv creation, installation, tests and running the app:

  - Run app: `.
un.ps1`
  - Run tests: `.
un.ps1 -Action test`

- DB and migrations: this project uses `SQLAlchemy` with `db.create_all()` and no migration system. Before changing models:
  - Backup `attendance.db` (if present) and run the tests locally using the in-memory DB (`tests/test_db.py`) to validate schema changes.
  - For production schema changes, add Alembic/Flask-Migrate and create explicit migrations.

- Admin seed: login with `admin@teacher` / `system123` will create an admin `Teacher` record automatically during login if it doesn't exist. Use this to bootstrap admin access.

- Tests & automation:
  - A lightweight test script is included at `tests/test_db.py` which uses an in-memory SQLite DB to verify model CRUD and QR generation.
  - A manual mobile/responsive checklist is at `tests/MOBILE_TESTS.md`.
  - For CI, add a job that creates a venv, installs `requirements.txt`, runs `python -m pytest` (after converting the current test script into pytest style) and lints the code.

- Frontend conventions & workflow:
  - Static pages live at the repository root and are served with `send_file`. They are plain HTML files (no Jinja templates).
  - Styles live under `CSS/`. Recent changes consolidated shared page styles into `CSS/pages.css`. Keep page-unique CSS small; prefer adding shared rules to `pages.css`.
  - A small JS helper `JS/mobile-nav.js` implements the mobile slide-out side menu. Use the DevTools device toolbar to validate responsive breakpoints: 1024px, 768px, 480px.

- Common pitfalls and gotchas:
  - Do NOT change `Student.get_id()` / `Teacher.get_id()` formats without updating the `login_manager.user_loader` and any code that parses `user_id`.
  - Endpoints accept either JSON or form data; preserve that pattern when adding new routes.
  - QR payload format is `STUDENT_{id}_{email}` — the scan endpoint expects this exact prefix.

## Troubleshooting & tips

- Can't import `app` in tests? Import by file path (tests use a loader that imports `app.py` directly to avoid module path issues).
- If the app creates an empty `attendance.db` unexpectedly, check `DATABASE_URL` env var and the working directory where `app.py` runs.
- To generate/regenerate a student's QR manually: open a Python REPL in the project with the venv active and run:

  ```python
  from app import app, db, Student
  with app.app_context():
      s = Student.query.get(1)
      s.generate_qr_code()
      db.session.commit()
  ```

## Next steps you can ask me to implement

- Convert tests to pytest and add them to a CI workflow (GitHub Actions).
- Add Flask-Migrate and scaffold a migration workflow; provide an `alembic` example for safe migrations.
- Harden production config (remove debug, require FLASK_SECRET_KEY and DATABASE_URL, add a basic `Procfile` or Dockerfile).

Refer to `MANUAL.txt` for a step-by-step walkthrough with examples, troubleshooting procedures, and deployment tips.
