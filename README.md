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


The GoodReads_Analysis.ipynb file uses some data analysis techniques to determine patterns, report observations, and visualize trends in one's reading history. The file will begin by cleaning the CSV file produced by the parser file in order to eliminate duplicate rows and convert data types. Then, visualizations will be produced that explore Pages Read, Authors, Ratings, and Dates Associated with the books in your history. 

### Required Downloads and Libraries
Languages
- Python

Virtual Environment
- Jupyter Lab or Notebook

Libraries/Modules
- BeautifulSoup
- Pandas
- NumPy
- Seaborn
- matplotlib
- datetime
- Itertools

### Directions
1. Fork, Clone, or Download the files
 - GoodReads_Parser.py
 - GoodReads_Analysis.ipnyb
2. Open GoodReads_Parser.py and replace the GOODREADS_URL with the link from your account (You can use the link from the My Books section of the site)
3. Run the parser. This produces a CSV file with your history.
4. Open GoodReads_Analysis.ipynb and run all cells.

### Need to Work on
Several issues need attention in the GoodReads_Parser.py file:
- [line 6] The GoodReads link that needs replacing for every new user is somewhat confusing. There is probably a better way to deal with the source page. 
- [line 167] The variable num_of_pages_in_library is currently set to 30, but it would be better if it could detect the number of pages and generate a CSV that doesn't create duplicates
