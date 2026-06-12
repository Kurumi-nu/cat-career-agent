from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse
import json
import mimetypes
import sqlite3


ROOT = Path(__file__).parent.resolve()
DB_PATH = ROOT / "miranoa.db"
PORT = 8000


SPOTS = [
    ("ランタン運河", "名所", "旧市街", "夕暮れ", 4.9, "街の中心を流れる全長4.2kmの運河。橋ごとに灯るランタンが水面に映り、ミラノアらしい夜景を作ります。", "夕暮れ以降", "中央桟橋から徒歩4分", "/images/spots/lantern-canal.png"),
    ("風見の観測塔", "名所", "丘陵区", "展望", 4.7, "旧港、新市街、内海を一望できる高さ86mの展望塔。屋上の風見盤は街の象徴です。", "20:00前後", "水上トラムT2線 終点", "/images/spots/observatory-tower.png"),
    ("北桟橋市場", "食", "北桟橋", "朝市", 4.6, "魚介、柑橘、焼き菓子が並ぶ朝市。旅人には焼きレモンのパンと港のスープが人気です。", "6:00-9:00", "中央駅から徒歩12分", "/images/spots/north-pier-market.png"),
    ("硝子屋根の回廊", "建築", "旧市街", "雨の日", 4.5, "商店街と美術館をつなぐ透明な屋根の歩道。雨の日は石畳に光がやわらかく落ちます。", "午後", "市庁舎前から徒歩2分", "/images/spots/glass-arcade.png"),
    ("潮風植物園", "自然", "南岸", "散策", 4.3, "海辺の植物だけを集めた庭園。午前中は香りが濃く、静かな散策に向いています。", "午前中", "電気バスB4線 植物園前", "/images/spots/botanical-garden.png"),
    ("月波温浴場", "体験", "南岸", "夜", 4.4, "観光後に立ち寄れる公共浴場。丸窓から運河の灯りが見える浴室が名物です。", "21:00以降", "水上トラムT1線 月波前", "/images/spots/moonwave-bath.png"),
    ("回廊美術館", "文化", "美術区", "屋内", 4.2, "ガラス回廊の途中にある小さな美術館。港町の設計図や古い航海日誌も展示されています。", "雨の日", "硝子屋根の回廊内", "/images/spots/arcade-museum.png"),
    ("灯台広場", "名所", "旧港", "夜市", 4.8, "毎月17日に夜市が開かれる広場。小皿料理の屋台と手仕事の露店が22時まで並びます。", "毎月17日", "中央桟橋から徒歩7分", "/images/spots/lighthouse-square.png"),
]


EVENTS = [
    ("水鏡の花舟", "春", "4月上旬", "春の花を積んだ小舟が旧市街をゆっくり巡る季節行事です。"),
    ("海風映画祭", "夏", "8月最終週", "港の倉庫壁をスクリーンにした屋外上映会。夜風が気持ちよい時期に開催されます。"),
    ("ランタン点灯週間", "秋", "11月中旬", "橋、窓辺、船着場に手作りランタンが灯る、ミラノアで最も人気のある一週間です。"),
    ("回廊の夜市", "毎月", "毎月17日", "灯台広場に小皿料理と工芸品の店が並ぶ月例マーケットです。"),
]


def connect():
    return sqlite3.connect(DB_PATH)


