import matplotlib.pyplot as plt

def plot_comparison(results):
    algorithms = list(results.keys())
    faults = [results[algo]['faults'] for algo in algorithms]
    hits = [results[algo]['hits'] for algo in algorithms]

    plt.figure(figsize=(10, 5))

    # Plotting as zigzag/line
    plt.plot(algorithms, faults, label='Page Faults', marker='o', linestyle='-', color='red')
    plt.plot(algorithms, hits, label='Page Hits', marker='o', linestyle='-', color='green')
    plt.xlabel("Algorithm")
    plt.ylabel("Count")
    plt.title("Page Replacement Algorithms Comparison")
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.legend()
    plt.tight_layout()
    plt.show()