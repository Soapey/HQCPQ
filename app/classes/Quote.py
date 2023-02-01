import os
import win32com.client as win32
from datetime import datetime
from tkinter import Tk, messagebox
from tkinter.filedialog import askdirectory
from fpdf import FPDF
from app.classes.QuoteItem import QuoteItem
from app.db.config import get_cursor_type


class Quote:
    def __init__(
        self,
        id: int,
        date_created: datetime,
        date_required: datetime,
        name: str,
        address: str,
        suburb: str,
        contact_number: str,
        kilometres: int,
    ) -> None:
        self.id = id
        self.date_created = date_created
        self.date_required = date_required
        self.name = name
        self.address = address
        self.suburb = suburb
        self.contact_number = contact_number
        self.kilometres = kilometres

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({vars(self)})"

    def items(
        self, all_quote_items: dict[int, QuoteItem] = None
    ) -> dict[int, QuoteItem]:

        if all_quote_items:
            return {
                qi.id: qi for qi in all_quote_items.values() if qi.quote_id == self.id
            }

        return QuoteItem.get(quote_id=self.id)

    def total_inc_gst(self, all_quote_items: dict[int, QuoteItem] = None) -> float:

        quote_items: dict[int, QuoteItem] = None
        if all_quote_items:
            quote_items = self.items(all_quote_items)
        else:
            quote_items = self.items()

        return 1.1 * sum(
            [
                (
                    (qi.transport_rate_ex_gst + qi.product_rate_ex_gst)
                    * qi.vehicle_combination_net
                )
                for qi in quote_items.values()
            ]
        )

    def insert(self):

        cur_type = get_cursor_type()

        with cur_type() as cur:

            if not cur:
                return

            self.id = cur.execute(
                """
                INSERT INTO quote (date_created, date_required, name, address, suburb, contact_number, kilometres) 
                OUTPUT INSERTED.id
                VALUES (?, ?, ?, ?, ?, ?, ?);
                """,
                [
                    self.date_created.date(),
                    self.date_required.date(),
                    self.name,
                    self.address,
                    self.suburb,
                    self.contact_number,
                    self.kilometres,
                ],
            ).fetchone()[0]

    def update(self):

        cur_type = get_cursor_type()

        with cur_type() as cur:

            if not cur:
                return

            cur.execute(
                """
                UPDATE quote 
                SET date_created = ?, date_required = ?, name = ?, address = ?, suburb = ?, contact_number = ?, kilometres = ? 
                WHERE id = ?;
                """,
                [
                    self.date_created.date(),
                    self.date_required.date(),
                    self.name,
                    self.address,
                    self.suburb,
                    self.contact_number,
                    self.kilometres,
                    self.id,
                ],
            )

    def delete(self):

        cur_type = get_cursor_type()

        with cur_type() as cur:

            if not cur:
                return

            cur.execute(
                """
                DELETE FROM quote 
                WHERE id = ?;
                """,
                [self.id],
            )

    def export_with_excel(self):

        # Dialog box requests user to select destination folder.
        Tk().withdraw()
        directory_path = askdirectory()

        # Return if no destination folder was selected.
        if not directory_path:
            return

        try:
            # Create excel object
            excel = win32.Dispatch("Excel.Application")

            # Open the workbook and read the first worksheet to a variable.
            wb = excel.Workbooks.Open(os.path.abspath(r"files\quote_template.xlsx"))
            ws = wb.Worksheets["Sheet1"]

            # Write all Quote attribute values to the worksheet.
            # (General values)
            ws.Cells(9, 1).Value = self.name
            ws.Cells(10, 1).Value = self.address
            ws.Cells(11, 1).Value = self.suburb
            ws.Cells(12, 1).Value = self.contact_number
            ws.Cells(8, 4).Value = self.id
            ws.Cells(9, 4).Value = datetime.strftime(self.date_created, "%d/%m/%Y")
            ws.Cells(15, 4).Value = self.total_inc_gst()

            # (Quote Items)
            for index, quote_item in enumerate(self.items().values()):
                ws.Cells(20 + index, 1).Value = quote_item.vehicle_combination_net
                ws.Cells(20 + index, 2).Value = quote_item.product_name
                ws.Cells(20 + index, 3).Value = quote_item.vehicle_combination_name
                ws.Cells(20 + index, 4).Value = quote_item.total_inc_gst()
                ws.Cells(20 + index, 4).NumberFormat = "$#,##0.00"

                ws.Range(
                    ws.Cells(20 + index, 1), ws.Cells(20 + index, 4)
                ).HorizontalAlignment = 3

            # Clean file name of illegal characters before exporting with it.
            illegal_characters: str = r'*."/\\[]:;|,'
            file_name: str = f"Hunter Quarries Quote #{self.id} - {self.name} ({datetime.strftime(self.date_created, '%d-%m-%Y')})"
            for illegal_character in illegal_characters:
                file_name = file_name.replace(illegal_character, "")

            full_path: str = rf"{directory_path}\{file_name}.pdf"

            # Export the worksheet as a PDF to the selected desination folder.
            ws.ExportAsFixedFormat(0, os.path.abspath(full_path))

            # Confirmation messagebox to confirm that the Quote was exported to a pdf successfully.
            messagebox.showinfo(
                title="Export Success",
                message=f"Quote was successfully exported to path:\n\n{full_path}",
            )
        except Exception as e:
            messagebox.showerror(message=e)
        finally:
            # Close the workbook regardless if export succeeds or fails.
            wb.Close(False)

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



        pdf = FPDF('P', 'mm', 'A4')
        pdf.add_page()
        pdf.set_font("Arial", "", 14)
        pdf.cell(40, 10, 'QUOTE')
        pdf.output(full_path, "F")

    @classmethod
    def get(cls, id: int = None) -> dict:

        records: list[tuple] = None

        cur_type = get_cursor_type()

        with cur_type() as cur:

            if not cur:
                return dict()

            if not id:
                records = cur.execute(
                    """
                    SELECT id, date_created, date_required, name, address, suburb, contact_number, kilometres 
                    FROM quote;
                    """
                ).fetchall()

            else:
                records = cur.execute(
                    """
                    SELECT id, date_created, date_required, name, address, suburb, contact_number, kilometres
                    FROM quote 
                    WHERE id = ?;
                    """,
                    [id],
                ).fetchall()

        return {
            q.id: q
            for q in [
                Quote(
                    r[0],
                    datetime.strptime(r[1], "%Y-%m-%d"),
                    datetime.strptime(r[2], "%Y-%m-%d"),
                    r[3],
                    r[4],
                    r[5],
                    r[6],
                    r[7],
                )
                for r in records
            ]
        }
