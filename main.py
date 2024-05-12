import matplotlib.pyplot as plt
import numpy as np

with open("./local_machine_res/data.txt", "r") as f:
    analysis_data_input = f.read()
with open("./docker_res/data.txt", "r") as f:
    analysis_data_docker_input = f.read()
 
analysis_data = analysis_data_input.split(" ")
analysis_data_docker = analysis_data_docker_input.split(" ")


analysis_data_docker = [float(i) for i in analysis_data_docker]
analysis_data_docker = [int(i) for i in analysis_data_docker]
analysis_data_docker = analysis_data_docker[2:-1]


analysis_data = [float(i) for i in analysis_data]
analysis_data = [int(i) for i in analysis_data]
analysis_data = analysis_data[2:-1]


x = range(1, len(analysis_data) + 1)
x2 = range(1, len(analysis_data_docker) + 1)

# Create the plot
plt.figure(figsize=(10, 6))
plt.plot(x, analysis_data, marker='o', linestyle='-', color='r')
plt.plot(x2, analysis_data_docker, marker='o', linestyle='-', color='b')
plt.title('Analysis Data Plot')
plt.xlabel('Times')
plt.ylabel('Execution Time')
plt.grid(True)
plt.ylim(0, 70)  # Ensure y-axis starts at 0 and has some space above the max value
plt.xticks(np.arange(min(x), max(x)+1, 1.0))


for i, value in enumerate(analysis_data):
    plt.annotate(value, (x[i], analysis_data[i]), textcoords="offset points", xytext=(0,10), ha='center')


for i, value in enumerate(analysis_data_docker):
    plt.annotate(value, (x2[i], analysis_data_docker[i]), textcoords="offset points", xytext=(0,10), ha='center')


# Show the plot
plt.show()

