## COMS 6111 - Association Rule Mining
### Project 3 Group 1
Chia-Hao Hsu (ch3141)
Yu Wang (yw2783)

### NYC Open Data Set
New York City Leading Causes of Death
—The leading causes of death by sex and ethnicity in New York City in since 2007.
https://data.cityofnewyork.us/Health/New-York-City-Leading-Causes-of-Death/jb7j-dtam

### Data Processing
We wrote a data processing python code to re-format the data. As there is a ‘ death count’ column in the original dataset which has already aggregate the data to some extent. We re-organize the data into individual tuples and removed the aggregation column so that the algorithm can calculate the frequency as expected.
Split the ‘death’ count column into separate rows according to the count number. i.e. If death = 3, then current row will be duplicate 2 more times in the dataset. Delete the original ‘death’ column in dataset.
*The output dataset INTEGRATED-DATASET.csv has been enclosed. 

### Association Rules
We ran the algorithm with support value = 0.1 and confidence = 0.5 and here is a summery of associations we found.
•	Frequent items<br>
For frequent items, we found high support items such as [DISEASES OF HEART] - 35.0%, [MALIGNANT NEOPLASMS] - 25%, which means heart and malignant neoplasms are two major causes of death of New York City.<br><br>

•	High confidence (> 50%) association rules<br>
We found some interesting results from the association rules illustrated as below.
- **[DISEASES OF HEART(I00-I09, I11, I13, I20-I51)] => [White Non-Hispanic] (Conf: 55.0%, Supp: 19.0%)**<br>
Diseases of heart ‘implies’ white non Hispanic ethnicity. White people in NYC seems to be more vulnerable to heart diseases than other ethnic groups.<br>
- **[Diseases of Heart (I00-I09, I11, I13, I20-I51)] => [F] (Conf: 53.0%, Supp: 19.0%)**<br>
Among people died from heart diseases, women seem to be more vulnerable than men.<br>
- **[Diseases of Heart (I00-I09, I11, I13, I20-I51), White Non-Hispanic] => [F] (Conf: 54.0%, Supp: 10.0%)**<br>
Specifically, for white non - Hispanic group of people who suffer heart diseases, females are major victims. This association is a combination of previous two.<br>
- **[Malignant Neoplasms (Cancer: C00-C97)] => [F] (Conf: 51.0%, Supp: 13.0%)**<br>
For people died from malignant neoplasms, females are also more vulnerable than men. 

### List of Files
AssocRulesExtractor.py
Candidate.py
Error.py
Util.py
main.py

### Internal Design
- ***main.py:***<br>
In main.py, we implement the argument parser, help message, and the main logic for this project, which in in the run function.

- ***AssocRulesExtractor.py:***<br>
Follow the content in the paper, "Fast Algorithms for Mining Association Rules", to implement the Apriori algorithm. Use the concept in figure 1 on page 3 to implement all the process.

- ***Candidate.py:***<br>
Implement the ItemSet & Candidate data structure. ItemSet is a sorted touple, and candidate is actually a ordered dictionary. We extend the original data strcucture in python to make it more powerful and increase the readability of our code.

- ***Util.py:***<br>
Implement several useful functions isolated from the main logic of the algorithm in the program. For example, I implement gen_output in this file to generate the final output.txt.

- ***Error.py:***<br>
	Devise several error exception for this program.

### How to run the program
```python
python main.py <DATASET_FILENAME> <min_supp> <min_conf>
```
ex.
```python
python main.py Cause_of_Death.csv 0.1 0.5
```
