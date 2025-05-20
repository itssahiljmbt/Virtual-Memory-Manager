import tkinter as tk
from tkinter import ttk, messagebox, filedialog

from fifo import FIFOPageReplacement
from lru import LRUPageReplacement
from optimal import OptimalPageReplacement
from comparison_chart import plot_comparison

def recommend_best_policy(reference_string, num_frames):
    results = {}

    fifo = FIFOPageReplacement(num_frames)
    fifo_faults, fifo_hits = fifo.run(reference_string, simulate_only=True)
    results["FIFO"] = {'faults': fifo_faults, 'hits': fifo_hits}

    lru = LRUPageReplacement(num_frames)
    lru_faults, lru_hits = lru.run(reference_string, simulate_only=True)
    results["LRU"] = {'faults': lru_faults, 'hits': lru_hits}

    optimal = OptimalPageReplacement(num_frames)
    optimal_faults, optimal_hits = optimal.run(reference_string, simulate_only=True)
    results["Optimal"] = {'faults': optimal_faults, 'hits': optimal_hits}

    best = min(results, key=lambda k: results[k]['faults'])
    return best, results

def simulate():
    try:
        frames = int(entry_frames.get())
        ref_str = list(map(int, entry_ref.get().strip().split()))
        algo = combo_algo.get()

        if algo not in ["FIFO", "LRU", "Optimal"]:
            raise ValueError("Select a valid algorithm")

        if algo == "FIFO":
            obj = FIFOPageReplacement(frames)
        elif algo == "LRU":
            obj = LRUPageReplacement(frames)
        elif algo == "Optimal":
            obj = OptimalPageReplacement(frames)

        log, faults, hits = obj.run(ref_str, simulate_only=False)
        best_algo, all_results = recommend_best_policy(ref_str, frames)

        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, f"Algorithm: {algo}\n\n")
        result_text.insert(tk.END, "\n".join(log))
        result_text.insert(tk.END, f"\n\nPage Faults: {faults}, Page Hits: {hits}")
        result_text.insert(tk.END, f"\n\nRecommended: {best_algo} (fewest faults: {all_results[best_algo]['faults']})")

        plot_comparison(all_results)

    except Exception as e:
        messagebox.showerror("Error", str(e))

def load_trace_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if file_path:
        try:
            selected_type = access_type.get()
            reference_string = []
            with open(file_path, 'r') as file:
                for line in file:
                    parts = line.strip().split()
                    if len(parts) == 2:
                        op, page = parts[0], int(parts[1])
                        if selected_type == "All" or op == selected_type:
                            reference_string.append(page)
            if reference_string:
                entry_ref.delete(0, tk.END)
                entry_ref.insert(0, " ".join(map(str, reference_string)))
                messagebox.showinfo("Success", f"Loaded {len(reference_string)} references from file.")
            else:
                messagebox.showwarning("No Data", f"No entries found for access type '{selected_type}' in the file.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load trace file: {str(e)}")

# GUI Layout
app = tk.Tk()
app.title("Page Replacement Simulator")
app.geometry("700x700")

tk.Label(app, text="Number of Frames:").pack()
entry_frames = tk.Entry(app)
entry_frames.pack()

tk.Label(app, text="Reference String (space-separated):").pack()
entry_ref = tk.Entry(app, width=70)
entry_ref.pack()

# Access Type Filter
access_type = tk.StringVar(value="All")
tk.Label(app, text="Filter Access Type:").pack()
ttk.Combobox(app, textvariable=access_type, values=["All", "R", "I"]).pack()

# Load Button
tk.Button(app, text="Load Reference String from Trace File", command=load_trace_file).pack(pady=5)

# Algorithm Selection
tk.Label(app, text="Choose Algorithm:").pack()
combo_algo = ttk.Combobox(app, values=["FIFO", "LRU", "Optimal"])
combo_algo.pack()

tk.Button(app, text="Simulate", command=simulate).pack(pady=10)

result_text = tk.Text(app, height=25, width=80)
result_text.pack()

app.mainloop()