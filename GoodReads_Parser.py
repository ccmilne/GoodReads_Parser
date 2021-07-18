from bs4 import BeautifulSoup
import itertools
import urllib.request
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

    page = requests.get(PAGE_URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    tables = soup.find_all('table')
    #print(len(soup.find_all('table'))) #There are 2 tables; the books are in the second
    book_table = tables[1]

    #Headers: Working!
    headers = []
    column_headers = book_table.find_all('th')
    for column in column_headers:
        headers.append(column['alt'])

    #Rows
    page_list = []
    table_rows = book_table.find_all('tr')
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


        #Column Extraction
        author = row.find(class_='field author').find('div').find('a').text.strip()
        isbn = row.find(class_='field isbn').find('div').text.strip()
        isbn13 = row.find(class_='field isbn13').find('div').text.strip()
        num_pages_string = row.find(class_='field num_pages').find('div').text.strip()
        num_pages = ''.join(i for i in num_pages_string if i.isdigit())
        avg_rating = row.find(class_='field avg_rating').find('div').text.strip()
        num_ratings = row.find(class_='field num_ratings').find('div').text.strip()
        num_ratings_converted = int(num_ratings.replace(',', ''))
        date_pub = row.find(class_='field date_pub').find('div').text.strip()
        date_pub_edition = row.find(class_='field date_pub_edition').find('div').text.strip()
        rating = row.find(class_='field rating').find('div').text.strip()

        #Shelves: Needs to be Checked
        shelves = row.find(class_='field shelves').find('div').find('a').text.strip()

        read_count = row.find(class_='field read_count').find('div').text.strip()
        date_started = row.find(class_='field date_started').find('div').find('span').text.strip()
        date_read = row.find(class_='field date_read').find('div').find('span').text.strip()
        date_added = row.find(class_='field date_added').find('div').find('span').text.strip()

        #adding to list
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
    '''Combine Collections of Lists by Page

    Takes a list of lists and combines those lists into one using
    the itertools library.

    Parameters
    ----------
    library_list: a list of lists

    returns
    -------
    list: flattened list
    '''
    flatten = itertools.chain.from_iterable
    return list(flatten(library_list))

def convert_list_to_csv(one_big_list):
    '''Converts the flattened list a CSV file

    Takes a list of values and writes them to a CSV file

    Parameters
    ----------
    one_big_list: a specific list produced from combine_page_lists()

    returns:
    --------
    CSV file: 'ReadingHistory.csv'
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
    print(f"This program could take several minutes to complete:")
    print(f"")

    #Calling functions
    goodreads_page_data = scrape_goodreads_page(GOODREADS_URL, 1)
    #print(goodreads_page_data)

    #Scrape all pages and add to a list:
    entire_library = []
    num_of_pages_in_library = 30 #Assumes 30 books per page for now, need to figure out how to make the loop dynamic.

    for i in range(num_of_pages_in_library):
        goodreads_page_data = scrape_goodreads_page(GOODREADS_URL, page_number=i)
        entire_library.append(goodreads_page_data)
    #print(len(entire_library))

    combined_lists = combine_page_lists(entire_library)
    convert_list_to_csv(combined_lists)