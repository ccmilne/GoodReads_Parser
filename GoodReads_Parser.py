from bs4 import BeautifulSoup
import itertools
import urllib.request
from bs4.element import Tag
import requests, json, csv

GOODREADS_URL = 'https://www.goodreads.com/review/list/62504919-cameron-milne?' #Replace with your link

### GoodReads Data
def scrape_goodreads_page(url, page_number):
    '''Scrapes GoodReads reading history into a dictionary

    This function takes in a particular page of one's GoodReads reading history
    and scrapes relevant statistics for every book on that page. 

    Parameters
    ----------
    URL of page

    Returns:
    -------
    List of lists; all lists within the list are an individual book and its data
    '''

    page_number_string = 'page=' + str(page_number)
    PAGE_URL = url + page_number_string
    #print(PAGE_URL)

    # GOODREADS_URL = 'https://www.goodreads.com/review/list/62504919-cameron-milne?view=table'

    page = requests.get(PAGE_URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    #print(soup.title.string)

    #Trying regex
    tables = soup.find_all('table')
    #print(len(soup.find_all('table'))) #There are 2 tables; the books are in the second
    book_table = tables[1]

    #Headers: Working!
    headers = []
    column_headers = book_table.find_all('th')
    for column in column_headers:
        headers.append(column['alt'])
    #print(headers)

    #Rows
    page_list = []
    table_rows = book_table.find_all('tr')
    #print(table_rows)
    for row in table_rows[1:]:

        #Title: Needs edits
        childTag = row.find(class_='field title').find('div').find('a').find('span')
        if childTag:
            title_mess = row.find(class_='field title').find('div').text.strip()
            indented_list = title_mess.splitlines()
            new_list = []
            for line in indented_list:
                new_line = line.strip()
                new_list.append(new_line)
            title = ' '.join(new_list)
        else:
            title = row.find(class_='field title').find('div').find('a').text.strip()


        #Author: Working!
        author = row.find(class_='field author').find('div').find('a').text.strip()
        #print(author)

        #field isbn: Working!
        isbn = row.find(class_='field isbn').find('div').text.strip()
        #print(isbn)

        #field isbn13: Working!
        isbn13 = row.find(class_='field isbn13').find('div').text.strip()
        #print(isbn13)

        #Number of Pages: Working!
        num_pages_string = row.find(class_='field num_pages').find('div').text.strip()
        num_pages = ''.join(i for i in num_pages_string if i.isdigit())
        #print(num_pages_stripped)

        #Average Rating: Working!
        avg_rating = row.find(class_='field avg_rating').find('div').text.strip()
        #print(avg_rating)

        #Number of Ratings: Working!
        num_ratings = row.find(class_='field num_ratings').find('div').text.strip()
        num_ratings_converted = int(num_ratings.replace(',', ''))
        #print(num_ratings)

        #Publish Date: Working!
        date_pub = row.find(class_='field date_pub').find('div').text.strip()
        #print(date_pub)

        #Publish Date Edition: Working!
        date_pub_edition = row.find(class_='field date_pub_edition').find('div').text.strip()
        #print(date_pub_edition)

        #My Rating: Working!
        rating = row.find(class_='field rating').find('div').text.strip()
        #print(rating)

        #Shelves: Needs to be Checked
        shelves = row.find(class_='field shelves').find('div').find('a').text.strip()
        #print(shelves)

        #Read Count: Working!
        read_count = row.find(class_='field read_count').find('div').text.strip()
        #print(read_count)

        #Date Started: Working!
        date_started = row.find(class_='field date_started').find('div').find('span').text.strip()
        #print(date_started)

        #Date Read: Working!
        date_read = row.find(class_='field date_read').find('div').find('span').text.strip()
        #print(date_read)

        #Date Added: Working!
        date_added = row.find(class_='field date_added').find('div').find('span').text.strip()
        #print(date_added)

        row_list = []
        row_list.append(title)
        row_list.append(author)
        row_list.append(isbn)
        row_list.append(isbn13)
        row_list.append(num_pages)
        row_list.append(avg_rating)
        row_list.append(num_ratings_converted)
        row_list.append(date_pub)
        row_list.append(date_pub_edition)
        row_list.append(rating)
        row_list.append(shelves)
        row_list.append(read_count)
        row_list.append(date_started)
        row_list.append(date_read)
        row_list.append(date_added)

        #Appending row data to the list of rows for a single page
        page_list.append(row_list)

    return page_list

def combine_page_lists(library_list):
    '''Parses Wikipedia dictionary and cleans data

    Iterates through the dictionary produced by the build_wikipedia_dictionary()
    and removes capitalization, dollar signs, and commas.

    Parameters
    ----------
    wiki_dict: a dictionary produced by build_wikipedia_dictionary()

    returns
    -------
    new_dict: cleaned dictionary
    '''
    flatten = itertools.chain.from_iterable

    return list(flatten(library_list))

def convert_list_to_csv(one_big_list):
    '''Converts the Wikipedia Dictionary into a CSV file

    The CSV file used in build_wikipedia_dictionary() converted the raw
    data into a dictionary in order for data cleaning. Now, it's being converted
    back to a CSV file in order for the data to be uploaded to the database.
    The function iterates through the dictionary keys and appends each key, list of values
    to a row in the csv file.

    Parameters
    ----------
    wiki_dict: a specific wikipedia dictionary produced from clean_wikipedia_dictionary()

    returns:
    --------
    CSV file: 'wikipedia.csv'
    '''
    fields = [
        'Title',
        'Author',
        'ISBN',
        'IBSN13',
        'Number of Pages',
        'Average Rating',
        'Number of Ratings',
        'Publish Date',
        'Publish Date Edition',
        'My Rating',
        'Shelves',
        'Read Count',
        'Date Started',
        'Date Read',
        'Date Added',
    ]

    filename = 'ReadingHistory.csv'
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile) # creating a csv writer object
        csvwriter.writerow(fields) # writing the fields
        csvwriter.writerows(one_big_list)  # writing the data rows

if __name__ == "__main__":

    print(f"")
    print(f"This program will take several minutes to complete:")
    print(f"")

    #Calling functions
    goodreads_page_data = scrape_goodreads_page(GOODREADS_URL, 1)
    #print(goodreads_page_data)

    #Scrape all pages and add to a list:
    entire_library = []
    num_of_pages_in_library = 24 #Assumes 30 books per page for now, need to figure out how to make the loop dynamic.

    for i in range(num_of_pages_in_library):
        goodreads_page_data = scrape_goodreads_page(GOODREADS_URL, page_number=i)
        entire_library.append(goodreads_page_data)
    #print(len(entire_library))

    combined_lists = combine_page_lists(entire_library)
    convert_list_to_csv(combined_lists)