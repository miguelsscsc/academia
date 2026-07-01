from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs
import html
import json
import os
import sqlite3
from datetime import datetime


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "checkins.sqlite3"
STATIC_DIR = BASE_DIR / "static"


def load_env_file():
    env_path = BASE_DIR / ".env"
    if not env_path.exists():
        return
    for line in env_path.read_text(encoding="utf-8").splitlines():
        clean_line = line.strip()
        if not clean_line or clean_line.startswith("#") or "=" not in clean_line:
            continue
        key, value = clean_line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


load_env_file()

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
SUPABASE_TABLE = os.environ.get("SUPABASE_TABLE", "checkins")

CLASS_LIMIT = 8
CLASS_TIMES = ["06:00", "07:00", "12:00", "18:00", "19:00", "20:00"]
_supabase_client = None


def use_supabase():
    return bool(SUPABASE_URL and SUPABASE_KEY)


def get_supabase_client():
    global _supabase_client
    if _supabase_client is None:
        try:
            from supabase import create_client
        except ImportError as exc:
            raise RuntimeError(
                "Instale a dependencia 'supabase' ou remova SUPABASE_URL/SUPABASE_KEY."
            ) from exc
        _supabase_client = create_client(SUPABASE_URL, SUPABASE_KEY)
    return _supabase_client


def init_db():
    if use_supabase():
        return
    DATA_DIR.mkdir(exist_ok=True)
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS checkins (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_name TEXT NOT NULL,
                class_time TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )


def get_counts():
    if use_supabase():
        rows = (
            get_supabase_client()
            .table(SUPABASE_TABLE)
            .select("class_time")
            .execute()
            .data
        )
        counts = {class_time: 0 for class_time in CLASS_TIMES}
        for row in rows:
            class_time = row.get("class_time")
            if class_time in counts:
                counts[class_time] += 1
        return counts

    with sqlite3.connect(DB_PATH) as conn:
        rows = conn.execute(
            "SELECT class_time, COUNT(*) FROM checkins GROUP BY class_time"
        ).fetchall()
    counts = {class_time: 0 for class_time in CLASS_TIMES}
    counts.update({class_time: total for class_time, total in rows})
    return counts


def get_recent_checkins():
    if use_supabase():
        rows = (
            get_supabase_client()
            .table(SUPABASE_TABLE)
            .select("student_name,class_time,created_at")
            .order("created_at", desc=True)
            .limit(20)
            .execute()
            .data
        )
        return [
            (
                row.get("student_name", ""),
                row.get("class_time", ""),
                row.get("created_at", ""),
            )
            for row in rows
        ]

    with sqlite3.connect(DB_PATH) as conn:
        rows = conn.execute(
            """
            SELECT student_name, class_time, created_at
            FROM checkins
            ORDER BY id DESC
            LIMIT 20
            """
        ).fetchall()
    return rows


def create_checkin(student_name, class_time):
    clean_name = " ".join(student_name.strip().split())
    if not clean_name:
        return False, "Informe o nome do aluno."
    if class_time not in CLASS_TIMES:
        return False, "Selecione um horario valido."

    if use_supabase():
        client = get_supabase_client()
        rows = (
            client.table(SUPABASE_TABLE)
            .select("id")
            .eq("class_time", class_time)
            .execute()
            .data
        )
        if len(rows) >= CLASS_LIMIT:
            return False, f"A turma das {class_time} ja atingiu o limite de {CLASS_LIMIT} alunos."

        client.table(SUPABASE_TABLE).insert(
            {
                "student_name": clean_name,
                "class_time": class_time,
                "created_at": datetime.now().isoformat(timespec="seconds"),
            }
        ).execute()
        return True, f"Check-in confirmado para {clean_name} as {class_time}."

    with sqlite3.connect(DB_PATH) as conn:
        total = conn.execute(
            "SELECT COUNT(*) FROM checkins WHERE class_time = ?", (class_time,)
        ).fetchone()[0]
        if total >= CLASS_LIMIT:
            return False, f"A turma das {class_time} ja atingiu o limite de {CLASS_LIMIT} alunos."

        conn.execute(
            """
            INSERT INTO checkins (student_name, class_time, created_at)
            VALUES (?, ?, ?)
            """,
            (clean_name, class_time, datetime.now().isoformat(timespec="seconds")),
        )
    return True, f"Check-in confirmado para {clean_name} as {class_time}."


