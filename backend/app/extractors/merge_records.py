# def merge_by_candidate(records):
#     temp = {}

#     # Priority: higher wins when choosing conflicting fields
#     DOC_PRIORITY = {
#     "resume": 5,
#     "text": 4,
#     "personal": 3,
#     "bank": 2,
#     "aadhar": 1,
# }

#     def prio(rec):
#         return DOC_PRIORITY.get(rec.get("doc_type"), 1)

#     for record in records:
#         email = record.get("email")
#         if not email:
#             continue

#         if email not in temp:
#             temp[email] = {
#                 "_prio_full_name": -1,
#                 "_prio_role": -1,
#                 "_prio_location": -1,
#                 "_prio_doj": -1,
#             }

#         for k, v in record.items():
#             if v is None or v == "":
#                 continue

#             # Prefer numeric candidate_id (from a real Candidate ID), otherwise keep existing
#             if k == "candidate_id":
#                 curr = str(temp[email].get("candidate_id", ""))
#                 nv = str(v)
#                 if nv.isdigit():
#                     temp[email]["candidate_id"] = nv
#                 elif "candidate_id" not in temp[email]:
#                     temp[email]["candidate_id"] = nv
#                 continue

#             # Always overwrite these with the latest extracted value
#             if k in ["bank_name", "account_number", "aadhar_number", "t_shirt_size", "reporting_manager"]:
#                 temp[email][k] = v
#                 continue

#             # Full name: choose best source (resume/text > aadhar/form)
#             if k == "full_name":
#                 p = prio(record)
#                 if p >= temp[email]["_prio_full_name"]:
#                     temp[email]["full_name"] = v
#                     temp[email]["_prio_full_name"] = p
#                 continue

#             # Role/location/doj also should not be polluted by “... Location/Email”
#             if k in ["role", "location", "date_of_joining"]:
#                 p = prio(record)
#                 key_prio = "_prio_" + ("doj" if k == "date_of_joining" else k)
#                 if p >= temp[email][key_prio]:
#                     temp[email][k] = v
#                     temp[email][key_prio] = p
#                 continue
#             if k in [
#                 "bank_name",
#                 "account_number",
#                 "ifsc_code",
#                 "account_holder_address",
#                 "t_shirt_size",
#                 "age",
#                 "address",
#                 "phone_number",
#                 "aadhar_number",
#                 "reporting_manager"
#                 ]:
#                 temp[email][k] = v
#                 continue

#             # Default: fill only if empty
#             if k not in temp[email] or temp[email][k] in ("", None):
#                 temp[email][k] = v

#     # cleanup
#     out = []
#     for r in temp.values():
#         r.pop("_prio_full_name", None)
#         r.pop("_prio_role", None)
#         r.pop("_prio_location", None)
#         r.pop("_prio_doj", None)
#         out.append(r)

#     return out

