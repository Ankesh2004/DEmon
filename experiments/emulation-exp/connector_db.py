import sqlite3
import configparser
import traceback

parser = configparser.ConfigParser()
parser.read('demonMonitoring.ini')

def get_connection():
    try:
        return sqlite3.connect('./new_folder/demonDB.db', check_same_thread=False)
    except Exception as e:
        print("Error connecting to demonDB: {}".format(e))
        return None

def insert_into_round_of_node(run_id, ip, port, this_round, nd, fd, rm, ic, bytes_of_data, connection):
    try:
        connection = get_connection()
        if not connection:
            return False
        cursor = connection.cursor()
        cursor.execute("DELETE FROM round_of_node WHERE run_id = ? AND ip = ? AND port = ? AND round = ?",
                       (run_id, ip, port, this_round))
        cursor.execute("INSERT INTO round_of_node ("
                       "run_id,"
                       "ip,"
                       "port,"
                       "round,"
                       "nd,"
                       "fd,"
                       "rm,"
                       "ic,"
                       "bytes_of_data) "
                       "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                       (run_id,
                        ip,
                        port,
                        this_round,
                        nd,
                        fd,
                        rm,
                        ic,
                        bytes_of_data))
        connection.commit()
        connection.close()
        return True
    except Exception as e:
        print("Error db: {}".format(e))
        print("Trace: {}".format(traceback.format_exc()))
        return False

def insert_into_round_of_node_max_round(run_id, ip, port, this_round, nd, fd, rm, ic, bytes_of_data, connection):
    try:
        connection = get_connection()
        if not connection:
            return False
        cursor = connection.cursor()
        cursor.execute("DELETE FROM round_of_node_max_round WHERE run_id = ? AND ip = ? AND port = ? AND round = ?",
                       (run_id, ip, port, this_round))
        cursor.execute("INSERT INTO round_of_node_max_round ("
                       "run_id,"
                       "ip,"
                       "port,"
                       "round,"
                       "nd,"
                       "fd,"
                       "rm,"
                       "ic,"
                       "bytes_of_data) "
                       "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                       (run_id,
                        ip,
                        port,
                        this_round,
                        nd,
                        fd,
                        rm,
                        ic,
                        bytes_of_data))
        connection.commit()
        connection.close()
        return True
    except Exception as e:
        print("Error db: {}".format(e))
        print("Trace: {}".format(traceback.format_exc()))
        return False

class NodeDB:
    def __init__(self):
        try:
            self.connection = sqlite3.connect('./new_folder/NodeStorage.db', check_same_thread=False)
            self.cursor = self.connection.cursor()
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS unique_entries (
                    id INTEGER PRIMARY KEY,
                    key TEXT,
                    value TEXT
                )
            ''')
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS data_entries (
                    id INTEGER PRIMARY KEY,
                    node TEXT,
                    round INTEGER,
                    key TEXT,
                    unique_entry_id INTEGER,
                    FOREIGN KEY (unique_entry_id) REFERENCES unique_entries(id)
                )
            ''')
            self.connection.commit()
            self.connection.close()
        except Exception as e:
            print("Error initializing NodeDB: {}".format(e))
            print("Trace: {}".format(traceback.format_exc()))

    def get_connection(self):
        try:
            return sqlite3.connect('./new_folder/NodeStorage.db', check_same_thread=False)
        except Exception as e:
            print("Error connecting to NodeStorage: {}".format(e))
            return None