def render_home(message=None, success=True):
    try:
        counts = get_counts()
        recent = get_recent_checkins()
    except Exception:
        counts = {class_time: 0 for class_time in CLASS_TIMES}
        recent = []
        message = "Nao foi possivel conectar ao banco de dados."
        success = False

    time_options = "\n".join(
        f'<option value="{class_time}">{class_time} - {counts[class_time]}/{CLASS_LIMIT} vagas</option>'
        for class_time in CLASS_TIMES
    )
    cards = "\n".join(
        f"""
        <article class="slot">
            <strong>{class_time}</strong>
            <span>{counts[class_time]} de {CLASS_LIMIT} vagas</span>
            <meter min="0" max="{CLASS_LIMIT}" value="{counts[class_time]}"></meter>
        </article>
        """
        for class_time in CLASS_TIMES
    )
    rows = "\n".join(
        f"""
        <tr>
            <td>{html.escape(name)}</td>
            <td>{html.escape(class_time)}</td>
            <td>{html.escape(created_at.replace("T", " "))}</td>
        </tr>
        """
        for name, class_time, created_at in recent
    )
    if not rows:
        rows = '<tr><td colspan="3">Nenhum check-in registrado ainda.</td></tr>'

    alert = ""
    if message:
        alert_class = "success" if success else "error"
        alert = f'<p class="alert {alert_class}">{html.escape(message)}</p>'

    return f"""<!doctype html>
<html lang="pt-BR">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Forca & Foco - Check-in</title>
    <link rel="stylesheet" href="/static/styles.css">
</head>
<body>
    <main class="app">
        <section class="panel">
            <div>
                <p class="eyebrow">Forca & Foco</p>
                <h1>Check-in de aulas</h1>
            </div>
            {alert}
            <form method="post" action="/checkin">
                <label for="student_name">Nome do aluno</label>
                <input id="student_name" name="student_name" maxlength="80" required autocomplete="name">

                <label for="class_time">Horario desejado</label>
                <select id="class_time" name="class_time" required>
                    {time_options}
                </select>

                <button type="submit">Confirmar check-in</button>
            </form>
        </section>

        <section class="panel">
            <h2>Ocupacao das turmas</h2>
            <div class="slots">
                {cards}
            </div>
        </section>

        <section class="panel wide">
            <h2>Ultimos check-ins</h2>
            <table>
                <thead>
                    <tr>
                        <th>Aluno</th>
                        <th>Horario</th>
                        <th>Registro</th>
                    </tr>
                </thead>
                <tbody>{rows}</tbody>
            </table>
        </section>
    </main>
</body>
</html>"""


class AppHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/" or self.path.startswith("/?"):
            self.respond_html(render_home())
            return
        if self.path == "/api/health":
            database_ok = False
            try:
                if use_supabase():
                    get_supabase_client().table(SUPABASE_TABLE).select("id").limit(1).execute()
                    database_ok = True
                else:
                    database_ok = DB_PATH.exists()
            except Exception:
                database_ok = False
            self.respond_json(
                {
                    "status": "ok",
                    "database": database_ok,
                    "database_provider": "supabase" if use_supabase() else "sqlite",
                    "class_limit": CLASS_LIMIT,
                    "checked_at": datetime.now().isoformat(timespec="seconds"),
                }
            )
            return
        if self.path == "/static/styles.css":
            self.respond_static(STATIC_DIR / "styles.css", "text/css; charset=utf-8")
            return
        self.send_error(404)

    def do_POST(self):
        if self.path != "/checkin":
            self.send_error(404)
            return

        length = int(self.headers.get("Content-Length", "0"))
        form = parse_qs(self.rfile.read(length).decode("utf-8"))
        success, message = create_checkin(
            form.get("student_name", [""])[0],
            form.get("class_time", [""])[0],
        )
        self.respond_html(render_home(message, success))

    def respond_html(self, body):
        encoded = body.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)

    def respond_json(self, payload):
        encoded = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)

    def respond_static(self, file_path, content_type):
        if not file_path.exists():
            self.send_error(404)
            return
        encoded = file_path.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)

    def log_message(self, format, *args):
        print("[%s] %s" % (self.log_date_time_string(), format % args))


def run(host="0.0.0.0", port=8000):
    init_db()
    server = ThreadingHTTPServer((host, port), AppHandler)
    print(f"Sistema Forca & Foco disponivel em http://{host}:{port}")
    server.serve_forever()


if __name__ == "__main__":
    run()
