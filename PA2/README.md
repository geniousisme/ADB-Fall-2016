## COMS 6111 - Project 2 Group 1 - QProber

### a) Group Name & Team members:
- Chia-Hao Hsu (ch3141)
- Yu Wang (yw2783)

### b) A list of all the files
- BingSearchEngine.py
- Category.py
- ContentSummarizer.py
- Util.py
- main.py
- Root.txt
- Sports.txt
- Health.txt
- Computers.txt

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
    In this file, there are several functions under MainFunc class. We basically provide the functionality to parse the arguments in the       command line, print out information for search, write the information into transcript.txt and call QueryExpansion.py to generate the       updated augmented words for query. We initialize the query as user input and also set up the target precision followed with user         input. Then, based on user's feedback, we can know what current precision is. If current precision is still below target precision, we     will call Query Expansion function to generate augmented words for new query. Once the precision reaches the target precision, the         program will stop. Otherwise, it will repeat itself, just like above process.

- **QueryExpansion.py**<br>
    This file includes several function implementations that contain the algorithm we will explain later in part(e)

- **BingSearchEngine.py**<br>
    Format the query to url format, call Bing Search API, and return the JSON format result.

- **VectorCompute.py**<br>
    Implement several computation functions for vectors, like dot product, sum up two vectors, minus two vectors.

- **DocumentEnum.py**<br>
    Define several constants, which we don't want user or even developer easily to change.

- **Utils.py**<br>
    Includes stop word list and special character list, which I will use to remove stop words & special characters from the input document.     Also, we include some utility function, like replace_non_ascii_with_space, replace_special_chars, in this file, and the error class we     define by ourselves.

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
    Now we get tf & idf vectors, we use the following formula to get tf-idf value for all the words:
    ![Imgur](http://i.imgur.com/5R0qgOW.png)
    
    Now we have the 2D vectors for all words tf-idf value in each documents.

6. Compute weight vector by Rocchio's Algo:<br>
    Now, we pick up the categorize relevant tf-idf vectors & non-relevant tf-idf vectors from the result we get from above steps. And         follow Rocchio's algorithm to get our updated weight vectors for each word:
    ![Imgur](http://i.imgur.com/cjBfweI.png)
    
    We set a = 1, b = 0.75, c = 0.15 according to the reference we have.

7. Sort the weight vector by reversed order:<br>
   Now we already have updated weight vector for each word. We sort them with the weight by decreasing order, since we only want the first    two words with biggest weight.

8. Pick up the first two words and append them with current query<br>

### f) Your Bing Search Account Key
    key: 66VZ/0vWWypKpW7Okf53vtYWsni12Mo9a1dua43bKnU
### g) Any additional information that you consider significant 
We also try title enhancement for our case, but the result doesn't improve too much in the end, sometimes it makes the result even worse since there are some words that will make the result become weird. Take "taj mahel" as example. If we do the title enhancement, then the augmented words the algorithm will pick will be "video" & "streaming" since these two words are in the title of the relevant results.

### Reference:
Stop Word List: http://xpo6.com/list-of-english-stop-words/ <br>
Modern Information Retrieval: A Brief Overview http://www.cs.columbia.edu/~gravano/cs6111/Readings/singhal.pdf <br>
Introduction to Information Retrieval, Ch 9: http://nlp.stanford.edu/IR-book/
