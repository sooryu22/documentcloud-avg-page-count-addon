"""
This is a Average Page Count add-on for DocumentCloud.

It demonstrates how to write a add-on which can be activated from the
DocumentCloud add-on system and run using Github Actions.  It receives data
from DocumentCloud via the request dispatch and writes data back to
DocumentCloud using the standard API
"""

import sys
from documentcloud.addon import AddOn
import csv


class AvgPageCount(AddOn):
    """An Average Page Count Add-On for DocumentCloud."""

    def main(self):
        """The main add-on functionality goes here."""

        # get documents id array
        documents = self.data.get("documents")

        if not documents:
            sys.exit("Please select at least one document")

        for document in documents:
            try:
                int(document)
            except:
                sys.exit("Please only provide an integer form of document id")

        self.set_message("Beginning average page count!")

        doc_objects = [0]*len(documents)
        doc_selected = len(documents)
        page_total = 0

        min_page = self.client.documents.get(int(documents[0])).page_count
        max_page = self.client.documents.get(int(documents[0])).page_count
        min_page_doc = self.client.documents.get(int(documents[0]))
        max_page_doc = self.client.documents.get(int(documents[0]))

        for i in range(doc_selected):

            doc_objects[i] = self.client.documents.get(int(documents[i]))

            page_total += doc_objects[i].page_count
            if doc_objects[i].page_count < min_page:
                min_page = doc_objects[i].page_count
                min_page_doc = doc_objects[i]
            if doc_objects[i].page_count > max_page:
                max_page = doc_objects[i].page_count
                max_page_doc = doc_objects[i]
        avg_page_cnt = round(page_total/doc_selected, 2)

        with open("avg_page_count_for_"+str(doc_selected)+"_docs"+".csv", "w+") as file_:
            field_names = ['total_page',
                           'average_page_count', 'min_page', 'max_page']
            writer = csv.DictWriter(file_, fieldnames=field_names)

            writer.writeheader()
            writer.writerow({'total_page': page_total,
                            'average_page_count': avg_page_cnt,
                             'min_page': min_page_doc.pdf_url,
                             'max_page': max_page_doc.pdf_url})

            self.upload_file(file_)


if __name__ == "__main__":
    AvgPageCount().main()
