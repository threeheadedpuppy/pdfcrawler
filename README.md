# pdfcrawler
Iterate through pdfs and prints out URLs

## Prerequisites
[python 3.7](https://www.python.org/downloads/) or higher
[pipenv](https://pypi.org/project/pipenv/#installation)

To install:-
```sh
# Extract files into a directory, then from that directory, install virtual environment, using
pipenv install
```

Usage information:-
```sh
pipenv run python crawler.py --help
```

To print urls in a pdf:-
```sh
pipenv run python crawler.py example.pdf
```

To open links in a pdf:-
```sh
pipenv run python crawler.py example.pdf -i
# When prompted, type an 'o'
```
