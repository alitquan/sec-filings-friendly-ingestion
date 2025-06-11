from sec_downloader import Downloader 
import sec_parser as sp
from sec_api import PdfGeneratorApi
from pprint import pprint
from bs4 import BeautifulSoup
import contextlib 
from flask import Flask,request,jsonify,send_file,send_from_directory
from flask_cors import CORS 
import os
import io
import contextlib
from config import SEC_API_KEY,GENERATION_DIRECTORY

'''
+=========+
| UTILITY |
+=========+  
'''


# creates the PDF from the @URL provided by the user
# stores it as a file named @pdfName prefixed with timestamp 
# it is stored in a directory called pdf-filings in the CWD 
def store_pdf(url,pdfName):
    # renderApi = RenderApi(api_key=SEC_API_KEY)
    filing = pdfGeneratorApi.get_pdf(url)
    
    output_folder = 'pdf-filings'

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    pdfName2 = pdfName+".pdf" 
    with open(os.path.join(output_folder,pdfName2),"wb") as f: 
        f.write(filing) 



'''
+=============+
|    SETUP    |
+=============+ 
'''

# reference: https://pypi.org/project/sec-api/#pdf-generator-api
pdfGeneratorApi = PdfGeneratorApi(SEC_API_KEY)


'''
+=============+
|    ROUTES   |
+=============+ 
'''

app = Flask(__name__)
CORS(app, origins=["http://localhost:5173"])
@app.route('/')
def home():
    return 'Hello, Flask!'


@app.route('/generatePDF-filing',methods=['POST']) 
def generate_pdf(): 
    data = request.get_json()
    data_url = data ['url']
    data_outputfile=data['outputFile']
    pdf_name = data_outputfile + ".pdf"

    # generate the PDF 
    print("Received from frontend: ", data_url)
    store_pdf(data_url,data_outputfile)
    print("Processing completed: ", data_url)
    return jsonify({"filename":pdf_name})

@app.route('/download-pdf/<path:filename>') 
def view_pdf(filename):
    return send_from_directory( 
        GENERATION_DIRECTORY,filename,as_attachment=False
    )

if __name__ == '__main__':
    print(f"SEC API key is: {SEC_API_KEY}")
    # store_pdf("https://www.sec.gov/Archives/edgar/data/320193/000032019320000096/aapl-20200926.htm","dinkleburg")
    # store_pdf("https://www.sec.gov/Archives/edgar/data/1422183/000162828025023202/fsk-20250331.htm","peter")
    # # examples: 10-K filing, Form 8-K exhibit
    # url_10k_filing = "https://www.sec.gov/Archives/edgar/data/320193/000032019320000096/aapl-20200926.htm"
    # url_8k_exhibit_url = "https://www.sec.gov/ix?doc=/Archives/edgar/data/1320695/000132069520000148/ths12-31x201910krecast.htm"

    # # get PDFs
    # pdf_10k_filing = pdfGeneratorApi.get_pdf(url_10k_filing)
    # pdf_8k_exhibit = pdfGeneratorApi.get_pdf(url_8k_exhibit_url)

    # # save PDFs to disk
    # with open("pdf_10k_filing.pdf", "wb") as f:
    #     f.write(pdf_10k_filing)
    # with open("pdf_8k_exhibit.pdf", "wb") as f:
    #     f.write(pdf_8k_exhibit)
    
    app.run(debug=True, port=5000)

