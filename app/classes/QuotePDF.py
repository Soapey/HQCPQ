from datetime import datetime
from fpdf import FPDF
from tkinter import messagebox
from tkinter.filedialog import askdirectory


A4_PAGE_WIDTH_MM = 210
A4_PAGE_BORDER = 20


class QuotePDF(FPDF):
    def __init__(self, quote):

        super().__init__()

        self.quote = quote
        self.items = quote.items()
        self.column_width_mm = self.epw / 4
        self.row_height_mm = 10

        self.add_page()
        self._header()
        self._body()
        self._footer()

    def _header(self):

        # Header
        self.set_font("Arial", "B", 20)
        self.cell(40, 10, "QUOTE", False, 0)
        self.ln(20)

    def _body(self):

        # Supplier details.
        self.set_font("Arial", "B", 14)
        self.cell(self.column_width_mm * 2, self.row_height_mm, "Hunter Quarries")
        self.ln(self.row_height_mm // 2)

        self.set_font("Arial", "", 12)
        self.cell(self.column_width_mm * 2, self.row_height_mm, "Blue Rock Close")
        self.ln(self.row_height_mm // 2)

        self.cell(self.column_width_mm * 2, self.row_height_mm, "Karuah, NSW 2324")
        self.ln(self.row_height_mm // 2)
        self.cell(self.column_width_mm * 2, self.row_height_mm, "4050-0304")
        self.ln(20)

        # Customer details.
        # Row 1
        self.set_font("Arial", "B", 12)
        self.cell(self.column_width_mm * 2, self.row_height_mm, "Customer")
        self.cell(self.column_width_mm, self.row_height_mm, "Quote Number", align="R")
        self.cell(
            self.column_width_mm, self.row_height_mm, str(self.quote.id), align="R"
        )
        self.ln(self.row_height_mm // 2)

        # Row 2
        self.set_font("Arial", "", 12)
        self.cell(self.column_width_mm * 2, self.row_height_mm, self.quote.name)
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
        self.cell(self.column_width_mm * 2, self.row_height_mm, self.quote.address)
        self.ln(self.row_height_mm // 2)

        # Row 4
        self.cell(self.column_width_mm * 2, self.row_height_mm, self.quote.suburb)
        self.ln(self.row_height_mm // 2)

        # Row 5
        self.cell(
            self.column_width_mm * 2, self.row_height_mm, self.quote.contact_number
        )
        self.ln(self.row_height_mm)

        # Quote total inc GST.
        self.set_font("Arial", "B", 20)
        self.cell(
            self.column_width_mm * 2, self.row_height_mm, "Total Inc. GST", 1, align="R"
        )
        self.cell(
            self.column_width_mm * 2,
            self.row_height_mm,
            "${:,.2f}".format(self.quote.total_inc_gst()),
            1,
            align="R",
        )
        self.ln(self.row_height_mm)

        # QuoteItem details.
        # QuoteItem table headers.
        self.set_font("Arial", "B", 12)
        self.set_fill_color(217, 217, 217)
        self.cell(
            self.column_width_mm * 4, self.row_height_mm, "ITEMS", 1, align="C", fill=1
        )
        self.ln(self.row_height_mm)

        self.set_font("Arial", "B", 10)
        self.cell(
            self.column_width_mm, self.row_height_mm, "Tonnes", 1, align="C", fill=1
        )
        self.cell(
            self.column_width_mm, self.row_height_mm, "Product", 1, align="C", fill=1
        )
        self.cell(
            self.column_width_mm,
            self.row_height_mm,
            "via Combination",
            1,
            align="C",
            fill=1,
        )
        self.cell(
            self.column_width_mm,
            self.row_height_mm,
            "Total Inc. GST",
            1,
            align="C",
            fill=1,
        )
        self.ln(self.row_height_mm)

        # QuoteItems
        self.set_font("Arial", "", 8)
        data = [
            [
                str(quote_item.vehicle_combination_net),
                quote_item.product_name,
                quote_item.vehicle_combination_name,
                "${:,.2f}".format(quote_item.total_inc_gst()),
            ]
            for quote_item in self.items.values()
        ]

        for row in data:
            for datum in row:
                self.multi_cell(
                    self.column_width_mm,
                    self.row_height_mm,
                    datum,
                    border=1,
                    new_x="RIGHT",
                    new_y="TOP",
                )
            self.ln(self.row_height_mm)

    def _footer(self):
        pass

    def export(self):

        # Dialog box requests user to select destination folder.
        directory_path = askdirectory()

        # Return if no destination folder was selected.
        if not directory_path:
            return

        try:
            # Clean file name of illegal characters before exporting with it.
            illegal_characters: str = r'*."/\\[]:;|,'
            file_name: str = f"Hunter Quarries Quote #{self.quote.id} - {self.quote.name} ({datetime.strftime(self.quote.date_created, '%d-%m-%Y')})"
            for illegal_character in illegal_characters:
                file_name = file_name.replace(illegal_character, "")

            full_path: str = rf"{directory_path}\{file_name}.pdf"

            self.output(full_path, "F")

            # Confirmation messagebox to confirm that the Quote was exported to a pdf successfully.
            messagebox.showinfo(
                title="Export Success",
                message=f"Quote was successfully exported to path:\n\n{full_path}",
            )
        except Exception as e:
            messagebox.showerror(message=e)
