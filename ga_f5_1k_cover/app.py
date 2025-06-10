from flask import Flask, render_template
import pymysql
from datetime import datetime, timedelta

app = Flask(__name__)

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'ga_f5_lotto',
    'cursorclass': pymysql.cursors.DictCursor
}

def get_connection():
    return pymysql.connect(**DB_CONFIG)

@app.route('/')
def index():
    return "GA F5 1K Cover"

@app.route('/check')
def check_cover():
    prev_date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    drawdate = (datetime.now() - timedelta(days=1)).strftime('%y%m%d')
    temp_table = f"temp_cover_1k_scaffolding_135_{drawdate}"

    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT b1,b2,b3,b4,b5 FROM ga_f5_draws WHERE date=%s LIMIT 1",
                (prev_date,)
            )
            row = cursor.fetchone()
            if not row:
                return f"No draw found for {prev_date}"
            winning_numbers = [row['b1'], row['b2'], row['b3'], row['b4'], row['b5']]

            cursor.execute(
                f"SELECT id,b1,b2,b3,b4,b5 FROM {temp_table} ORDER BY id ASC"
            )
            rows = cursor.fetchall()
    finally:
        conn.close()

    two_wins = three_wins = four_wins = five_wins = 0
    results = []
    for r in rows:
        numbers_in_row = [r['b1'], r['b2'], r['b3'], r['b4'], r['b5']]
        match_count = len(set(winning_numbers) & set(numbers_in_row))
        results.append({'id': r['id'], 'numbers': numbers_in_row, 'match': match_count})
        if match_count == 2:
            two_wins += 1
        elif match_count == 3:
            three_wins += 1
        elif match_count == 4:
            four_wins += 1
        elif match_count == 5:
            five_wins += 1

    return render_template(
        'results.html',
        prev_date=prev_date,
        winning_numbers=winning_numbers,
        results=results,
        two_wins=two_wins,
        three_wins=three_wins,
        four_wins=four_wins,
        five_wins=five_wins,
    )

if __name__ == '__main__':
    app.run(debug=True)
