# import re
# from pypdf import PdfReader

# def extract_text_from_pdf(pdf_path):
#     reader = PdfReader(pdf_path)
#     text = ""

#     for page in reader.pages:
#         extracted = page.extract_text()
#         if extracted:
#             text += extracted + "\n"

#     return text


# def extract_text_based_fields(pdf_path):
#     text = extract_text_from_pdf(pdf_path)
#     #print(text)

#     data = {"doc_type": "text"}

#     clean_text = re.sub(r"\s+"," ", text).strip()
#     #print(clean_text)

#     # -------------------------
#     # Common Fields
#     # -------------------------

#     email = re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",text)

#     if email:
#         data["email"] = email.group(0)
#         data["candidate_id"] = email.group(0)

#     cid = re.search(r"Candidate ID[:\s]*(\d+)", text, re.IGNORECASE)

#     if cid:
#         data["candidate_id"] = cid.group(1)

#     name = re.search(r"(?:Name|To|Candidate Name)[:\s]+([A-Z][a-z]+(?:\s[A-Z][a-z]+)+)",text)

#     if name:
#         data["full_name"] = name.group(1).strip()

#     phone = re.search(r"(?:Phone|Mobile)[:\s]*([6-9]\d{9})",text)

#     if phone:
#         data["phone_number"] = phone.group(1)

#     mgr = re.search(
#         r"(?:Reporting Manager|Reporting To|reporting to)[:\s]+([A-Za-z\s]+?)(?:\.|,|\n)",text,re.IGNORECASE)

#     if mgr:
#         data["reporting_manager"] = ( mgr.group(1).strip().rstrip("."))

#     # -------------------------
#     # aadhaar
#     # -------------------------

#     if "aadhaar" in clean_text.lower():


#         data["doc_type"] = "aadhaar"

#         uid = re.search(
#         r"(?:Number|No)[:\s]*((?:\d{4}[\s-]?){2}\d{4})",
#         text,
#         re.IGNORECASE
#         )

#         if uid:
#             raw = (
#                 uid.group(1)
#                 .replace(" ", "")
#                 .replace("\n", "")
#             )

#             if len(raw) >= 12:
#                 data["aadhaar_number"] = raw

#         age = re.search(
#             r"Age[:\s]*(\d{2})",
#             text,
#             re.IGNORECASE
#         )

#         if age:
#             data["age"] = age.group(1)

#     # for real aadhar 

#     # if "aadhaar" in text.lower():

#     #     data["doc_type"] = "aadhaar"

#     #     # -------------------------
#     #     # NAME (line before C/O)
#     #     # -------------------------
#     #     name_match = re.search(
#     #         r"([A-Z][A-Z\s]+)\s+C/O",
#     #         text
#     #     )

#     #     if name_match:
#     #         data["full_name"] = (
#     #             name_match.group(1)
#     #             .strip()
#     #         )

#     #     # -------------------------
#     #     # AADHAAR NUMBER (flexible formats)
#     #     # -------------------------
#     #     uid = re.search(
#     #         r"\b(?:\d{4}[\s-]?){3}\b|\b(?:XXXX[\s-]?){2}\d{4}\b",
#     #         text
#     #     )

#     #     if uid:
#     #         raw = uid.group(0)
#     #         raw = raw.replace(" ", "").replace("-", "").strip()

#     #         # optional safety check
#     #         if len(raw) == 12:
#     #             data["aadhaar_number"] = raw

#     #     # -------------------------
#     #     # DOB
#     #     # -------------------------
#     #     dob = re.search(
#     #         r"DOB[:\s]*([0-9]{2}[-/][0-9]{2}[-/][0-9]{4})",
#     #         text,
#     #         re.IGNORECASE
#     #     )

#     #     if dob:
#     #         data["date_of_birth"] = dob.group(1)

#     # -------------------------
#     # RESUME
#     # -------------------------

#     elif (
#         "experience" in clean_text.lower()
#         and
#         "education" in clean_text.lower()
#     ):
#         print("resume")

