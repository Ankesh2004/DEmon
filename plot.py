import sqlite3
import matplotlib.pyplot as plt

dbname = 'experiments.db'



class DemonDataDB:
    def __init__(self):
        self.connection = sqlite3.connect(dbname, check_same_thread=False)
        self.cursor = self.connection.cursor()

    def get_data_retrieval_by_failure_rate(self):
        # Example: assumes a table 'data_retrieval' with columns 'failure_rate' and 'retrieved_data'
        # Modify the query as per your schema
        try:
            self.cursor.execute(
                "SELECT failure_rate, AVG(retrieved_data) FROM data_retrieval GROUP BY failure_rate"
            )
            return self.cursor.fetchall()
        except Exception as e:
            print("Error DB Query: {}".format(e))
            return []


def plot_data_retrieval_vs_failure_rate():
    demon_db = DemonDataDB()
    data = demon_db.get_data_retrieval_by_failure_rate()
    if not data:
        print("No data to plot.")
        return
    failure_rates = [row[0] for row in data]
    retrievals = [row[1] for row in data]
    plt.plot(failure_rates, retrievals, marker='o')
    plt.xlabel('Failure Rate')
    plt.ylabel('Data Retrieval')
    plt.title('Data Retrieval vs Failure Rate')
    plt.grid(True)
    plt.savefig('data_retrieval_vs_failure_rate.png')
    plt.show()


if __name__ == '__main__':
    plot_data_retrieval_vs_failure_rate()


