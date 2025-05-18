from sec_downloader import Downloader 
import sec_parser as sp
from pprint import pprint

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


def hasTableTag(element):
    if element._html_tag._contains_tag[('table', True)] == True: 
        return True
    return False 

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


# table elements 
table_elements =  {} 

print("Printing all elements..") 
# get solely the table elements
for i in range(len(elements)): 
    element=elements[i]
    print("lebronx ",i)
    print(element)
    try: 
        if (hasTableTag(element)):
            table_elements[i] = element
    except KeyError as e: 
        print("skipping element ",i)

print("Getting elemental structure") 
print(vars(elements[0]))
pprintTag(elements[0])  
pprintTag(elements[1])  

# seeing if we can accurately detect whether the elemnt contains a table or an image 
print(elements[0]._html_tag._contains_tag)
print(elements[0]._html_tag._contains_tag[('img', True)])
print(elements[0]._html_tag._contains_tag[('table',True)])
print(hasTableTag(elements[0]))

# print table list 
print(table_elements)


