###Main.py

from algo_runner import  run_initialization, monthly_rebalance

if __name__ == '__main__':
    run_initialization()
    # Call the monthly rebalance after initialization
    
    monthly_rebalance()
