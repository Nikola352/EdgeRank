# Edge Rank

Python implementation of the EdgeRank algorithm for ranking statuses in the news feed of social networks.

## Overview

On application start, you can login just by entering a name present in the dataset (try "Sarina Hudgens" or "Angel Harmison"). 
<br/>

Then, 10 most relevant statuses will be displayed. These are the statuses with the highest EdgeRank score, which is calculated as follows:

    EdgeRank = user_affinity * status_weight * time_decay_factor

where:
    
    user_affinity is the affinity of the user to the author of the status
    status_weight is determined by the statuses popularity (number of likes, comments and shares)
    time_decay_factor is a factor that decreases the score of older statuses
<br/>

Then, the status search is shown. The search looks for statuses that contain the given keywords in the message, with statuses with higher EdgeRank score being displayed first.

## Running 

To run the program, simply start main.py with python3
    
```bash
python3 main.py
```

## Loading data

If there are no serialized data structures, the program will try to load them from the dataset. You can start this operation manually by running the load_data.py script.

```bash
python3 load_data.py
```

A new dataset can be appended to existing data by running the append_data.py script.

```bash
python3 append_data.py
```

The test files can be updated to use newer dates by running the following script.

```bash
python3 data_utils/parse_files.py
```