def merge_by_candidate(records):
    candidates = {}

    email_map = {}
    phone_map = {}
    aadhaar_map = {}
    pan_map = {}
    name_dob_map = {}

    next_candidate_id = 1

    # -------------------------
    # Document Priority
    # -------------------------
    DOC_PRIORITY = {
        "resume": 5,
        "text": 4,
        "personal_csv": 3,
        "bank_csv": 3,
        "aadhaar": 2,
        "pan": 2,
    }

    def prio(record):
        return DOC_PRIORITY.get(
            record.get("doc_type"),
            1
        )

    # -------------------------
    # Helpers
    # -------------------------
    def norm(value):
        if not value:
            return None

        return " ".join(
            str(value).upper().split()
        )

    def get_name_dob_key(record):
        name = norm(
            record.get("full_name")
        )

        dob = (
            record.get("date_of_birth")
            or record.get("dob")
        )

        if name and dob:
            return f"{name}|{dob}"

        return None

    # -------------------------
    # Candidate Lookup
    # -------------------------
    def find_candidate(record):
        aadhaar = record.get("aadhaar_number")
        if aadhaar:
            cid = aadhaar_map.get(aadhaar)
            if cid:
                return cid

        pan = record.get("pan_number")
        if pan:
            cid = pan_map.get(pan)
            if cid:
                return cid

        email = record.get("email")
        if email:
            cid = email_map.get(email)
            if cid:
                return cid

        phone = record.get("phone_number")
        if phone:
            cid = phone_map.get(phone)
            if cid:
                return cid

        key = get_name_dob_key(record)
        if key:
            cid = name_dob_map.get(key)
            if cid:
                return cid

        return None

    # -------------------------
    # Merge Fields
    # -------------------------
    def merge_fields(candidate, record):
        for k, v in record.items():
            if v is None or v == "":
                continue

            # Full name
            if k == "full_name":
                p = prio(record)

                if (
                    "_prio_full_name"
                    not in candidate
                ):
                    candidate["_prio_full_name"] = -1

                if (
                    p >=
                    candidate["_prio_full_name"]
                ):
                    candidate[k] = norm(v)
                    candidate["_prio_full_name"] = p

                continue

            # Role
            if k == "role":
                p = prio(record)

                if (
                    "_prio_role"
                    not in candidate
                ):
                    candidate["_prio_role"] = -1

                if (
                    p >=
                    candidate["_prio_role"]
                ):
                    candidate[k] = v
                    candidate["_prio_role"] = p

                continue

            # Location
            if k == "location":
                p = prio(record)

                if (
                    "_prio_location"
                    not in candidate
                ):
                    candidate["_prio_location"] = -1

                if (
                    p >=
                    candidate["_prio_location"]
                ):
                    candidate[k] = v
                    candidate["_prio_location"] = p

                continue

            # Date of Joining
            if k == "date_of_joining":
                p = prio(record)

                if (
                    "_prio_doj"
                    not in candidate
                ):
                    candidate["_prio_doj"] = -1

                if (
                    p >=
                    candidate["_prio_doj"]
                ):
                    candidate[k] = v
                    candidate["_prio_doj"] = p

                continue

            # Always overwrite
            if k in [
                "bank_name",
                "account_number",
                "ifsc_code",
                "account_holder_address",
                "t_shirt_size",
                "age",
                "address",
                "phone_number",
                "aadhaar_number",
                "pan_number",
                "reporting_manager",
                "salary",
                "company_name",
                "education",
                "cgpa",
                "experience_years",
                "contract_end_date",
                "date_of_birth",
            ]:
                candidate[k] = v
                continue

            # Fill if empty
            if (
                k not in candidate
                or candidate[k] in (
                    "",
                    None,
                )
            ):
                candidate[k] = v

    # -------------------------
    # Update Indexes
    # -------------------------
    def update_indexes(candidate, cid):
        email = candidate.get("email")
        if email:
            email_map[email] = cid

        phone = candidate.get("phone_number")
        if phone:
            phone_map[phone] = cid

        aadhaar = candidate.get(
            "aadhaar_number"
        )
        if aadhaar:
            aadhaar_map[aadhaar] = cid

        pan = candidate.get(
            "pan_number"
        )
        if pan:
            pan_map[pan] = cid

        key = get_name_dob_key(
            candidate
        )
        if key:
            name_dob_map[key] = cid

    # -------------------------
    # Main Processing
    # -------------------------
    for record in records:
        cid = find_candidate(record)

        if cid is None:
            cid = next_candidate_id

            candidates[cid] = {
                "candidate_id": cid
            }

            next_candidate_id += 1

        candidate = candidates[cid]

        merge_fields(
            candidate,
            record
        )

        update_indexes(
            candidate,
            cid
        )

    # -------------------------
    # Cleanup
    # -------------------------
    result = []

    for candidate in candidates.values():
        candidate.pop(
            "_prio_full_name",
            None
        )
        candidate.pop(
            "_prio_role",
            None
        )
        candidate.pop(
            "_prio_location",
            None
        )
        candidate.pop(
            "_prio_doj",
            None
        )

        result.append(candidate)

    return result