#         data["doc_type"] = "resume"

#         exp = re.search(
#             r"(\d+)\s+years",
#             text,
#             re.IGNORECASE
#         )

#         if exp:
#             data["experience_years"] = exp.group(1)

#         cgpa = re.search(
#             r"CGPA[:\s]*([\d\.]+)",
#             text,
#             re.IGNORECASE
#         )

#         if cgpa:
#             data["cgpa"] = cgpa.group(1)

#         for degree in [
#             "B.Tech",
#             "M.Tech",
#             "MBA",
#             "B.Com",
#             "B.Des",
#             "BCA",
#             "MCA"
#         ]:
#             if degree in text:
#                 data["education"] = degree
#                 break

#         role = re.search(
#             r"Current Role[:\s-]*([A-Za-z\s]+)",
#             text,
#             re.IGNORECASE
#         )

#         if role:
#             data["role"] = (
#                 role.group(1).strip()
#             )

#     # -------------------------
#     # OFFER LETTERS /
#     # APPOINTMENT LETTERS
#     # -------------------------

#     else:
#         print("offer")
#         name = re.search(
#         r"\d{2}/\d{2}/\d{4}\s+([A-Za-z]+(?:\s[A-Za-z]+)+)\s+\d{12}",
#         text
#         )

#         if name:
#             data["full_name"] = name.group(1).strip()

#         # Role
#         role_patterns = [
#             r"position of\s+(.+?)\s+(?:based|at|starting)",
#             r"role of\s+(.+?)\s+(?:based|at|starting)",
#             r"designation[:\s-]*(.+)",
#             r"position[:\s-]*(.+)",
#             r"job title[:\s-]*(.+)"
#         ]

#         for pattern in role_patterns:

#             match = re.search(
#                 pattern,
#                 clean_text,
#                 re.IGNORECASE
#             )

#             if match:
#                 data["role"] = (
#                     match.group(1)
#                     .strip()
#                 )
#                 break

#         # Date of Joining
#         doj_patterns = [
#             r"Joining Date[:\s-]*(\d{4}-\d{2}-\d{2})",
#             r"DOJ[:\s-]*(\d{4}-\d{2}-\d{2})",
#             r"starting[:\s-]*(\d{4}-\d{2}-\d{2})",
#             r"Date of Joining[:\s-]*(\d{2}/\d{2}/\d{4})",
#             r"Joining Date[:\s-]*(\d{2}/\d{2}/\d{4})",
#             r"Start Date[:\s-]*(\d{2}/\d{2}/\d{4})",
#             r"(\d{2}/\d{2}/\d{4})\s+to\s+(\d{2}/\d{2}/\d{4})"
#         ]

#         for pattern in doj_patterns:

#             match = re.search(
#                 pattern,
#                 text,
#                 re.IGNORECASE
#             )

#             if match:
#                 data["date_of_joining"] = (
#                     match.group(1)
#                 )
#                 break

#         doj_range = re.search(
#             r"(\d{2}/\d{2}/\d{4})\s+to\s+(\d{2}/\d{2}/\d{4})",
#             text,
#             re.IGNORECASE
#         )

#         if doj_range and "date_of_joining" not in data:
#             data["date_of_joining"] = doj_range.group(1)
#             data["contract_end_date"] = doj_range.group(2)
#         salary = re.search(
#             r"(INR|USD|\$|₹|EUR|GBP)\s*([\d,]+(?:\.\d+)?)",
#             text,
#             re.IGNORECASE
#         )

#         if salary:
#             data["salary"] = salary.group(2).replace(",", "")

#         company_patterns = [
#             r"Welcome to\s+([A-Za-z0-9\s&.,]+)",
#             r"employed by\s+([A-Za-z0-9\s&.,]+)",
#             r"Company[:\s-]*([A-Za-z0-9\s&.,]+)",
#             r"This offer is made by\s+([A-Za-z0-9\s&.,]+)"
#         ]

