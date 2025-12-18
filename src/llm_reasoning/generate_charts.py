import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import sys

# Setup
plt.style.use('bmh') # Clean aesthetic
logging_handler = sys.stdout

def generate_charts(input_file, assets_dir):
    try:
        df = pd.read_csv(input_file)
    except FileNotFoundError:
        print(f"File not found: {input_file}")
        return

    # Ensure assets dir exists
    os.makedirs(assets_dir, exist_ok=True)
    
    # 1. Top 10 Scores Bar Chart
    top_10 = df.head(10).copy()
    top_10 = top_10.sort_values(by='final_score', ascending=True) # Sort for barh

    plt.figure(figsize=(10, 6))
    bars = plt.barh(top_10['ticker'], top_10['final_score'], color='#2c3e50')
    
    plt.title('Top 10 Companies by Fundamental Score', fontsize=14, pad=20)
    plt.xlabel('Composite Score')
    plt.grid(axis='x', linestyle='--', alpha=0.7)
    
    # Add values to bars
    for bar in bars:
        width = bar.get_width()
        plt.text(width, bar.get_y() + bar.get_height()/2, 
                 f'{width:.2f}', 
                 ha='left', va='center', fontsize=10)

    output_path = os.path.join(assets_dir, 'top10_scores.png')
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()
    print(f"Generated {output_path}")

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    INPUT = os.path.join(base_dir, 'reports', 'top_50.csv')
    OUTPUT_DIR = os.path.join(base_dir, 'reports', 'assets')
    
    generate_charts(INPUT, OUTPUT_DIR)
