"""
This is a Page Stats add-on for DocumentCloud.
This will return a csv file containing total pages, average number of pages, 
and link the largest and small document with their number of pages for a given selection of documents.

It demonstrates how to write a add-on which can be activated from the
DocumentCloud add-on system and run using Github Actions.  It receives data
from DocumentCloud via the request dispatch and writes data back to
DocumentCloud using the standard API
"""

from documentcloud.addon import AddOn
import csv


class PageStats(AddOn):
    """A Page Stats Add-On for DocumentCloud."""

    def main(self):
        """The main add-on functionality goes here."""

        if not self.documents:
            print("not documents")
            self.set_message("Please select at least one document")
            return

        self.set_message("Beginning page stats!")

        doc_selected = len(self.documents)
        page_total = 0
        min_page_count = float("inf")
        max_page_count = 0
        min_page_doc = None
        max_page_doc = None

        for document in self.client.documents.list(id__in=self.documents):
            page_total += document.page_count
            if document.page_count < min_page_count:
                min_page_count = document.page_count
                min_page_doc = document
            if document.page_count > max_page_count:
                max_page_count = document.page_count
                max_page_doc = document

        avg_page_cnt = round(page_total / doc_selected, 2)

        with open(
            "page_stats_for_" + str(doc_selected) + "_docs" + ".csv", "w+"
        ) as file_:
            field_names = [
                "total_page",
                "average_page_count",
                "min_page_count",
                "max_page_count",
                "min_page_url",
                "max_page_url",
            ]
            writer = csv.DictWriter(file_, fieldnames=field_names)

            writer.writeheader()
            writer.writerow(
                {
                    "total_page": page_total,
                    "average_page_count": avg_page_cnt,
                    "min_page_count": min_page_count,
                    "max_page_count": max_page_count,
                    "min_page_url": min_page_doc.pdf_url,
                    "max_page_url": max_page_doc.pdf_url,
                }
            )
            self.upload_file(file_)
        self.set_message("Page stats end!")


if __name__ == "__main__":
    PageStats().main()
