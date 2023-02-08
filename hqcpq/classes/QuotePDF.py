from datetime import datetime
from fpdf import FPDF
from tkinter import messagebox
from tkinter.filedialog import askdirectory
from hqcpq.helpers import resource_path
from hqcpq.classes.Toast import Toast


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
        self.set_font("Helvetica", "B", 20)
        self.cell(self.column_width_mm * 2, self.row_height_mm, "QUOTE")

        img_path = resource_path("hqcpq\\hq_keq_logos.jpg")
        img_width_px = 258
        img_height_px = 107
        height_ratio = img_height_px / img_width_px
        img_desired_width = 68
        img_desired_height = img_desired_width * height_ratio

        self.image(
            img_path,
            self.w - self.r_margin - img_desired_width,
            0,
            img_desired_width,
            img_desired_height,
        )

        self.ln(20)

    def _body(self):

        # Supplier details.
        self.set_font("Helvetica", "B", 14)
        self.cell(self.column_width_mm * 2, self.row_height_mm, "Hunter Quarries")
        self.ln(self.row_height_mm // 2)

        self.set_font("Helvetica", "", 12)
        self.cell(self.column_width_mm * 2, self.row_height_mm, "Blue Rock Close")
        self.ln(self.row_height_mm // 2)

        self.cell(self.column_width_mm * 2, self.row_height_mm, "Karuah, NSW 2324")
        self.ln(self.row_height_mm // 2)

        self.cell(self.column_width_mm * 2, self.row_height_mm, "4050-0304")
        self.ln(self.row_height_mm // 2)

        self.cell(
            self.column_width_mm * 2, self.row_height_mm, "orders@hunterquarries.com.au"
        )
        self.ln(20)

        # Customer details.
        # Row 1
        self.set_font("Helvetica", "B", 12)
        self.cell(self.column_width_mm * 2, self.row_height_mm, "Customer")
        self.cell(self.column_width_mm, self.row_height_mm, "Quote Number", align="R")
        self.cell(
            self.column_width_mm, self.row_height_mm, str(self.quote.id), align="R"
        )
        self.ln(self.row_height_mm // 2)

        # Row 2
        self.set_font("Helvetica", "", 12)
        self.cell(self.column_width_mm * 2, self.row_height_mm, self.quote.name)
        self.set_font("Helvetica", "B", 12)
        self.cell(self.column_width_mm, self.row_height_mm, "Quote Date", align="R")
        self.set_font("Helvetica", "", 12)
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
        self.set_font("Helvetica", "B", 20)
        self.cell(
            self.column_width_mm * 2, self.row_height_mm, "Total inc. GST", 1, align="R"
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
        self.set_font("Helvetica", "B", 12)
        self.set_fill_color(217, 217, 217)
        self.cell(
            self.column_width_mm * 4, self.row_height_mm, "ITEMS", 1, align="C", fill=1
        )
        self.ln(self.row_height_mm)

        self.set_font("Helvetica", "B", 10)
        self.cell(
            self.column_width_mm, self.row_height_mm, "Tonnes", 1, align="C", fill=1
        )
        self.cell(
            self.column_width_mm, self.row_height_mm, "Product", 1, align="C", fill=1
        )
        self.cell(
            self.column_width_mm,
            self.row_height_mm,
            "via",
            1,
            align="C",
            fill=1,
        )
        self.cell(
            self.column_width_mm,
            self.row_height_mm,
            "Total inc. GST",
            1,
            align="C",
            fill=1,
        )
        self.ln(self.row_height_mm)

        # QuoteItems
        self.set_font("Helvetica", "", 8)
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

        self.ln(self.row_height_mm)

    def _footer(self):

        special_conditions = [
            (
                "Products are subject to availability and an agreed offtake schedule.",
                self.row_height_mm,
            ),
            ("Rates valid for 8 weeks from time of quoting.", self.row_height_mm),
            (
                "Quarry operating hours: Mon to Fri 6:00am to 4:30pm, Sat 6:00am to 12:00pm (noon).",
                self.row_height_mm,
            ),
            (
                "Conformance to site specifications must be confirmed by the customer prior to supply. Hunter Quarries takes no responsibility for checking materials meets site specifications.",
                self.row_height_mm + 5,
            ),
            (
                "Hunter Quarries can supply test results upon request.",
                self.row_height_mm,
            ),
            (
                "Payment required via credit card per load once final weights determined & prior to despatch.",
                self.row_height_mm,
            ),
            (
                "Site access must be suitable to receive goods. If deemed unsuitable on arrival by the driver, product will be returned to the quarry & credited, however freight charges will apply.",
                self.row_height_mm + 5,
            ),
        ]

        # Special conditions header.
        self.set_font("Helvetica", "B", 10)
        self.cell(
            self.column_width_mm * 4,
            self.row_height_mm,
            "SPECIAL CONDITIONS",
            border=1,
            align="C",
            fill=1,
        )
        self.ln(self.row_height_mm)

        # Special conditions.
        self.set_font("Helvetica", "", 8)
        for special_condition in special_conditions:
            self.multi_cell(
                self.column_width_mm * 4,
                special_condition[1],
                special_condition[0],
                border=1,
                ln=3,
                max_line_height=self.font_size_pt,
            )
            self.ln(special_condition[1])

        # Business details.
        self.set_font("Helvetica", "B", 10)
        self.multi_cell(
            self.column_width_mm * 4,
            self.row_height_mm,
            "Karuah East Quarry Pty Ltd trading as Hunter Quarries - ABN: 80 141 505 035",
        )

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
            Toast(
                "Export Success",
                f"Quote was successfully exported to path:\n\n{full_path}",
            ).show()

        except Exception as e:
            messagebox.showerror(message=e)
