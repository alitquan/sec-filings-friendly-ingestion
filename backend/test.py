from sec_downloader import Downloader 
import sec_parser as sp
from pprint import pprint
from bs4 import BeautifulSoup
import contextlib 

'''
+=========+
| UTILITY |
+=========+  
'''

# Utility function to make the example code a bit more compact
def print_first_n_lines(text: str, *, n: int):
    print("\n".join(text.split("\n")[:n]), "...", sep="\n")

# Utility function that pretty-prints a particular Element 
def pprintTag(element): 
    pprint(vars(element._html_tag))

# returns whether or not element is a table 
def hasTableTag(element):
    if element._html_tag._contains_tag[('table', True)] == True: 
        return True
    return False 

# returns whether or not the element is a header or title 
def isHeaderOrTitle(element):
    elementType = type(element)
    if (elementType == sp.semantic_elements.title_element.TitleElement):
        return True 
    elif (elementType == sp.semantic_elements.top_section_title.TopSectionTitle):
        return True 
    else:
          return False 

# original method before trying to parse headers 
# def printTable(element):
#     # actually getting the tables out 
#     table_tag1 = element._html_tag._bs4
#     parsed_table = [] 
#     rows = table_tag1.find_all("tr") 
#     print("#TABLE_START") 
#     for row in rows: 
#         cells = row.find_all(["td", "th"])
#         text_cells = [cell.get_text(strip=True) for cell in cells if cell.get_text(strip=True)]
#         if text_cells:
#             print(text_cells)
#             parsed_table.append(row)
#     print("#TABLE_END") 


def printTable(element):
    def clean_row(row):
        """Merge $ with numeric values and remove unnecessary tokens."""
        cleaned = []
        skip = False
        for i, val in enumerate(row):
            if val == '$':
                skip = True
                continue
            if skip:
                cleaned.append(f"${val}")
                skip = False
            else:
                cleaned.append(val)
        return cleaned

    table_tag = element._html_tag._bs4
    rows = table_tag.find_all("tr")
    
    headers = []
    print("#TABLE_START")

    for idx, row in enumerate(rows):
        cells = row.find_all(["td", "th"])
        raw_text_cells = [cell.get_text(strip=True) for cell in cells if cell.get_text(strip=True)]

        if not raw_text_cells:
            continue

        text_cells = clean_row(raw_text_cells)

        # Set headers from the first valid date row
        if not headers and all(',' in cell for cell in text_cells) and len(text_cells) >= 2:
            headers = ['Line Item'] + text_cells
            print(headers)
            continue

        # Section label (e.g. "ASSETS:", "LIABILITIES")
        if len(text_cells) == 1:
            print([f"**{text_cells[0]}**"] + [''] * (len(headers) - 1))
        else:
            print(text_cells)

    print("#TABLE_END")

'''
+=============+
|    SETUP    |
+=============+ 
'''
# Initialize the downloader with your company name and email
dl = Downloader("Felipo", "alitmallick@gmail.com")

# Download the latest 10-Q filing for Apple
html = dl.get_filing_html(ticker="AAPL", form="10-Q")

print(html) 

# Parse the HTML
elements: list = sp.Edgar10QParser().parse(html)

# render the filing
demo_output: str = sp.render(elements)
print_first_n_lines(demo_output, n=60)
print(elements)

# elements for tables 
table_elements =  {} 

# elements to be rendered 
render_elements = {} 



print("Printing all elements..") 
# get solely the table elements
for i in range(len(elements)): 
    element=elements[i]
    print("lebronx ",i)
    print(element)
    print(type(element))
    try: 
        if (hasTableTag(element)):
            table_elements[i] = element
            render_elements[i] = element 
        elif (isHeaderOrTitle(element)):
            render_elements[i] = element 
            print("is a header or title") 
        print() 
    except KeyError as e: 
        print("skipping element ",i)
        print() 

print("Getting elemental structure") 
print(vars(elements[0]))
pprintTag(elements[0])  
pprintTag(elements[1])  

print("\n\n\nPrinting a tag known to have tables")
# seeing if we can accurately detect whether the elemnt contains a table or an image 
print(elements[0]._html_tag._contains_tag)
print(elements[0]._html_tag._contains_tag[('img', True)])
print(elements[0]._html_tag._contains_tag[('table',True)])
print(hasTableTag(elements[0]))


print("\n\n\nPrinting a tag known to have titles")
print(vars(elements[51]))
pprintTag(elements[51])  
print(elements[51]._html_tag._contains_tag)
print(elements[51]._html_tag._contains_tag[('img', True)])
print(elements[51]._html_tag._contains_tag[('table',True)])
print(hasTableTag(elements[51]))
print(type(elements[51]))

# printing out the tables that were created  
print("Table Elements: ") 
print(table_elements)
print("Render Elements: ") 
print(render_elements) 

print("\n\nFiguring Out Tables") 
pprintTag(elements[9])  

# actually getting the tables out 
table_tag1 = elements[9]._html_tag._bs4
parsed_table = [] 
rows = table_tag1.find_all("tr") 
for row in rows: 
    cells = row.find_all(["td", "th"])
    text_cells = [cell.get_text(strip=True) for cell in cells if cell.get_text(strip=True)]
    if text_cells:
        print(text_cells)
        parsed_table.append(row)
    #print(row) 

print(table_elements)
print("making pretty") 


for key, element in table_elements.items():
    print("Table #",key) 
    printTable(element)
    print() 

for key, element in render_elements.items():
    print("Element #",key) 
    elementType = type(element) 
    if (elementType == sp.semantic_elements.title_element.TitleElement or 
        elementType == sp.semantic_elements.top_section_title.TopSectionTitle
    ):
        print(element.text) 
    elif (elementType == sp.semantic_elements.table_element.table_element.TableElement):
        printTable(element) 
    else:
        print("Not Handled") 
    print() 


# getting titles 
# print("\n\nHeaderElement") 
# pprintTag(elements[197])  
# print(elements[197].text)

# following segment was AI-generated 
# TODO: rewrite methods so that they return strings
with open("output.txt", "w", encoding="utf-8") as f:
    with contextlib.redirect_stdout(f):
        for key, element in table_elements.items():
            print("Table #", key)
            printTable(element)
            print()

        for key, element in render_elements.items():
            print("Element #", key)
            elementType = type(element) 
            if (elementType == sp.semantic_elements.title_element.TitleElement or 
                elementType == sp.semantic_elements.top_section_title.TopSectionTitle):
                print(element.text)
            elif (elementType == sp.semantic_elements.table_element.table_element.TableElement):
                printTable(element)
            else:
                print("Not Handled")
            print()


'''
+=============+
|    ROUTES   |
+=============+ 
'''



