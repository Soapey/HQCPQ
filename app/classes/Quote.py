from datetime import datetime
from .QuoteItem import QuoteItem
from app.db.SQLCursor import SQLCursor
from tkinter import Tk, messagebox
from tkinter.filedialog import askdirectory
import win32com.client as win32
import os


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

        with SQLCursor() as cur:

            if not cur:
                return

            cur.execute(
                """
                INSERT INTO quote (date_created, date_required, name, address, suburb, contact_number, kilometres) 
                VALUES (?, ?, ?, ?, ?, ?, ?);
                """,
                (
                    self.date_created.date(),
                    self.date_required.date(),
                    self.name,
                    self.address,
                    self.suburb,
                    self.contact_number,
                    self.kilometres,
                ),
            )

            res = cur.execute(
                """
                SELECT id 
                FROM quote 
                WHERE ROWID = last_insert_rowid();
                """
            ).fetchall()

            if res:
                last_record = res[0]
                self.id = last_record[0]

    def update(self):

        with SQLCursor() as cur:

            if not cur:
                return

            cur.execute(
                """
                UPDATE quote 
                SET date_created = ?, date_required = ?, name = ?, address = ?, suburb = ?, contact_number = ?, kilometres = ? 
                WHERE id = ?;
                """,
                (
                    self.date_created.date(),
                    self.date_required.date(),
                    self.name,
                    self.address,
                    self.suburb,
                    self.contact_number,
                    self.kilometres,
                    self.id,
                ),
            )

    def delete(self):

        with SQLCursor() as cur:

            if not cur:
                return

            cur.execute(
                """
                DELETE FROM quote 
                WHERE id = ?;
                """,
                (self.id,),
            )

    def export(self):

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
            wb = excel.Workbooks.Open(os.path.abspath(r"app\quote_template.xlsx"))
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

            # Export the worksheet as a PDF to the selected desination folder.
            file_name: str = f"Hunter Quarries Quote #{self.id} ({datetime.strftime(self.date_created, '%d-%m-%Y')})"
            ws.ExportAsFixedFormat(
                0, os.path.abspath(rf"{directory_path}\{file_name}.pdf")
            )
        except Exception as e:
            messagebox.showerror(message=e)
        finally:
            # Close the workbook regardless if export succeeds or fails.
            wb.Close(False)
            excel.Quit()

    @classmethod
    def get(cls, id: int = None) -> dict:

        records: list[tuple] = None

        with SQLCursor() as cur:

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
                    FROM quote WHERE id = ?;
                    """,
                    (id,),
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
