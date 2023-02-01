from fpdf import FPDF
from tkinter.filedialog import askdirectory
from app.classes.Quote import Quote
from datetime import datetime


class QuotePDF(FPDF):
    def __init__(self, quote: Quote):

        super().__init__()

        self.quote = quote
        self.page_width_mm = 210
        self.column_width_mm = (self.page_width_mm - 50) // 2
        self.row_height_mm = 10

        self.add_page()
        self._header()
        self._body()
        self._footer()

    def _header(self):

        # Header
        self.set_font("Arial", "B", 16)
        self.cell(40, 10, "QUOTE", False, 0)
        self.ln(20)

    def _body(self):

        # Supplier details.
        self.set_font("Arial", "B", 14)
        self.cell(self.column_width_mm, self.row_height_mm, "Hunter Quarries")
        self.ln(self.row_height_mm // 2)
        self.set_font("Arial", "", 12)
        self.cell(self.column_width_mm, self.row_height_mm, "Blue Rock Close")
        self.ln(self.row_height_mm // 2)
        self.cell(self.column_width_mm, self.row_height_mm, "Karuah, NSW 2324")
        self.ln(self.row_height_mm // 2)
        self.cell(self.column_width_mm, self.row_height_mm, "4050-0304")
        self.ln(20)

        # Customer details.

        # Row 1
        self.set_font("Arial", "B", 12)
        self.cell(self.column_width_mm, self.row_height_mm, "Customer")
        self.cell(self.column_width_mm, self.row_height_mm, "Quote Number", align="R")
        self.cell(
            self.column_width_mm, self.row_height_mm, str(self.quote.id), align="R"
        )
        self.ln(self.row_height_mm // 2)

        # Row 2
        self.set_font("Arial", "", 12)
        self.cell(self.column_width_mm, self.row_height_mm, self.quote.name)
        self.set_font("Arial", "B", 12)
        self.cell(self.column_width_mm, self.row_height_mm, "Quote Date", align="R")
        self.set_font("Arial", "", 12)
        self.cell(
            self.column_width_mm,
            self.row_height_mm,
            datetime.strftime(self.quote.date_created, "%d/%m/%Y"),
            align="R",
        )
        self.ln(self.row_height_mm // 2)

        # Row 3
        self.cell(self.column_width_mm, self.row_height_mm, self.quote.address)
        self.ln(self.row_height_mm // 2)

        # Row 4
        self.cell(self.column_width_mm, self.row_height_mm, self.quote.suburb)
        self.ln(self.row_height_mm // 2)

        # Row 5
        self.cell(self.column_width_mm, self.row_height_mm, self.quote.contact_number)
        self.ln(self.row_height_mm // 2)

        # Quote details.
        self.set_font("Arial", "B", 12)

    def _footer(self):

        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, "Page " + str(self.page_no()) + "/{nb}", 0, 0, "C")

    def export(self):

        # Dialog box requests user to select destination folder.
        directory_path = askdirectory()

        # Return if no destination folder was selected.
        if not directory_path:
            return

        # Clean file name of illegal characters before exporting with it.
        illegal_characters: str = r'*."/\\[]:;|,'
        file_name: str = f"test"
        for illegal_character in illegal_characters:
            file_name = file_name.replace(illegal_character, "")

        full_path: str = rf"{directory_path}\{file_name}.pdf"

        self.output(full_path, "F")


if __name__ == "__main__":

    q = Quote(
        1,
        datetime.today(),
        datetime.today(),
        "Grant Soper",
        "4 Bilmark Drive",
        "Raymond Terrace",
        "0481552395",
        33,
    )

    pdf = QuotePDF(q)
    pdf.export()
