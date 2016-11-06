## COMS 6111 - Project 2 Group 1 - QProber + Content Summary

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
  For example:
```python
python main.py "66VZ/0vWWypKpW7Okf53vtYWsni12Mo9a1dua43bKnU" 0.6 100 yahoo.com
```
### d) Internal Design
- **main.py**<br>
    In this project, the main.py functionality is pretty simple. Basically, run function in main.py will QProber.py to classify, and then use the result QProber collects to build the content summary by using Content Summarizer (ContentSummarizer.py). Other functionalities include argument parser (arg_parser), helper function (helper).

- **QProber.py**<br>
    This function is the implementation of QProbe classification algorithm, which is mentioned in the paper p.15 & p.9. The classificatio algorithm is as follow:<br><br>
      ***Classify Algorithm:***<br>
      ![classify](http://i.imgur.com/Ghqi6UL.png)
      <br><br>
      ***ECoverage & ESpecificity:***<br>
      ![Imgur](http://i.imgur.com/kIgnn30.png)
      
      Basically, we use Bing API to get the match number for every query of one category to get the estimate coverage (ECoverage). Then, we can use the formula in the paper to calculate estimate specificity (ESpecificity). If the ecoverage & especificity is larger or equal to the target coverage and target specificity, we can declare that this web database is belong to this category. We recursively classify until we meet the leaves of categories.
    
- **BingSearchEngine.py**<br>
    Return the match number for every query under the category, and collect top 4 urls for each query of the category for content summary.

- **ContentSummarizer.py**<br>
    There are four parts in the content summarizer. <br>
    1) summarize: calls summarize_for_categ for each subcategory <br>
    2) summarize_for_categ: calculate the word document frequency for each category <br>
    3) fetch_page: Return set of words from the url page and fetch page through lynx <br>
    4) page_parser: parse each html page with the approach mentioned in proj2 description, which includes three requirements:<br>
          - Any part of the text after the "References" line should be ignored.<br>
          - Also any text within brackets "[....]" should be ignored.<br>
          - Any character not in the English alphabet should be treated as a word separator, and the words are case-insensitive.<br>

    We avoid the visiting the same url by eliminating those urls from root urls set. However, we collect the word document frequency in another dictionary and assign the dictionary to Root when we need the calculate word document frequency for Root. Last but not the least, since we think that generating so many txt files under same directory is very bothering, our code will put all the summary txt file under ContentSummary directory. Our code will generate the directory if the directory doesn't exist yet.

- **Category.py**<br>
    Category class for category objects. We also implemented basic object operation methods such as showing classification infomation, or checking category is root or not. 

- **Utils.py**<br>
    Utility function to extract queries regarding to each category into a dictionary.
    
- **Root.txt, Health.txt, Computers.txt, Sports.txt**<br>
    Text files which stores category and its corresponding queries. 

### e) Your Bing Search Account Key
    key: 66VZ/0vWWypKpW7Okf53vtYWsni12Mo9a1dua43bKnU

### f) Additional Information
We didn't implement the multi-word entries part. The performance of classificaiton is the same as reference. However, content summary are slightly differet due to different factors. In our implementation, if the url header shows that it is not text/html file, we just skip the url. Nevertheless, the word frequency is still quite simialr with reference implementation.

### Reference:
QProber: A System for Automatic Classification of Hidden-Web Databases http://www.cs.columbia.edu/~gravano/Papers/2003/tois03.pdf