#         for pattern in company_patterns:

#             match = re.search(
#                 pattern,
#                 clean_text,
#                 re.IGNORECASE
#             )

#             if match:
#                 data["company_name"] = (
#                     match.group(1)
#                     .strip()
#                 )
#                 break
#         company = re.search(
#             r"([A-Z][A-Za-z0-9\s&.,()\-]+?)\s+CONFIDENTIAL",
#             text
#         )

#         if company:
#             data["company_name"] = company.group(1).strip()
#         # Work Location
#         location_patterns = [
#         r"Location[:\s-]*([A-Za-z]+)\b",
#         r"based in\s+([A-Za-z]+)\b",
#         r"work location[:\s-]*([A-Za-z]+)\b",
#         r"office location[:\s-]*([A-Za-z]+)\b",
#         r"site[:\s-]*([A-Za-z]+)\b",
#         r"work base will be\s+(.+?)(?:\(|--)"
#         ]

#         for pattern in location_patterns:

#             match = re.search(
#                 pattern,
#                 clean_text,
#                 re.IGNORECASE
#             )

#             if match:
#                 data["location"] = (match.group(1).strip())
#                 break
#     print(data)
#     return data

import re
from pypdf import PdfReader


def extract_text_from_pdf(pdf_path):
    reader = PdfReader(pdf_path)
    text = ""

    for page in reader.pages:
        extracted = page.extract_text()
        if extracted:
            text += extracted + "\n"

    return text


def extract_text_based_fields(pdf_path):
    text = extract_text_from_pdf(pdf_path)

    data = {"doc_type": "text"}

    clean_text = re.sub(r"\s+", " ", text).strip()

    # -------------------------
    # Common Fields
    # -------------------------

    email = re.search(
        r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
        text
    )

    if email:
        data["email"] = email.group(0)
        data["candidate_id"] = email.group(0)

    cid = re.search(
        r"Candidate ID[:\s]*(\d+)",
        text,
        re.IGNORECASE
    )

    if cid:
        data["candidate_id"] = cid.group(1)

    name = re.search(
        r"(?:Name|To|Candidate Name)[:\s]+([A-Z][a-z]+(?:\s[A-Z][a-z]+)+)",
        text
    )

    if name:
        data["full_name"] = name.group(1).strip()

    phone = re.search(
        r"(?:Phone|Mobile)[:\s]*([6-9]\d{9})",
        text
    )

    if phone:
        data["phone_number"] = phone.group(1)

    mgr = re.search(
        r"(?:Reporting Manager|Reporting To|reporting to)[:\s]+([A-Za-z\s]+?)(?:\.|,|\n)",
        text,
        re.IGNORECASE
    )

    if mgr:
        data["reporting_manager"] = (
            mgr.group(1)
            .strip()
            .rstrip(".")
        )

    # -------------------------
    # AADHAAR
    # -------------------------

    if "aadhaar" in clean_text.lower():

        data["doc_type"] = "aadhaar"

        # -------------------------
        # Aadhaar Number
        # Supports:
        # 1234 1234 1234
        # 123412341234
        # XXXX XXXX 1234
        # XXXXXXXX1234
        # -------------------------
        uid = re.search(
            r"\b(?:\d{4}[\s-]?){2}\d{4}\b"
            r"|\b(?:X{4}[\s-]?){2}\d{4}\b"
            r"|\bX{8}\d{4}\b",
            text,
            re.IGNORECASE
        )

        if uid:
            raw = (
                uid.group(0)
                .replace(" ", "")
                .replace("-", "")
            )

            data["aadhaar_number"] = raw

        # -------------------------
        # Date of Birth
        # Supports:
        # DOB: 26-06-2004
        # DOB : 26/06/2004
        # Date of Birth: 26-06-2004
        # -------------------------
        dob = re.search(
            r"(?:DOB|Date of Birth)[:\s]*"
            r"(\d{2}[/-]\d{2}[/-]\d{4})",
            text,
            re.IGNORECASE
        )

        if dob:
            date = dob.group(1).replace("/", "-")
            data["date_of_birth"] = date

        # -------------------------
        # Age
        # -------------------------
        age = re.search(
            r"Age[:\s]*(\d{1,3})",
            text,
            re.IGNORECASE
        )

        if age:
            data["age"] = age.group(1)

        # -------------------------
        # Name
        # Between:
        # To
        # <NAME>
        # C/O
        # -------------------------
        name = re.search(
            r"To\s+([A-Za-z]+(?:\s+[A-Za-z]+)+)\s+C/?O",
            text,
            re.IGNORECASE
        )

        if name:
            data["full_name"] = (
                " ".join(
                    name.group(1).upper().split()
                )
            )

    # -------------------------
    # PAN CARD
    # -------------------------

    # -------------------------
