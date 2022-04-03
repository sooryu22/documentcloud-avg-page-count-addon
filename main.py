"""
This is a Average Page Count add-on for DocumentCloud.

It demonstrates how to write a add-on which can be activated from the
DocumentCloud add-on system and run using Github Actions.  It receives data
from DocumentCloud via the request dispatch and writes data back to
DocumentCloud using the standard API
"""

from documentcloud.addon import AddOn
from addon import AddOn
import csv


class AvgPageCount(AddOn):
    """An example Add-On for DocumentCloud."""

    def main(self):
        # fetch your add-on specific data
        if not self.documents:
            self.set_message("Please select at least one document")
            return

        with open("average_page_count.txt", "w+") as file_:
            for document in self.client.documents.list(id__in=self.documents):

                page_total = + document.page()
            num_docs = self.documents.count()
            avg_page = round(page_total/num_docs)

            file_.write("Average page number for " + num_docs +
                        "documents is: " + avg_page)
            self.upload_file(file_)

        self.set_message("Average Page Count end!")


if __name__ == "__main__":
    AvgPageCount().main()
