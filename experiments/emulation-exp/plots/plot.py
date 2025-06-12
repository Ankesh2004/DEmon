import sqlite3
import matplotlib.pyplot as plt

DB_FILE = './demonDB.db'  # Adjust path if needed


def get_failure_vs_success():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    # Count number of successful queries for each failure_percent
    cur.execute("""
        SELECT failure_percent, COUNT(*) as total, 
               SUM(CASE WHEN success='1' OR success='True' OR success='true' THEN 1 ELSE 0 END) as success_count
        FROM query
        GROUP BY failure_percent
        ORDER BY failure_percent
    """)
    data = cur.fetchall()
    conn.close()
    return data


def plot_failure_vs_success():
    data = get_failure_vs_success()
    if not data:
        print("No data found in query table.")
        return
    failure_rates = [row[0] for row in data]
    total_queries = [row[1] for row in data]
    success_counts = [row[2] for row in data]
    # Calculate success rate as percentage
    success_percent = [100 * s / t if t > 0 else 0 for s, t in zip(success_counts, total_queries)]

    plt.plot(failure_rates, success_percent, marker='o')
    plt.xlabel('Failure Rate (%)')
    plt.ylabel('Success Rate (%)')
    plt.title('Failure Rate vs Success Rate')
    plt.grid(True)
    plt.savefig('failure_vs_success.png')
    plt.show()


if __name__ == '__main__':
    plot_failure_vs_success()


