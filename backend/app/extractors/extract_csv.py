# import pandas as pd


# def extract_csv_records(csv_path):
#     df = pd.read_csv(csv_path)
#     records = []

#     filename = csv_path.lower()

#     for _, row in df.iterrows():

#         record = {}

#         # -------------------------
#         # Personal Details CSV
#         # -------------------------
#         if "personal" in filename:

#             record = {
#                 "doc_type": "personal_csv",
#                 "full_name": row.get("Full Name"),
#                 "email": row.get("Email"),
#                 "phone_number": row.get("Ph Number"),
#                 "address": row.get("Addr"),
#                 "age": row.get("Age"),
#                 "t_shirt_size": row.get("Merch Tshirt size"),
#             }

#         # -------------------------
#         # Bank Details CSV
#         # -------------------------
#         elif "bank" in filename:

#             record = {
#                 "doc_type": "bank_csv",
#                 "full_name": row.get("Name"),
#                 "email": row.get("Email"),
#                 "bank_name": row.get("Bank Name"),
#                 "account_number": row.get("Acc Number"),
#                 "ifsc_code": row.get("IFSC Code"),
#                 "account_holder_address":
#                     row.get("Acc Holder Address"),
#             }

#         if record.get("email"):
#             record["candidate_id"] = record["email"]
#             records.append(record)

#     return records

import pandas as pd
import os

def normalize_name(name):
    if pd.isna(name):
        return None

    return " ".join(
        str(name).upper().split()
    )

def extract_csv_records(csv_path):
    df = pd.read_csv(csv_path)
    records = []

    filename = csv_path.lower()

    for _, row in df.iterrows():

        record = {}

        # -------------------------
        # Personal Details CSV
        # -------------------------
        if "personal" in filename:

            record = {
                "doc_type": "personal_csv",
                "full_name": normalize_name(row.get("Full Name")),
                "date_of_birth": row.get("Date of Birth"),
                "email": row.get("Email"),
                "phone_number": row.get("Ph Number"),
                "address": row.get("Addr"),
                "age": row.get("Age"),
                "t_shirt_size": row.get("Merch Tshirt size"),
            }

        # -------------------------
        # Bank Details CSV
        # -------------------------
        elif "bank" in filename:

            record = {
                "doc_type": "bank_csv",
                "full_name": normalize_name(row.get("Name")),
                "email": row.get("Email"),
                "bank_name": row.get("Bank Name"),
                "account_number": row.get("Acc Number"),
                "ifsc_code": row.get("IFSC Code"),
                "account_holder_address":
                    row.get("Acc Holder Address"),
            }

        record["source_file"] = os.path.basename(csv_path)
        records.append(record)

    return records