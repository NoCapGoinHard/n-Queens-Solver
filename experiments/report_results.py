import pandas as pd
import matplotlib.pyplot as plt
import pathlib

FILE_ASTAR = "astar_results.csv"
FILE_CSP = "csp_results.csv"
OUTPUT_DIR = "." #"this one" is "."

def main():
    
    df_astar = pd.read_csv(FILE_ASTAR)
    df_csp = pd.read_csv(FILE_CSP)

    plt.style.use('bmh') # looked more stylish
    plt.figure(figsize=(10, 6))

    for heuristic in df_astar['HEURISTIC'].unique():
        subset = df_astar[df_astar['HEURISTIC'] == heuristic]
        plt.plot(subset['N'], subset['TIME_TAKEN'], marker='o', label=f'A* - {heuristic}')
    plt.plot(df_csp['N'], df_csp['TIME_TAKEN'], marker='s', linestyle='--', label='CSP', color='black')
    
    plt.title('Execution Time: A* vs CSP WITH LOGARITMIC SCALE', fontsize=16)
    plt.xlabel('Scaling parameter -> N (n° of queens and chessboard cells per side)', fontsize=14)
    plt.ylabel('Time (sec)', fontsize=12)
    plt.yscale('log') 
    plt.legend()
    plt.grid(True, which="both", ls="-", alpha=0.5)
    plt.tight_layout()

    output_path = OUTPUT_DIR + '/plot_time_comparison_log.png'
    plt.savefig(output_path, dpi=300)
    plt.close()