# PAN CARD
# -------------------------
    elif (
        "permanent account number card" in clean_text.lower()
        or
        re.search(r"\bPAN\b", text, re.IGNORECASE)
    ):

        data["doc_type"] = "pan"

        # -------------------------
        # Name
        # NAME <NAME> DATE OF BIRTH
        # NAME <NAME> Father's Name
        # -------------------------
        name = re.search(
            r"NAME\s+([A-Za-z\s]+?)\s+"
            r"(?:DATE\s+OF\s+BIRTH|FATHER'?S\s+NAME)",
            clean_text,
            re.IGNORECASE
        )

        if name:
            data["full_name"] = (
                " ".join(
                    name.group(1)
                    .upper()
                    .split()
                )
            )
        # -------------------------
        # Date of Birth
        # Supports:
        # Date of Birth 26-06-2004
        # Date of Birth: 26/06/2004
        # Date of Birth : 26 – 06 - 2004
        # -------------------------
        dob = re.search(
            r"DATE\s+OF\s+BIRTH\s*:?\s*"
            r"(\d{2}\s*[-–—/]\s*\d{2}\s*[-–—/]\s*\d{4})",
            clean_text,
            re.IGNORECASE
        )

        if dob:
            data["date_of_birth"] = re.sub(
                r"\s*[-–—/]\s*",
                "-",
                dob.group(1)
            )

        # -------------------------
        # PAN Number
        # Supports:
        # ABCDE1234F
        # abcde1234f
        # -------------------------
        pan = re.search(
            r"\b[A-Z]{5}[0-9]{4}[A-Z]\b",
            text,
            re.IGNORECASE
        )

        if pan:
            data["pan_number"] = (
                pan.group(0)
                .upper()
            )
    # -------------------------
    # RESUME
    # -------------------------

    elif re.search(
        r"(experience|work experience|professional experience)",
        clean_text,
        re.IGNORECASE
    ) and re.search(
        r"(education|academics|qualification|qualifications)",
        clean_text,
        re.IGNORECASE
    ):
        data["doc_type"] = "resume"