class DemonDB:
    def __init__(self):
        try:
            self.connection = sqlite3.connect('./new_folder/demonDB.db', check_same_thread=False)
            self.cursor = self.connection.cursor()
            self.cursor.execute(
                "CREATE TABLE IF NOT EXISTS experiment ("
                "id INTEGER PRIMARY KEY AUTOINCREMENT, "
                "timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)")
            self.cursor.execute(
                "CREATE TABLE IF NOT EXISTS run ("
                "id INTEGER PRIMARY KEY AUTOINCREMENT, "
                "experiment_id INTEGER REFERENCES experiment(id), "
                "run_count INTEGER, "
                "node_count INTEGER, "
                "gossip_rate REAL, "
                "target_count INTEGER, "
                "convergence_round INTEGER, "
                "convergence_message_count INTEGER, "
                "convergence_time REAL)"
            )
            self.cursor.execute(
                "CREATE TABLE IF NOT EXISTS round_of_node ("
                "id INTEGER PRIMARY KEY AUTOINCREMENT, "
                "run_id BIGINT REFERENCES run(id), "
                "ip TEXT, "
                "port TEXT, "
                "round INTEGER, "
                "nd INTEGER, "
                "fd INTEGER, "
                "rm INTEGER, "
                "ic INTEGER, "
                "bytes_of_data INTEGER)")
            self.cursor.execute(
                "CREATE TABLE IF NOT EXISTS round_of_node_max_round ("
                "id INTEGER PRIMARY KEY AUTOINCREMENT, "
                "run_id BIGINT REFERENCES run(id), "
                "ip TEXT, "
                "port TEXT, "
                "round INTEGER, "
                "nd INTEGER, "
                "fd INTEGER, "
                "rm INTEGER, "
                "ic INTEGER, "
                "bytes_of_data INTEGER)")
            self.cursor.execute(
                "CREATE TABLE IF NOT EXISTS query ("
                "id INTEGER PRIMARY KEY AUTOINCREMENT, "
                "run_id BIGINT REFERENCES run(id), "
                "node_count INTEGER, "
                "query_num INTEGER,"
                "failure_percent REAL, "
                "time_to_query REAL, "
                "total_messages_for_query INTEGER, "
                "success TEXT)"
            )
            self.connection.commit()
            self.connection.close()
        except Exception as e:
            print("Error initializing DemonDB: {}".format(e))
            print("Trace: {}".format(traceback.format_exc()))

    def insert_into_experiment(self, timestamp):
        try:
            self.connection = sqlite3.connect('./new_folder/demonDB.db', check_same_thread=False)
            self.cursor = self.connection.cursor()
            self.cursor.execute("INSERT INTO experiment (timestamp) VALUES (?)", (timestamp,))
            to_return = self.cursor.lastrowid
            self.connection.commit()
            self.connection.close()
            return to_return
        except Exception as e:
            print("Error DB Insert experiment: {}".format(e))
            print("Trace: {}".format(traceback.format_exc()))
            return -1

    def insert_into_run(self, experiment_id, run_count, node_count, gossip_rate, target_count):
        try:
            self.connection = sqlite3.connect('./new_folder/demonDB.db', check_same_thread=False)
            self.cursor = self.connection.cursor()
            self.cursor.execute("INSERT INTO run ("
                                "experiment_id,"
                                "run_count, "
                                "node_count, "
                                "gossip_rate, "
                                "target_count) "
                                "VALUES (?, ?, ?, ?, ?)",
                                (experiment_id,
                                 run_count,
                                 node_count,
                                 gossip_rate,
                                 target_count))
            to_return = self.cursor.lastrowid
            self.connection.commit()
            self.connection.close()
            return to_return
        except Exception as e:
            print("Error DB Insert run: {}".format(e))
            print("Trace: {}".format(traceback.format_exc()))
            return -1

    def save_query_in_database(self, run_id, node_count, i, failure_percent, time_to_query, total_messages_for_query,
                              success):
        try:
            connection = get_connection()
            if not connection:
                return False
            cursor = connection.cursor()
            cursor.execute(
                "INSERT INTO query ("
                "run_id,"
                "node_count, "
                "query_num,"
                "failure_percent, "
                "time_to_query, "
                "total_messages_for_query, "
                "success)"
                "VALUES (?, ?, ?, ?, ?, ?, ?)",
                (run_id,
                 node_count,
                 i,
                 failure_percent,
                 time_to_query,
                 total_messages_for_query,
                 success))
            connection.commit()
            connection.close()
            return True
        except Exception as e:
            print("Exception in save_query_in_database: {}".format(e))
            print("Trace: {}".format(traceback.format_exc()))
            return False

    def insert_into_converged_run(self, run_id, convergence_round, convergence_message_count, convergence_time):
        try:
            self.connection = sqlite3.connect('./new_folder/demonDB.db', check_same_thread=False)
            self.cursor = self.connection.cursor()
            self.cursor.execute("UPDATE run SET "
                                "convergence_round = ?, "
                                "convergence_message_count = ?, "
                                "convergence_time = ? "
                                "WHERE id = ?",
                                (convergence_round,
                                 convergence_message_count,
                                 convergence_time,
                                 run_id))
            self.connection.commit()
            self.connection.close()
            return run_id
        except Exception as e:
            print("Error DB Update run: {}".format(e))
            print("Trace: {}".format(traceback.format_exc()))
            return -1