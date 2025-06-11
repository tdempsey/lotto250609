from flask import Flask, render_template
import pymysql
from datetime import datetime

app = Flask(__name__)

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'ga_f5_lotto',
    'cursorclass': pymysql.cursors.DictCursor
}

# ----------------------------------------------------------------------
# Database helpers
# ----------------------------------------------------------------------

def get_connection():
    return pymysql.connect(**DB_CONFIG)


def create_table(conn, table_name, columns, drop_if_exists=False):
    with conn.cursor() as cur:
        if drop_if_exists:
            cur.execute(f"DROP TABLE IF EXISTS `{table_name}`")
        cols = ", ".join(columns)
        cur.execute(
            f"CREATE TABLE IF NOT EXISTS `{table_name}` ({cols}) "
            "ENGINE=InnoDB DEFAULT CHARSET=utf8mb4"
        )
    conn.commit()


def temp1_columns():
    return [
        "`id` int(10) unsigned NOT NULL auto_increment",
        "`sum` int(3) unsigned NOT NULL default '0'",
        "`even` tinyint(1) unsigned NOT NULL default '0'",
        "`odd` tinyint(1) unsigned NOT NULL default '0'",
        "`k_count` tinyint(2) unsigned NOT NULL default '0'",
        "`last_updated` date NOT NULL default '1962-08-17'",
        "PRIMARY KEY (`id`)"
    ]


def standard_columns():
    return [
        "`id` int(10) unsigned NOT NULL auto_increment",
        "`b1` tinyint(2) unsigned NOT NULL default '0'",
        "`b2` tinyint(2) unsigned NOT NULL default '0'",
        "`b3` tinyint(2) unsigned NOT NULL default '0'",
        "`b4` tinyint(2) unsigned NOT NULL default '0'",
        "`b5` tinyint(2) unsigned NOT NULL default '0'",
        "`sum` int(5) unsigned NOT NULL default '0'",
        "`hml` int(3) unsigned NOT NULL default '0'",
        "`even` tinyint(1) unsigned NOT NULL default '0'",
        "`odd` tinyint(1) unsigned NOT NULL default '0'",
        "`d0` tinyint(1) unsigned NOT NULL default '0'",
        "`d1` tinyint(1) unsigned NOT NULL default '0'",
        "`d2` tinyint(1) unsigned NOT NULL default '0'",
        "`d3` tinyint(1) unsigned NOT NULL default '0'",
        "`d4` tinyint(1) unsigned NOT NULL default '0'",
        "`rank0` tinyint(1) unsigned NOT NULL default '0'",
        "`rank1` tinyint(1) unsigned NOT NULL default '0'",
        "`rank2` tinyint(1) unsigned NOT NULL default '0'",
        "`rank3` tinyint(1) unsigned NOT NULL default '0'",
        "`rank4` tinyint(1) unsigned NOT NULL default '0'",
        "`rank5` tinyint(1) unsigned NOT NULL default '0'",
        "`rank6` tinyint(1) unsigned NOT NULL default '0'",
        "`rank7` tinyint(1) unsigned NOT NULL default '0'",
        "`mod_tot` tinyint(1) unsigned NOT NULL default '0'",
        "`mod_x` tinyint(1) unsigned NOT NULL default '0'",
        "`seq2` tinyint(1) unsigned NOT NULL default '0'",
        "`seq3` tinyint(1) unsigned NOT NULL default '0'",
        "`comb2` tinyint(1) unsigned NOT NULL default '0'",
        "`comb3` tinyint(1) unsigned NOT NULL default '0'",
        "`comb4` tinyint(1) unsigned NOT NULL default '0'",
        "`comb5` tinyint(1) unsigned NOT NULL default '0'",
        "`dup1` tinyint(1) unsigned NOT NULL default '0'",
        "`dup2` tinyint(1) unsigned NOT NULL default '0'",
        "`dup3` tinyint(1) unsigned NOT NULL default '0'",
        "`dup4` tinyint(1) unsigned NOT NULL default '0'",
        "`dup5` tinyint(1) unsigned NOT NULL default '0'",
        "`dup6` tinyint(1) unsigned NOT NULL default '0'",
        "`dup7` tinyint(1) unsigned NOT NULL default '0'",
        "`dup8` tinyint(1) unsigned NOT NULL default '0'",
        "`dup9` tinyint(1) unsigned NOT NULL default '0'",
        "`dup10` tinyint(1) unsigned NOT NULL default '0'",
        "`pair_sum` mediumint(8) unsigned NOT NULL default '0'",
        "`avg` float(4,2) unsigned NOT NULL default '0.00'",
        "`median` float(4,2) unsigned NOT NULL default '0.00'",
        "`harmean` float(4,2) unsigned NOT NULL default '0.00'",
        "`geomean` float(4,2) unsigned NOT NULL default '0.00'",
        "`quart1` float(4,2) unsigned NOT NULL default '0.00'",
        "`quart2` float(4,2) unsigned NOT NULL default '0.00'",
        "`quart3` float(4,2) unsigned NOT NULL default '0.00'",
        "`stdev` float(4,2) unsigned NOT NULL default '0.00'",
        "`variance` float(6,2) unsigned NOT NULL default '0.00'",
        "`avedev` float(4,2) unsigned NOT NULL default '0.00'",
        "`kurt` float(4,2) NOT NULL default '0.00'",
        "`skew` float(4,2) NOT NULL default '0.00'",
        "`devsq` float(6,2) unsigned NOT NULL default '0.00'",
        "`wheel_cnt5000` mediumint(5) unsigned NOT NULL default '0'",
        "`wheel_percent_wa` float(4,2) unsigned NOT NULL default '0.00'",
        "`draw_last` date NOT NULL default '1962-08-17'",
        "`draw_count` tinyint(3) unsigned NOT NULL default '0'",
        "`y1_sum` float(4,2) NOT NULL default '0.00'",
        "`last_updated` date NOT NULL default '1962-08-17'",
        "PRIMARY KEY (`id`)"
    ]


