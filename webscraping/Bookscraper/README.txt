This is a webscraping script to scrape full textbooks off of proquest.safaribooksonline.com and
convert them into readable PDFs with consistent formatting.


This script was written for Python 3.6
One of the current dependencies is currently in alpha (wkhtmltopdf 0.13)
The script is currently only configured for windows.

There are a number of non-standard
dependencies (note, you will need the conda package manager):

BeautifulSoup4
pdfkit
PyPDF2

install commands:
pip3.6 install beautifulsoup4
pip3.6 install pdfkit
conda install -c conda-forge pypdf2

PyPDF2 also has a dependency on wkhtmltopdf 0.13, which can be found at
https://wkhtmltopdf.org/downloads.html
(Windows (MSVC 2013) 64-bit) under bleeding edge releases.

Usage:
python BookScraper.py -u <url>
where <url> is the url for the cover page of the textbook on safaribooksonline


