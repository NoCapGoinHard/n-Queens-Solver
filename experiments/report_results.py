import pandas as pd
import matplotlib.pyplot as plt
import os

FILE_ASTAR = "astar_results.csv"
FILE_CSP = "csp_results.csv"
OUTPUT_DIR = "experiments"

def main():
    path_astar = os.path.join(OUTPUT_DIR, FILE_ASTAR)
    path_csp = os.path.join(OUTPUT_DIR, FILE_CSP)

    if not os.path.exists(path_astar):
        path_astar = FILE_ASTAR
    
    if not os.path.exists(path_csp):
        path_csp = FILE_CSP

    try:
        df_astar = pd.read_csv(path_astar)
        df_csp = pd.read_csv(path_csp)
    except FileNotFoundError as e:
        print(f"Cannot find the csv file paths.\n{e}")
        return

    plt.style.use('bmh') #looked more stylish
    

    #==========================================
    #GLOBAL COMPARISON
    #==========================================
    plt.figure(figsize=(10, 6))

    #plot A* all heuristics
    for heuristic in df_astar['HEURISTIC'].unique():
        subset = df_astar[df_astar['HEURISTIC'] == heuristic]
        plt.plot(subset['N'], subset['TIME_TAKEN'], marker='o', label=f'A* - {heuristic}')
    
    #plot pairwise encoding CSP
    csp_best = df_csp[df_csp['ENCODING'] == 'pairwise_diagonal']
    if not csp_best.empty:
        plt.plot(csp_best['N'], csp_best['TIME_TAKEN'], marker='s', linestyle='--', color='black', label='CSP (Pairwise)')

    plt.title('Execution Time: A* vs CSP (Log Scale)', fontsize=16)
    plt.xlabel('N (Number of Queens)', fontsize=12)
    plt.ylabel('Seconds', fontsize=12)
    plt.yscale('log') 
    plt.legend()
    plt.grid(True, which="both", ls="-", alpha=0.5)
    plt.tight_layout()
    
    output_path = os.path.join(OUTPUT_DIR, 'plot_comparison_log.png')
    plt.savefig(output_path, dpi=300)
    plt.close()

    #==========================================0
    #plot A* nodes expanded all heuristics
    #==========================================0
    plt.figure(figsize=(10, 6))
    
    for heuristic in df_astar['HEURISTIC'].unique():
        subset = df_astar[df_astar['HEURISTIC'] == heuristic]
        plt.plot(subset['N'], subset['NODES_EXPANDED'], marker='o', label=f'A* - {heuristic}')

    plt.title('A* Search Space: nodes expanded (wrt N)', fontsize=16)
    plt.xlabel('Scaling parameter N', fontsize=12)
    plt.ylabel('Nodes Expanded', fontsize=12)
    plt.yscale('log') 
    plt.legend()
    plt.grid(True, which="both", ls="-", alpha=0.5)
    plt.tight_layout()
    
    output_path = os.path.join(OUTPUT_DIR, 'plot_astar_nodes.png')
    plt.savefig(output_path, dpi=300)
    plt.close()

    #==========================================
    #plot csp encodings comparison
    #==========================================
    plt.figure(figsize=(10, 6))
    
    encodings = df_csp['ENCODING'].unique()
    for encoding in encodings:
        subset = df_csp[df_csp['ENCODING'] == encoding]
        plt.plot(subset['N'], subset['TIME_TAKEN'], marker='s', label=f'CSP - {encoding}')
        
    plt.title('CSP performances: Pairwise vs AllDiff encodings', fontsize=16)
    plt.xlabel('Scaling parameter N', fontsize=12)
    plt.ylabel('Seconds', fontsize=12)
    plt.yscale('log') 
    
    #reference line for timeout set at 120 sec (!!!COUPLED, remember to change accordingly!!!)
    plt.axhline(y=120, color='r', linestyle=':', label='Timeout Threshold')
    
    plt.legend()
    plt.grid(True, which="both", ls="-", alpha=0.5)
    plt.tight_layout()
    
    output_path = os.path.join(OUTPUT_DIR, 'plot_csp_encodings_time.png')
    plt.savefig(output_path, dpi=300)
    print(f"Generato: {output_path}")
    plt.close()

    #==========================================
    #plot constraints infos
    #==========================================
    plt.figure(figsize=(10, 6))
    
    for encoding in encodings:
        subset = df_csp[df_csp['ENCODING'] == encoding]
        if 'CONSTRAINTS' in subset.columns:
            plt.plot(subset['N'], subset['CONSTRAINTS'], marker='^', linestyle='-', label=f'CSP - {encoding}')
    
    plt.title('CSP Structure: constraints growth wrt N', fontsize=16)
    plt.xlabel('Scaling parameter N', fontsize=12)
    plt.ylabel('Number of constraints', fontsize=12)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    
    output_path = os.path.join(OUTPUT_DIR, 'plot_csp_constraints.png')
    plt.savefig(output_path, dpi=300)
    plt.close()

    #==========================================
    #plot csp variables infos
    #==========================================
    plt.figure(figsize=(10, 6))
    
    for encoding in encodings:
        subset = df_csp[df_csp['ENCODING'] == encoding]
        if 'VARIABLES' in subset.columns:
            plt.plot(subset['N'], subset['VARIABLES'], marker='x', linestyle='-', label=f'CSP - {encoding}')

    plt.title('CSP Structure: variables growth wrt N', fontsize=16)
    plt.xlabel('Scaling parameter N', fontsize=12)
    plt.ylabel('Number of variables', fontsize=12)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    
    output_path = os.path.join(OUTPUT_DIR, 'plot_csp_variables.png')
    plt.savefig(output_path, dpi=300)
    plt.close()

if __name__ == "__main__":
    main()