import os
from datetime import datetime

from fpdf import FPDF

from hqcpq.gui.classes.InfoMessageBox import InfoMessageBox
from hqcpq.gui.classes.ErrorMessageBox import ErrorMessageBox
from hqcpq.helpers.io import join_to_project_folder
from hqcpq.helpers.general import select_directory, insert_newline_at_max_length





class QuotePDF(FPDF):
    def __init__(self, quote):

        super().__init__()

        self.quote = quote
        self.items = quote.items()
        self.special_conditions = quote.special_conditions()

        self.add_page()

        self.column_width_mm = (self.w - 20) // 4
        self.row_height_mm = 10

        self._header()
        self._body()
        self._footer()

    def adjust_font_size(self, cell_width_mm, datum, max_characters):
        font_size = 8  # Initial font size

        if len(datum) > max_characters:
            overflow = len(datum) - max_characters
            increments = overflow // 5
            font_size -= 1.1 * increments

        return font_size

    def _header(self):

        # Header
        self.set_font("Helvetica", "B", 20)
        self.cell(self.column_width_mm * 2, self.row_height_mm, "QUOTE")

        img_path = join_to_project_folder(os.path.join("hqcpq", "assets", "hq_keq_logos.jpg"))
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
            self.column_width_mm * 4, self.row_height_mm, "ITEMS", 1, align="C", fill=True
        )
        self.ln(self.row_height_mm)

        self.set_font("Helvetica", "B", 10)
        self.cell(
            self.column_width_mm, self.row_height_mm, "Tonnes", 1, align="C", fill=True
        )
        self.cell(
            self.column_width_mm, self.row_height_mm, "Product", 1, align="C", fill=True
        )
        self.cell(
            self.column_width_mm,
            self.row_height_mm,
            "via",
            1,
            align="C",
            fill=True,
        )
        self.cell(
            self.column_width_mm,
            self.row_height_mm,
            "Total inc. GST",
            1,
            align="C",
            fill=True,
        )
        self.ln(self.row_height_mm)

        # QuoteItems
        max_quote_item_character_width = 35
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

        # QuoteItems
        for row_index, row in enumerate(data):
            for datum in row:
                font_size = self.adjust_font_size(self.column_width_mm, datum, 35)
                self.set_font("Helvetica", "", font_size)
                self.cell(self.column_width_mm, self.row_height_mm, datum, border=1, align="L")
            self.ln()

        self.ln()

        # Special conditions' header.
        self.set_font("Helvetica", "B", 10)
        self.cell(
            self.column_width_mm * 4,
            self.row_height_mm,
            "SPECIAL CONDITIONS",
            border=1,
            align="C",
            fill=True,
        )
        self.ln(self.row_height_mm)

        # Special conditions.
        self.set_font("Helvetica", "", 8)
        for special_condition in self.special_conditions.values():
            lines = insert_newline_at_max_length(special_condition.message, 140)
            message = '\n'.join(lines)
            added_vertical_space = (len(lines) - 1) * 1
            self.multi_cell(
                w=self.column_width_mm * 4,
                h=(self.row_height_mm - 4) + added_vertical_space,
                txt=message,
                border=1,
            )

    def _footer(self):

        # Business details.
        self.set_font("Helvetica", "B", 10)
        self.multi_cell(
            self.column_width_mm * 4,
            self.row_height_mm,
            "Karuah East Quarry Pty Ltd trading as Hunter Quarries - ABN: 80 141 505 035",
        )

    def export(self, notification=True):

        # Dialog box requests user to select destination folder.
        directory_path = select_directory()

        # Return if no destination folder was selected.
        if not directory_path:
            return None

        try:
            # Clean file name of illegal characters before exporting with it.
            illegal_characters: str = r'*."/\\[]:;|,'
            file_name = (
                f"Hunter Quarries Quote #{self.quote.id} - "
                f"{self.quote.name} ({datetime.strftime(self.quote.date_created, '%d-%m-%Y')})"
            )
            for illegal_character in illegal_characters:
                file_name = file_name.replace(illegal_character, "")

            full_path: str = rf"{directory_path}\{file_name}.pdf"

            self.output(full_path)

            # Confirmation messagebox to confirm that the Quote was exported to a pdf successfully.
            if notification:
                InfoMessageBox(f"Quote was successfully exported to path:\n\n{full_path}")

            return full_path

        except Exception as e:
            ErrorMessageBox(str(e))
            return None
