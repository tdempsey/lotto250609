# GA F5 1K 1/3/5 Cover (Flask)

This directory provides a minimal Flask application that ports the PHP
script `lot_cover_ga_f5_1k_1_3_5.php` up to the point where the
scaffolding counts are built. It connects to the `ga_f5_lotto` database
and reproduces the logic found in `includes_ga_f5/scaffolding_count.incl`
to generate the initial 1000 count table.

## Running

Install the requirements from the project root:

```bash
pip install -r ../requirements.txt
```

Run the application:

```bash
python app.py
```

Navigate to `http://127.0.0.1:5000/build` to execute the count-building
routine.
