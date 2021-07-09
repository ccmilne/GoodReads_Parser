# GoodReads Reading History Parser

This repository gives users the ability to explore their GoodReads reading history. Read below for explanations and required downloads. 

The GoodReads_Parser.py file uses BeautifulSoup to scrape relevant data from an individual's "My Books" section. Here, some data cleaning such as data type conversions and name accomodations are used to ensure all text is preserved as it's represented on the website. Fields include:
- Title
- Author
- ISBN
- IBSN13
- Number of Pages
- Average Rating
- Number of Ratings
- Publish Date
- Publish Date Edition
- My Rating
- Shelves
- Read Count
- Date Started
- Date Read
- Date Added

The EDA.ipynb file uses some data analysis techniques to determine patterns, report observations, and visualize trends in one's reading history. 


scrapes and analyzes one's GoodReads reading history. 

Required Downloads and Libraries
Languages
- Python

Libraries/Modules
- BeautifulSoup
- Pandas
- NumPy
- Seaborn
- matplotlib
- datetime