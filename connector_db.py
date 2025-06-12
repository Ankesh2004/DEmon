import sqlite3

class DemonDB:
    def __init__(self):
        self.dbname = "demonDB.db"
        self.connection = None
        self.cursor = None
        self.create_carbon_emissions_table()

    def create_carbon_emissions_table(self):
        try:
            self.connection = sqlite3.connect(self.dbname, check_same_thread=False)
            self.cursor = self.connection.cursor()
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS carbon_emissions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    run_id INTEGER,
                    ip TEXT,
                    port TEXT,
                    round INTEGER,
                    current_emission_rate REAL,
                    total_emission REAL,
                    power_consumption REAL,
                    timestamp REAL,
                    FOREIGN KEY (run_id) REFERENCES run (id)
                )
            """)
            self.connection.commit()
            self.connection.close()
        except Exception as e:
            print("Error creating carbon_emissions table: {}".format(e))

    def get_carbon_emissions_by_run(self, run_id):
        try:
            self.connection = sqlite3.connect(self.dbname, check_same_thread=False)
            self.cursor = self.connection.cursor()
            self.cursor.execute(
                "SELECT ip, port, round, current_emission_rate, total_emission, power_consumption, timestamp FROM carbon_emissions WHERE run_id = ? ORDER BY timestamp",
                (run_id,))
            emissions = self.cursor.fetchall()
            self.connection.close()
            return emissions
        except Exception as e:
            print("Error DB Query: {}".format(e))
            return []

    def get_average_emissions_per_node(self, run_id):
        try:
            self.connection = sqlite3.connect(self.dbname, check_same_thread=False)
            self.cursor = self.connection.cursor()
            self.cursor.execute(
                "SELECT ip, port, AVG(current_emission_rate), AVG(power_consumption), MAX(total_emission) FROM carbon_emissions WHERE run_id = ? GROUP BY ip, port",
                (run_id,))
            avg_emissions = self.cursor.fetchall()
            self.connection.close()
            return avg_emissions
        except Exception as e:
            print("Error DB Query: {}".format(e))
            return []