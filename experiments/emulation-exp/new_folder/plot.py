import sqlite3
import matplotlib.pyplot as plt

# Connect to demonDB.db
conn = sqlite3.connect('./demonDB.db')
cursor = conn.cursor()

# Query run data
cursor.execute("SELECT node_count, convergence_time, convergence_message_count FROM run")
data = cursor.fetchall()

# Extract data
node_counts = [row[0] for row in data]
conv_times = [float(row[1]) if row[1] is not None else 0 for row in data]
message_counts = [int(row[2]) if row[2] is not None else 0 for row in data]

# Plot 1: Convergence Time vs. Node Count
plt.figure(figsize=(10, 5))
plt.subplot(1, 2, 1)
plt.scatter(node_counts, conv_times, color='blue')
plt.plot(node_counts, conv_times, 'b-', alpha=0.5)
plt.xlabel('Number of Nodes')
plt.ylabel('Convergence Time (seconds)')
plt.title('Convergence Time vs. Node Count')
plt.grid(True)

# Plot 2: Message Count vs. Node Count
plt.subplot(1, 2, 2)
plt.scatter(node_counts, message_counts, color='green')
plt.plot(node_counts, message_counts, 'g-', alpha=0.5)
plt.xlabel('Number of Nodes')
plt.ylabel('Convergence Message Count')
plt.title('Message Count vs. Node Count')
plt.grid(True)

# Save and show
plt.tight_layout()
plt.savefig('./convergence_plots.png')
plt.show()

# Close connection
conn.close()