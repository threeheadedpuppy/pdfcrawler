import os, sys
import argparse
import re
import webbrowser
from pypdf import PdfReader

urlRegexString = "((http|https)://)[-a-zA-Z0-9@:%._\\+~#?&//=]{2,256}\\.[a-z]{2,6}\\b([-a-zA-Z0-9@:%._\\+~#?&//=]*)"
urlRegex = re.compile(urlRegexString)
interactive = False

def print_links(links):
    for link in links:
        print(link)

def open_links(links):
    print(f"Opening {links} all links")
    for link in links:
        webbrowser.open_new_tab(link)
        
def parse_pdf(filename):
    links = []
    def add_link(link):
        if link.startswith('mailto@'):
            return
        if link in links:
            return
        if not "://" in link:
            link = "http://" + link
        links.append(link)

    reader = PdfReader(filename)
    text = ""

    for page in reader.pages:
        text += page.extract_text() + "\n"

        if '/Annots' in page:
            for annotation in page['/Annots']:
                annotation_object = reader.get_object(annotation)
                if annotation_object['/Subtype'] == '/Link':
                    annotation_data = annotation_object['/A']
                    if '/URI' in annotation_data:
                        add_link(annotation_data['/URI'])
                    else:
                        raise Exception("Didn't understand link annotation - hand over to a coder, they'll sort it")

    for entry in re.finditer(urlRegex, text):
        add_link(entry.group(0))
    return links

def main(args):
    links = []

    for file in args.filename:
        if not os.path.exists(file):
            print(f"File not found {file}")
            continue
        links.extend(parse_pdf(file))

    if args.interactive:
        print("\n")
        print(f"Found {len(links)} links\n")
        while(True):
            inputstr = input("Enter o to open link(s), p to print, or any other key to exit:\n")
            if inputstr.lower() == 'o':
                open_links(links)
            elif inputstr.lower() == 'p':
                print_links(links)
            else:
                print("Exiting")
                break
    else:
        print_links(links)

    if args.open:
        open_links(links)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Parses PDF and outputs http links, optionally opening in a webbrowser")
    parser.add_argument("--interactive", "-i", action="store_true", help="Prompts user for action after parsing")
    parser.add_argument("--open", "-o", action="store_true", help="Opens all in a browser")
    parser.add_argument("filename", help="PDF file(s) to read", nargs="+")
    args = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_help()
        exit(1)
    main(args)
