## COMS 6111 - Project 2 Group 1 - QProber

### a) Group Name & Team members:
- Chia-Hao Hsu (ch3141)
- Yu Wang (yw2783)

### b) A list of all the files
- BingSearchEngine.py
- Category.py
- ContentSummarizer.py
- QProber.py
- Util.py
- main.py
- Root.txt
- Sports.txt
- Health.txt
- Computers.txt

### c) how to run this program
```python
python main.py <bing_key> <BING_ACCOUNT_KEY> <t_es> <t_ec> <host>
```
  Take this program to search musk with precision = 0.9 For example:
```python
python main.py qvgP+C20TXdZWmcBz34xkB2Ud0hG34a8IFmr4OpsaPQ 0.6 100 yahoo.com
```
### d) Internal Design
- **main.py**<br>
    In this project, the main.py functionality is pretty simple. Basically, run function in main.py will QProber.py to classify, and then use the result QProber collects to build the content summary by using Content Summarizer (ContentSummarizer.py). Other functionalities include argument parser (arg_parser), helper function (helper).

- **QProber.py**<br>
    It is very obvious. This function is the implementation of QProbe classification algorithm, which is mentioned in the paper p.15 & p.9. The classificatio algorithm is as follow:<br><br>
      ***Classify Algorithm:***<br>
      ![classify](http://i.imgur.com/Ghqi6UL.png)
      <br><br>
      ***ECoverage & ESpecificity:***<br>
      ![Imgur](http://i.imgur.com/kIgnn30.png)
      
      Basically, we use Bing API to get the match number for every query of one category to get the estimate coverage (ECoverage). Then, we can use the formula in the paper to calculate estimate specificity (ESpecificity). If the ecoverage & especificity is larger or equal to the target coverage and target specificity, we can declare that this web database is belong to this category. We recursively classify until we meet the leaves of categories.
    
- **BingSearchEngine.py**<br>
    Format the query to url format, call Bing Search API, and return the JSON format result.

- **ContentSummarizer.py**<br>
    Implement several computation functions for vectors, like dot product, sum up two vectors, minus two vectors.

- **Category.py**<br>
    Define several constants, which we don't want user or even developer easily to change.

- **Utils.py**<br>
    Includes stop word list and special character list, which I will use to remove stop words & special characters from the input document.     Also, we include some utility function, like replace_non_ascii_with_space, replace_special_chars, in this file, and the error class we     define by ourselves.
    
- **Root.txt, Health.txt, Computers.txt, Sports.txt**<br>
    Includes stop word list and special character list, which I will use to remove stop words & special characters from the input document.     Also, we include some utility function, like replace_non_ascii_with_space, replace_special_chars, in this file, and the error class we     define by ourselves.

### e) Your Bing Search Account Key
    key: 66VZ/0vWWypKpW7Okf53vtYWsni12Mo9a1dua43bKnU
### f) Any additional information that you consider significant 
We also try title enhancement for our case, but the result doesn't improve too much in the end, sometimes it makes the result even worse since there are some words that will make the result become weird. Take "taj mahel" as example. If we do the title enhancement, then the augmented words the algorithm will pick will be "video" & "streaming" since these two words are in the title of the relevant results.

### Reference:
QProber: A System for Automatic Classification of Hidden-Web Databases http://www.cs.columbia.edu/~gravano/Papers/2003/tois03.pdf
