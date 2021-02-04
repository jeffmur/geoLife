## Branch: Data
Only the generated data is stored here.

### 1.1 Mission 
Data pre-processing to detect anomoulous users <br>
Paper: https://doi.org/10.1145/3380970

### 1.2 Approach
1. Heatmaps for each user
2. Creates keras layers of image representation of heatmaps
3. Incorporate Training Data and Verfification set
4. Train LSTM Model

### 1.3 Results
Todo, include relavent graph and information.

Goal: public dataset when we have some results and data visualization

# Files to generate
dispatch.py {gen_user_all.py} or {gen_user_month.py}

Modify both files: 
- cell_size, currently 300 meters.
- directory, to where the data is stored on your local drive(s). 
    
TODO:
- Better Node Balances with CPU Cores (use file sizes rather than num of files)
- CPU overload (groups > num of cores available)

Note: your kernel will round robin and prevent overflow, however this was tested with Ryzen 7 2700x 16 Core processor. As well as, your CPU will hit 100% usage for 5 to 10 minutes to parse through large amount of files... 
