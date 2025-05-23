import numpy as np
import matplotlib.pyplot as plt

def showMetrics(time_path, gbest_path):
    # Read execution times.
    with open(time_path, 'r') as f:
        times = [float(line.strip()) for line in f if line.strip()]
    
    # Read fitness values ​​from the global best file.
    with open(gbest_path, 'r') as f:
        fitness = []
        for line in f:
            if line.strip():
                fit_str = line.strip().split('-')[0]
                try:
                    fitness.append(float(fit_str))
                except ValueError:
                    print(f"Error converting to float: {fit_str}")
    
    if not fitness or not times:
        print("The files could not be read correctly or are empty..")
        return

    fitness_np = np.array(fitness)
    times_np   = np.array(times)

    # Calculate statistical metrics.
    best_fit   = np.max(fitness_np)
    worst_fit  = np.min(fitness_np)
    avg_fit    = np.mean(fitness_np)
    median_fit = np.median(fitness_np)
    std_fit    = np.std(fitness_np)
    iqr_fit    = np.percentile(fitness_np, 75) - np.percentile(fitness_np, 25)
    avg_time   = np.mean(times_np)

    print("===== FITNESS METRICS =====")
    print(f"Best: {best_fit}")
    print(f"Worst: {worst_fit}")
    print(f"Avg: {avg_fit}")
    print(f"Median: {median_fit}")
    print(f"Std: {std_fit}")
    print(f"IQR: {iqr_fit}")
    print("\n===== TIME METRICS =====")
    print(f"Avg time: {avg_time:.6f} s")

    # Display boxplot to visualize the IQR.
    plt.figure(figsize=(6, 4))
    plt.boxplot(fitness_np, vert=False)
    plt.title("Fitness Boxplot (IQR)")
    plt.xlabel("Fitness")
    plt.grid(True)
    plt.tight_layout()
    plt.show()