def init_db():
    with connect() as db:
        db.execute(
            """
            CREATE TABLE IF NOT EXISTS places (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                category TEXT NOT NULL,
                area TEXT NOT NULL,
                tag TEXT NOT NULL,
                rating REAL NOT NULL,
                description TEXT NOT NULL,
                best_time TEXT NOT NULL,
                access TEXT NOT NULL,
                image TEXT NOT NULL DEFAULT ''
            )
            """
        )
        columns = [row[1] for row in db.execute("PRAGMA table_info(places)").fetchall()]
        if "image" not in columns:
            db.execute("ALTER TABLE places ADD COLUMN image TEXT NOT NULL DEFAULT ''")
        db.execute(
            """
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                season TEXT NOT NULL,
                date_label TEXT NOT NULL,
                description TEXT NOT NULL
            )
            """
        )
        place_count = db.execute("SELECT COUNT(*) FROM places").fetchone()[0]
        if place_count == 0:
            db.executemany(
                """
                INSERT INTO places
                    (name, category, area, tag, rating, description, best_time, access, image)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                SPOTS,
            )
        else:
            db.executemany("UPDATE places SET image = ? WHERE name = ?", [(spot[8], spot[0]) for spot in SPOTS])
        event_count = db.execute("SELECT COUNT(*) FROM events").fetchone()[0]
        if event_count == 0:
            db.executemany(
                "INSERT INTO events (name, season, date_label, description) VALUES (?, ?, ?, ?)",
                EVENTS,
            )


def rows_to_dicts(cursor):
    columns = [column[0] for column in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]


def get_places(params):
    category = params.get("category", ["all"])[0]
    query = params.get("q", [""])[0].strip()
    sql = "SELECT * FROM places WHERE 1 = 1"
    args = []
    if category != "all":
        sql += " AND category = ?"
        args.append(category)
    if query:
        sql += " AND (name LIKE ? OR area LIKE ? OR tag LIKE ? OR description LIKE ?)"
        like = f"%{query}%"
        args.extend([like, like, like, like])
    sql += " ORDER BY rating DESC, name ASC"
    with connect() as db:
        return rows_to_dicts(db.execute(sql, args))


def get_place(place_id):
    with connect() as db:
        cursor = db.execute("SELECT * FROM places WHERE id = ?", (place_id,))
        rows = rows_to_dicts(cursor)
        return rows[0] if rows else None


def get_related_places(place):
    with connect() as db:
        cursor = db.execute(
            """
            SELECT id, name, category, area, rating, image
            FROM places
            WHERE id != ? AND (category = ? OR area = ?)
            ORDER BY rating DESC, name ASC
            LIMIT 3
            """,
            (place["id"], place["category"], place["area"]),
        )
        return rows_to_dicts(cursor)


def get_events():
    with connect() as db:
        return rows_to_dicts(db.execute("SELECT * FROM events ORDER BY id ASC"))


def get_stats():
    with connect() as db:
        categories = rows_to_dicts(
            db.execute("SELECT category, COUNT(*) AS count FROM places GROUP BY category ORDER BY category")
        )
        total_places = db.execute("SELECT COUNT(*) FROM places").fetchone()[0]
        avg_rating = db.execute("SELECT ROUND(AVG(rating), 1) FROM places").fetchone()[0]
        return {"totalPlaces": total_places, "averageRating": avg_rating, "categories": categories}


class MiranoaHandler(BaseHTTPRequestHandler):
    def send_json(self, data, status=200):
        payload = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def send_file(self, path):
        if not path.exists() or not path.is_file():
            self.send_error(404)
            return
        content = path.read_bytes()
        content_type = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
        if path.suffix == ".html":
            content_type = "text/html; charset=utf-8"
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)

    def send_file_headers(self, path):
        if not path.exists() or not path.is_file():
            self.send_error(404)
            return
        content_type = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
        if path.suffix == ".html":
            content_type = "text/html; charset=utf-8"
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(path.stat().st_size))
        self.end_headers()

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == "/":
            self.send_file(ROOT / "index.html")
            return
        if parsed.path.startswith("/places/"):
            self.send_file(ROOT / "detail.html")
            return
        if parsed.path == "/api/places":
            self.send_json(get_places(parse_qs(parsed.query)))
            return
        if parsed.path.startswith("/api/places/"):
            try:
                place_id = int(parsed.path.rsplit("/", 1)[1])
            except ValueError:
                self.send_json({"error": "Invalid place id"}, 400)
                return
            place = get_place(place_id)
            if place is None:
                self.send_json({"error": "Place not found"}, 404)
                return
            self.send_json({"place": place, "related": get_related_places(place)})
            return
        if parsed.path == "/api/events":
            self.send_json(get_events())
            return
        if parsed.path == "/api/stats":
            self.send_json(get_stats())
            return
        if parsed.path.startswith("/images/"):
            safe_path = (ROOT / parsed.path.lstrip("/")).resolve()
            if ROOT in safe_path.parents:
                self.send_file(safe_path)
                return
        self.send_error(404)

    def do_HEAD(self):
        parsed = urlparse(self.path)
        if parsed.path == "/":
            self.send_file_headers(ROOT / "index.html")
            return
        if parsed.path.startswith("/places/"):
            self.send_file_headers(ROOT / "detail.html")
            return
        if parsed.path.startswith("/images/"):
            safe_path = (ROOT / parsed.path.lstrip("/")).resolve()
            if ROOT in safe_path.parents:
                self.send_file_headers(safe_path)
                return
        self.send_error(404)

    def log_message(self, format, *args):
        print("%s - %s" % (self.address_string(), format % args))


def main():
    init_db()
    server = ThreadingHTTPServer(("127.0.0.1", PORT), MiranoaHandler)
    print(f"Miranoa app running at http://127.0.0.1:{PORT}")
    print(f"SQLite database: {DB_PATH}")
    server.serve_forever()


if __name__ == "__main__":
    main()