def setup_tables(conn, temp_table1, temp_table2, temp_table4, drop_tables=True):
    if drop_tables:
        create_table(conn, temp_table1, temp1_columns(), drop_if_exists=True)
        create_table(conn, temp_table2, standard_columns(), drop_if_exists=True)
    create_table(conn, temp_table4, standard_columns(), drop_if_exists=drop_tables)

# ----------------------------------------------------------------------
# Count building logic translated from scaffolding_count.incl
# ----------------------------------------------------------------------

def build_sumx_count(conn):
    sumx_count = [0] * 30
    with conn.cursor() as cur:
        cur.execute("SELECT numx, percent_wa FROM ga_f5_sum WHERE percent_wa > 0.0 ORDER BY percent_wa DESC")
        for row in cur.fetchall():
            t = int(row['numx'])
            sumx_count[t] = float(row['percent_wa']) * 10
    temp_count = sum(sumx_count)
    s = 9
    while temp_count < 1000:
        sumx_count[s] += 1
        temp_count = sum(sumx_count)
        s += 1
    return sumx_count


def insert_k_count(cur, table, row, k):
    cur.execute(
        f"INSERT INTO {table} (sum, even, odd, k_count, last_updated) VALUES (%s,%s,%s,%s,'1962-08-17')",
        (row['numx'], row['even'], row['odd'], k)
    )


def build_percent_table(conn, sumx_count, temp_table1, drop_tables=True):
    date_diff = (datetime.now().date() - datetime(2015, 10, 1).date()).days
    count_all = 0
    with conn.cursor() as cur:
        ranges = [
            (5, 7, 25, False),
            (8, 13, 65, True),
            (14, 17, 65, False)
        ]
        for start, end, arr_len, require_min in ranges:
            for x in range(start, end + 1):
                y = x * 10
                z = y + 9
                table_name = f"ga_f5_sum_count_sum_{date_diff-1}"
                query = f"SELECT * FROM {table_name} WHERE numx >= {y} AND numx <= {z}"
                if require_min:
                    query += " AND percent_wa >= 0.5"
                query += " ORDER BY percent_wa DESC"
                cur.execute(query)
                rows = cur.fetchall()
                if not rows:
                    continue
                wa_sum = sum(float(r['percent_wa']) for r in rows)
                k_array = [0] * arr_len
                idx = 0
                for r in rows:
                    percent = float(r['percent_wa']) / wa_sum * 100
                    temp = round(percent, 2)
                    index_sumx = int(int(r['numx'])/10)
                    k = int((int(temp + 0.5) / 100) * sumx_count[index_sumx])
                    k_array[idx] = k
                    if k > 0 and drop_tables:
                        insert_k_count(cur, temp_table1, r, k)
                    idx += 1
                s = 0
                while sum(k_array) < sumx_count[index_sumx]:
                    k_array[s] += 1
                    s = (s + 1) % len(k_array)
                count_all += sum(k_array)
    conn.commit()
    return count_all

# ----------------------------------------------------------------------
# Flask Routes
# ----------------------------------------------------------------------

@app.route('/build')
def build():
    currdate = datetime.now().strftime('%y%m%d')
    temp_table1 = f"temp_cover_1k_count_{currdate}"
    temp_table2 = f"temp_cover_1k_scaffolding_135_{currdate}"
    temp_table4 = f"temp_cover_1k_candidates_scaffolding_{currdate}"

    conn = get_connection()
    try:
        setup_tables(conn, temp_table1, temp_table2, temp_table4, drop_tables=True)
        sumx = build_sumx_count(conn)
        total = build_percent_table(conn, sumx, temp_table1, drop_tables=True)
    finally:
        conn.close()

    message = f"{temp_table1} built with total count {total}."
    return render_template('build.html', message=message)

if __name__ == '__main__':
    app.run(debug=True)

