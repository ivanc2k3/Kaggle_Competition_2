# Kaggle_Competition_2
Data Science's In-Class Kaggle Competition 2: Predicting Tabletennis players' Attributes with raw data
**Rank: 2/60**

## Installation

1. Navigate to the directory containing the `Kaggle_Competition_2` folder:  
```bash
cd [DownloadFolder]
```  
2. Install the required packages:  
```bash
pip install -r requirements.txt
```

## Implement

1. Run `timeCut.py`  
I deleted the original `timeCut.py` because I assumed that we don't need to submit the code. Therefore, I generated an alternative version of `timeCut.py` that uses the same idea to split data. This step generates the answer that can be found in the time-splitting process, resulting about 288 data.  

2. Run `peak.py`  
This step generates results matching by splitting peaks.  

3. Run `transPeakToOutput.py`  
Tranform step 2's results to submission format.  

4. Run `mymerge.py`  
Use Step 2's results to fill in the missing parts of Step 1. After merging the two steps, sort them by data_id.

## Results

Leaderboard Score: 0.98335, securing rank 2.