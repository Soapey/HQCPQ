from datetime import datetime

import win32com.client

from hqcpq.classes.QuoteItem import QuoteItem
from hqcpq.classes.QuotePDF import QuotePDF
from hqcpq.classes.QuoteSpecialCondition import QuoteSpecialCondition
from hqcpq.classes.SpecialCondition import SpecialCondition
from hqcpq.db.SQLiteUtil import SQLiteConnection


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

    def export(self, notification=True):
        return QuotePDF(self).export(notification)

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
        special_conditions = self.special_conditions().values()

        # Create bulleted list of special conditions
        bullet_point = u"\u2022"
        bullet_points = []
        if special_conditions:
            for special_condition in special_conditions:
                message = special_condition.message.replace("\n", "\n   ")
                bullet_points.append(f"{bullet_point} {message}")
        bullet_points = '\n'.join(bullet_points)

        # Construct email body
        email_body = """Hi XXXX,

Thanks for giving Hunter Quarries the opportunity to provide a quotation for the Project Name. 

Please find quotation XXXX attached 

*Please note*  
* Quotation only. Price may vary once final truck weights are determined.
* Rocks vary in size within specified range.

Special Conditions:
-	Products are subject to availability and an agreed offtake schedule.
-	Bookings E: orders@hunterquarries.com.au, M: 0490 084 048 or T: 4050 0304 option 1.
-	Quarry Operating Hours: Mon to Fri 6am to 4.30pm, Sat 6am to 12 noon.
-	Delivery by Truck and Dog with min freight of 32t unless Rigids are specified in the quotation. 
-	Conformance to site specifications must be confirmed by the customer prior to supply. Hunter Quarries takes no responsibility for checking materials meets site specifications. 
-	Hunter Quarries can supply materials test results upon request.
-	Site access must be suitable to receive goods. If deemed unsuitable on arrival by the driver, product will be returned to the quarry & credited, however freight charges will apply. 
-	Site inspection & VMP required prior to acceptance of supply & delivery. 
-	Booking to be confirmed by 12 noon business day prior to delivery. Transport cancellation fee applicable if canceled after this time (T&D $880 ex gst, Rigid $600 ex gst).
-	Waiting time fee applicable after the first 20 minutes on-site, charged in 15-minute increments.
-	If the delivery vehicle is damaged and/or becomes bogged, the customer shall be responsible for all costs of repairs and/or towing. 
-	Payment required via credit card per load once final weights are determined, prior to despatch. 
-	COD terms are required for 8 weeks till a trading history is established, then payment terms will be reviewed.
-	SMZ20 requires the following RFI’s - i) PSD increase on the 19.0mm sieve to 100% passing - ii) PSD increase on the 2.36mm lower limit to 30% passing - iii) T103 Exemption.
-	CMS R11 BH requires the following RFI’s – i) 0.075mm sieve 0-12% passing – ii) frequency of testing. R11 SO requires RFI i) frequency of testing. 
-	Large rocks are supplied within listed size ranges only, picked by the operator with a reference stockpile as a guide. 

Please be in contact if you require any further information.

Kind regards,""".strip()


        try:
            attachment_path = self.export(notification=False)

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

            # Display the email
            mail.Display()

        except Exception as e:
            print("An error occurred:", e)




