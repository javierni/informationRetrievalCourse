"""
index.py
Author: Javier Nogueras Iso
Last update: 2024-09-07

Simple program to create an inverted index with the contents of text/xml files contained in a docs folder
This program is based on the whoosh library. See https://pypi.org/project/Whoosh/ .
Usage: python index.py -index <index folder> -docs <docs folder>
"""

from whoosh.index import create_in
from whoosh.fields import *

import os

import xml.etree.ElementTree as ET

def create_folder(folder_name):
    if (not os.path.exists(folder_name)):
        os.mkdir(folder_name)

class MyIndex:
    def __init__(self,index_folder):
        schema = Schema(path=ID(stored=True), content=TEXT)
        create_folder(index_folder)
        index = create_in(index_folder, schema)
        self.writer = index.writer()

    def index_docs(self,docs_folder):
        if (os.path.exists(docs_folder)):
            for file in sorted(os.listdir(docs_folder)):
                # print(file)
                if file.endswith('.xml'):
                    self.index_xml_doc(docs_folder, file)
                elif file.endswith('.txt'):
                    self.index_txt_doc(docs_folder, file)
        self.writer.commit()

    def index_txt_doc(self, foldername,filename):
        file_path = os.path.join(foldername, filename)
        # print(file_path)
        with open(file_path) as fp:
            text = ' '.join(line for line in fp if line)
        # print(text)
        self.writer.add_document(path=filename, content=text)

    def index_xml_doc(self, foldername, filename):
        file_path = os.path.join(foldername, filename)
        # print(file_path)
        tree = ET.parse(file_path)
        root = tree.getroot()
        raw_text = "".join(root.itertext())
        # break into lines and remove leading and trailing space on each
        text = ' '.join(line.strip() for line in raw_text.splitlines() if line)
        # print(text)
        self.writer.add_document(path=filename,content=text)

if __name__ == '__main__':

    index_folder = '../whooshindex'
    docs_folder = '../docs'
    i = 1
    while i < len(sys.argv):
        if sys.argv[i] == '-index':
            index_folder = sys.argv[i + 1]
            i = i + 1
        elif sys.argv[i] == '-docs':
            docs_folder = sys.argv[i + 1]
            i = i + 1
        i = i + 1

    my_index = MyIndex(index_folder)
    my_index.index_docs(docs_folder)


