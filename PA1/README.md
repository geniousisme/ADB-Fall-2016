
## COMS 6111 - Project 1 Group 1 - Query Expansion

### a) Group Name & Team members:
- Chia-Hao Hsu (ch3141)
- Yu Wang (yw2783)

### b) A list of all the files
- README.md
- transcript.txt (include the score for 'musk', 'brin', and 'taj mahal')
- main.py
- QueryExpansion.py
- BingSearchEngine.py
- VectorCompute.py
- DocumentEnum.py
- Utils.py

### c) how to run this program
```python
python main.py <bing_key> <target precision> <query>
```
  Take this program to search musk with precision = 0.9 For example:
```python
python main.py qvgP+C20TXdZWmcBz34xkB2Ud0hG34a8IFmr4OpsaPQ 0.9 musk
```
### d) Internal Design
- **main.py**<br>
    In this file, there are several functions under MainFunc class. We basically provide the functionality to parse the arguments in the       command line, print out information for search, write the information into transcript.txt and call QueryExpansion.py to generate the       updated augumented words for query. We initialize the query as user input and also set up the target precision followed with user         input. Then, based on user's feedback, we can know what current precision is. If current precision is still below target precision, we     will call Query Expansion function to generate augmented words for new query. Once the precision reaches the target precision, the         program will stop. Otherwise, it will repeat itself, just like above process.

- **QueryExpansion.py**<br>
    This file includes several function implementations that contain the algorithm we will explain later in part(e)

- **BingSearchEngine.py**<br>
    Format the query to url format, call Bing Search API, and return the JSON format result.

- **VectorCompute.py**<br>
    Implement several computation function for vectors, like dot product, sum up two vectors, minus two vectors.

- **DocumentEnum.py**<br>
    Define several constants which we don't want user or even developer easily to change.

- **Utils.py**<br>
    Includes stop word list and special charater list, which I will use to remove stop words & special charaters from the input document.     Also, we include some utility function, like replace_non_ascii_with_space, replace_special_chars, in this file, and the error class we     define by ourselves.

### e) Description Of Query-Modification Method

The query modification algorithm is composed of the following parts:

1. Build Up The Word Vector:
    We collect all the relevant & non-relevant JSON results first, build up the input document by adding them together, and run following     steps:<br>
      - Replace special charaters with space <br>
      - Replace non ascii word with space <br>
      - Split the document with space into a list of words <br>
      - Remove stop words from the list of words <br>
    
    After above steps, we can have all the words in all documents. We use this words to build up the word vector.

2. Initialize Query Vector:<br>
    We initial a vector filled with zero and iterate the array, if the word is equal to the word in query, we change the value of element     in the vector to one.

3. Compute idf vector:<br>
    Now we can process the idf value for each word. For the idf value, we use following formula to compute:

    ![Imgur](http://i.imgur.com/8iHR0jD.png)

4. Compute tf vector:<br>
    After we process idf vector, now we iterate each document to count the term frequecy value for each word in each document. We use         following formula to calculate:<br>
    
    ![Imgur](http://i.imgur.com/qW9T5mj.png)
    
    nij is the frequency the word i appears in this document j. The denominator is the summation of all words' frequency in this document.

5. Compute tf-idf vector:<br>

    

### f) Your Bing Search Account Key
    key: qvgP+C20TXdZWmcBz34xkB2Ud0hG34a8IFmr4OpsaPQ
### g) Any additional information that you consider significant 

### Reference:
Stop Word List: http://xpo6.com/list-of-english-stop-words/ <br>
Modern Information Retrieval: A Brief Overview http://www.cs.columbia.edu/~gravano/cs6111/Readings/singhal.pdf <br>
Introduction to Information Retrieval, Ch 9: http://nlp.stanford.edu/IR-book/
