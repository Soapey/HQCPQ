import os
from datetime import datetime

import win32com.client

from hqcpq.classes.QuoteItem import QuoteItem
from hqcpq.classes.QuotePDF import QuotePDF
from hqcpq.classes.QuoteSpecialCondition import QuoteSpecialCondition
from hqcpq.classes.SpecialCondition import SpecialCondition
from hqcpq.db.SQLiteUtil import SQLiteConnection
from hqcpq.helpers.io import get_email_body, get_documents_directory


class Quote:
    def __init__(
        self,
        obj_id: int,
        date_created: datetime,
        date_required: datetime,
        name: str,
        address: str,
        suburb: str,
        contact_number: str,
        email: str,
        memo: str,
        kilometres: int,
        completed: bool,
    ):
        self.id = obj_id
        self.date_created = date_created
        self.date_required = date_required
        self.name = name
        self.address = address
        self.suburb = suburb
        self.contact_number = contact_number
        self.email = email
        self.memo = memo
        self.kilometres = kilometres
        self.completed = completed

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({vars(self)})"

    def export(self, notification=True, save_directory_path=None):
        return QuotePDF(self).export(notification, save_directory_path)

    def items(self):
        return QuoteItem.get_all_by_quote_id(self.id)

    def special_conditions(self):
        all_special_conditions = SpecialCondition.get_all()
        quote_special_conditions = QuoteSpecialCondition.get_by_quote(self.id)
        return {qsc.special_condition_id: all_special_conditions[qsc.special_condition_id] for qsc in quote_special_conditions.values() if qsc.is_checked}

    def total_inc_gst(self):
        quote_items = self.items()

        return 1.1 * sum(
            [
                (
                    (quote_item.transport_rate_ex_gst + quote_item.product_rate_ex_gst)
                    * quote_item.vehicle_combination_net
                )
                for quote_item in quote_items.values()
            ]
        )

    def insert(self):
        query = ("INSERT INTO quote (date_created, date_required, name, address, suburb, contact_number, email, memo, "
                 "kilometres, completed) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)")
        with SQLiteConnection() as cur:
            cur.execute(query, (
                self.date_created.date(),
                self.date_required.date(),
                self.name,
                self.address,
                self.suburb,
                self.contact_number,
                self.email,
                self.memo,
                self.kilometres,
                int(self.completed)
            ))
            self.id = cur.lastrowid
        return self

    def update(self):
        query = "UPDATE quote SET date_created = ?, date_required = ?, name = ?, address = ?, suburb = ?, " \
                "contact_number = ?, email = ?, memo = ?, kilometres = ?, completed = ? WHERE id = ?"
        with SQLiteConnection() as cur:
            cur.execute(query, (
                self.date_created.date(),
                self.date_required.date(),
                self.name,
                self.address,
                self.suburb,
                self.contact_number,
                self.email,
                self.memo,
                self.kilometres,
                int(self.completed),
                self.id
            ))
        return self

    @classmethod
    def delete(cls, obj_id):
        query = "DELETE FROM quote WHERE id = ?"
        with SQLiteConnection() as cur:
            cur.execute(query, (obj_id,))

    @classmethod
    def get(cls, obj_id):
        query = "SELECT * FROM quote WHERE id = ?"
        with SQLiteConnection() as cur:
            cur.execute(query, (obj_id,))
            row = cur.fetchone()
            if row:
                return cls(
                    obj_id=row[0],
                    date_created=datetime.strptime(row[1], "%Y-%m-%d"),
                    date_required=datetime.strptime(row[2], "%Y-%m-%d"),
                    name=row[3],
                    address=row[4],
                    suburb=row[5],
                    contact_number=row[6],
                    email=row[7],
                    memo=row[8],
                    kilometres=row[9],
                    completed=bool(row[10])
                )
        return None

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM quote"
        with SQLiteConnection() as cur:
            cur.execute(query)
            rows = cur.fetchall()
            return {
                row[0]: cls(
                    obj_id=row[0],
                    date_created=datetime.strptime(row[1], "%Y-%m-%d"),
                    date_required=datetime.strptime(row[2], "%Y-%m-%d"),
                    name=row[3],
                    address=row[4],
                    suburb=row[5],
                    contact_number=row[6],
                    email=row[7],
                    memo=row[8],
                    kilometres=row[9],
                    completed=bool(row[10]))
                for row in rows
            }

    def create_email(self):
        email_to = self.email.strip() if self.email else ""
        email_subject = f"Hunter Quarries Quote #{self.id} - {self.name} ({datetime.strftime(self.date_created, '%d-%m-%Y')})"
        email_body = get_email_body().replace("[customer_name]", self.name).replace("[quote_id]", str(self.id))

        save_directory_path = get_documents_directory()

        try:
            attachment_path = self.export(notification=False, save_directory_path=save_directory_path)

            # Create Outlook application object
            outlook = win32com.client.Dispatch("Outlook.Application")

            # Create a new mail item
            mail = outlook.CreateItem(0)  # 0 represents olMailItem enumeration constant

            # Set recipients
            mail.To = email_to  # Use ";" to separate multiple recipients

            # Set subject and body
            mail.Subject = email_subject
            mail.Body = email_body

            # Add attachments
            mail.Attachments.Add(attachment_path)

            if os.path.exists(attachment_path):
                os.remove(attachment_path)

            # Display the email
            mail.Display()

        except Exception as e:
            print("An error occurred:", e)




