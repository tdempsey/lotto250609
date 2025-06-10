# GA F5 1K Cover (Flask)

This directory contains a small Flask application that replicates the
behaviour of the original PHP script `check_ga_f5_1k_cover.php`.
It connects to the `ga_f5_lotto` database, checks the previous day's
winning numbers and compares them against the rows in the dynamic table
`temp_cover_1k_scaffolding_135_<date>`.

## Running

Install the required dependencies (Flask and PyMySQL):

```bash
pip install -r ../requirements.txt
```

Run the app:

```bash
python app.py
```

Then open `http://127.0.0.1:5000/check` in your browser to see the
coverage results.
