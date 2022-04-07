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

        documents = self.data.get("documents")

        if not documents:
            sys.exit("Please select at least one document")

        for document in documents:
            try:
                int(document)
            except:
                sys.exit("Please only provide an integer")

        doc_objects = [0]*len(documents)
        doc_selected = len(documents)
        page_total = 0

        for i in range(doc_selected):

            doc_objects[i] = self.client.documents.get(int(documents[i]))
            page_total += doc_objects[i].page_count
        avg_page_cnt = round(page_total/doc_selected, 2)

        with open("average_page_count.csv", "w+") as file_:
            field_names = ['total_page', 'average_page_count']
            writer = csv.DictWriter(file_, fieldnames=field_names)

            writer.writeheader()
            writer.writerow({'total_page': page_total,
                            'average_page_count': avg_page_cnt})

            self.upload_file(file_)


if __name__ == "__main__":
    AvgPageCount().main()
