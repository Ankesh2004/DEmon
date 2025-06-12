import sqlite3
import matplotlib.pyplot as plt

# Connect to the database
conn = sqlite3.connect('./new_folder/demonDB.db')
cursor = conn.cursor()

# Query convergence data for all runs
cursor.execute("SELECT node_count, convergence_time FROM run")
data = cursor.fetchall()

# Extract node counts and convergence times
node_counts = [row[0] for row in data]
conv_times = [float(row[1]) if row[1] is not None else 0 for row in data]

# Create a scatter plot
plt.scatter(node_counts, conv_times, color='blue')
plt.plot(node_counts, conv_times, 'b-', alpha=0.5)
plt.xlabel('Number of Nodes')
plt.ylabel('Convergence Time (seconds)')
plt.title('Convergence Time vs. Node Count')
plt.grid(True)

# Save and show the plot
plt.savefig('./new_folder/convergence_plot.png')
plt.show()

# Close the connection
conn.close()