# Experience
        exp = re.search(
            r"(\d+(?:\.\d+)?)\s*(?:\+?\s*)?(?:years?|yrs?)",
            text,
            re.IGNORECASE
        )

        if exp:
            data["experience_years"] = exp.group(1)

        # CGPA
        cgpa = re.search(
            r"CGPA\s*[:\-]?\s*([\d.]+)",
            text,
            re.IGNORECASE
        )

        if cgpa:
            data["cgpa"] = cgpa.group(1)

        # Education
        for degree in [
            "B.Tech",
            "B.E.",
            "BE",
            "M.Tech",
            "MBA",
            "B.Com",
            "B.Des",
            "BCA",
            "MCA",
            "B.Sc",
            "M.Sc",
            "MS",
            "BS"
        ]:
            if re.search(
                re.escape(degree),
                text,
                re.IGNORECASE
            ):
                data["education"] = degree
                break

        

    # -------------------------
    # ACCEPTANCE LETTER
    # -------------------------
    elif (
        "formally" in clean_text.lower()
        and "reporting manager" in clean_text.lower()
    ):

        data["doc_type"] = "acceptance"

        # Name:
        # "I, Pratham Shetty, formally ..."
        name = re.search(
            r"\bI\s*,\s*([A-Za-z]+(?:\s+[A-Za-z]+)+)\s*,?\s*formally",
            text,
            re.IGNORECASE
        )

        if name:
            data["full_name"] = name.group(1).strip()

        # Email (common extractor already handles this,
        # but keep as fallback)
        if "email" not in data:
            email = re.search(
                r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
                text,
                re.IGNORECASE
            )

            if email:
                data["email"] = email.group(0)

        # Reporting Manager:
        # "Reporting Manager: Rajesh Kumar"
        mgr = re.search(
            r"Reporting\s+Manager\s*[:\-]?\s*([A-Za-z]+(?:\s+[A-Za-z]+)*)",
            text,
            re.IGNORECASE
        )

        if mgr:
            data["reporting_manager"] = (
                mgr.group(1).strip()
            )
        
    # -------------------------
# OFFER / APPOINTMENT LETTERS
# -------------------------

    else:

        print("offer")

        # -------------------------
        # Name between date and Aadhaar
        # -------------------------
        name = re.search(
            r"\d{2}[/-]\d{2}[/-]\d{4}\s+([A-Za-z]+(?:\s+[A-Za-z]+)+)\s+\d{12}",
            clean_text
        )

        if name:
            data["full_name"] = name.group(1).strip()

        # -------------------------
        # Aadhaar (12 digits)
        # -------------------------
        uid = re.search(
            r"\b\d{12}\b",
            text
        )

        if uid:
            data["aadhaar_number"] = uid.group(0)

        # -------------------------
        # DOJ = date not followed by name
        # and not preceded by "to"
        # -------------------------
        dates = re.finditer(
            r"\b\d{2}[/-]\d{2}[/-]\d{4}\b",
            clean_text
        )

        for m in dates:
            start = m.start()
            end = m.end()

            before = clean_text[max(0, start - 10):start].lower()
            after = clean_text[end:end + 40]

            if (
                "to" not in before
                and
                not re.match(
                    r"\s+[A-Za-z]+(?:\s+[A-Za-z]+)+",
                    after
                )
            ):
                data["date_of_joining"] = m.group(0)
                break

        # -------------------------
        # Role
        # placement as an X at
        # -------------------------
        role = re.search(
            r"placement as an?\s+(.+?)\s+at\b",
            clean_text,
            re.IGNORECASE
        )

        if role:
            data["role"] = role.group(1).strip()

        # -------------------------
        # Company
        # role at COMPANY (the "Company")
        # -------------------------
        if "role" in data:

            company = re.search(
            r"We\s+are\s+pleased\s+to\s+offer\s+you\s+.+?\s+at\s+(.+?)\s+\(the\s+[\"'“”]?Company[\"'“”]?\)",
            clean_text,
            re.IGNORECASE
        )

        if company:
            data["company_name"] = company.group(1).strip()

        # -------------------------
        # Work Base / Site
        # -------------------------
        site = re.search(
            r"work base will be\s+(.+?)(?:\.|\(|--|$)",
            clean_text,
            re.IGNORECASE
        )

        if site:
            data["location"] = site.group(1).strip()

        # -------------------------
        # Fallback Role
        # -------------------------
        if "role" not in data:

            role_patterns = [
                r"position of\s+(.+?)\s+(?:based|at|starting)",
                r"role of\s+(.+?)\s+(?:based|at|starting)",
                r"designation[:\s-]*(.+)",
                r"position[:\s-]*(.+)",
                r"job title[:\s-]*(.+)"
            ]

            for pattern in role_patterns:

                match = re.search(
                    pattern,
                    clean_text,
                    re.IGNORECASE
                )

                if match:
                    data["role"] = (
                        match.group(1)
                        .strip()
                    )
                    break

        # -------------------------
        # Fallback DOJ
        # -------------------------
        if "date_of_joining" not in data:

            doj_patterns = [
                r"Joining Date[:\s-]*(\d{4}-\d{2}-\d{2})",
                r"DOJ[:\s-]*(\d{4}-\d{2}-\d{2})",
                r"starting[:\s-]*(\d{4}-\d{2}-\d{2})",
                r"Date of Joining[:\s-]*(\d{2}/\d{2}/\d{4})",
                r"Joining Date[:\s-]*(\d{2}/\d{2}/\d{4})",
                r"Start Date[:\s-]*(\d{2}/\d{2}/\d{4})",
                r"(\d{2}/\d{2}/\d{4})\s+to\s+(\d{2}/\d{2}/\d{4})"
            ]

            for pattern in doj_patterns:

                match = re.search(
                    pattern,
                    text,
                    re.IGNORECASE
                )

                if match:
                    data["date_of_joining"] = match.group(1)
                    break

            doj_range = re.search(
                r"(\d{2}/\d{2}/\d{4})\s+to\s+(\d{2}/\d{2}/\d{4})",
                text,
                re.IGNORECASE
            )

            if doj_range and "date_of_joining" not in data:
                data["date_of_joining"] = doj_range.group(1)

        # -------------------------
        # Salary
        # -------------------------
        salary = re.search(
            r"(?:INR|USD|EUR|GBP|\$|₹)\s*([\d,]+(?:\.\d+)?)",
            text,
            re.IGNORECASE
        )

        if salary:
            data["salary"] = (
                salary.group(1)
                .replace(",", "")
            )

        # -------------------------
        # Fallback Company
        # -------------------------
        if "company_name" not in data:

            company_patterns = [
                r"Welcome to\s+([A-Za-z0-9\s&.,]+)",
                r"employed by\s+([A-Za-z0-9\s&.,]+)",
                r"Company[:\s-]*([A-Za-z0-9\s&.,]+)",
                r"This offer is made by\s+([A-Za-z0-9\s&.,]+)"
            ]

            for pattern in company_patterns:

                match = re.search(
                    pattern,
                    clean_text,
                    re.IGNORECASE
                )

                if match:
                    data["company_name"] = (
                        match.group(1)
                        .strip()
                    )
                    break

            company = re.search(
                r"([A-Z][A-Za-z0-9\s&.,()\-]+?)\s+CONFIDENTIAL",
                text
            )

            if company:
                data["company_name"] = (
                    company.group(1)
                    .strip()
                )

        # -------------------------
        # Fallback Location
        # -------------------------
        if "location" not in data:

            location_patterns = [
                r"Location[:\s-]*([A-Za-z]+)\b",
                r"based in\s+([A-Za-z]+)\b",
                r"work location[:\s-]*([A-Za-z]+)\b",
                r"office location[:\s-]*([A-Za-z]+)\b",
                r"site[:\s-]*([A-Za-z]+)\b",
                r"work base will be\s+(.+?)(?:\(|--)"
            ]

            for pattern in location_patterns:

                match = re.search(
                    pattern,
                    clean_text,
                    re.IGNORECASE
                )

                if match:
                    data["location"] = (
                        match.group(1)
                        .strip()
                    )
                    break

        # -------------------------
        # Fallback Aadhaar
        # -------------------------
        if "aadhaar_number" not in data:

            uid = re.search(
                r"\b(?:\d{4}[\s-]?){3}\b|\b(?:XXXX[\s-]?){2}\d{4}\b",
                text
            )

            if uid:
                data["aadhaar_number"] = (
                    uid.group(0)
                    .replace(" ", "")
                    .replace("-", "")
                )
    # -------------------------
    # Normalize Name
    # -------------------------

    if data.get("full_name"):
        data["full_name"] = (
            " ".join(
                data["full_name"]
                .upper()
                .split()
            )
        )

    print(data)

    return data