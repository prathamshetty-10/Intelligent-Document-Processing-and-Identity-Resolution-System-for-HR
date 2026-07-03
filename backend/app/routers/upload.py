# from fastapi import (
#     APIRouter,
#     UploadFile,
#     File
# )

# from typing import List
# import tempfile
# import shutil
# import os

# from app.extractors.extract_text import (
#     extract_text_based_fields
# )
# from app.extractors.merge_records import (
#     merge_by_candidate
# )
# from app.extractors.extract_csv import (
#     extract_csv_records
# )

# router = APIRouter(
#     prefix="/upload",
#     tags=["Upload"]
# )


# @router.post("/")
# async def process_pdfs(
#     files: List[UploadFile] = File(...)
# ):
#     records = []

#     with tempfile.TemporaryDirectory() as temp_dir:

#         for file in files:
#             try:
#                 temp_path = os.path.join(temp_dir, file.filename)
#                 #Take the uploaded file stream, save it temporarily on disk, let the extractors read it, and automatically delete it afterward.
#                 with open(temp_path, "wb") as buffer:
#                     shutil.copyfileobj(file.file, buffer)

#                 extension = os.path.splitext(file.filename)[1].lower()
            
#                 if extension == ".csv":
#                     csv_records = (extract_csv_records(temp_path))
#                     records.extend(csv_records)
#                     continue

#                 elif extension == ".pdf":
#                     print("pdf")
#                     rec = extract_text_based_fields(temp_path)
#                     rec["source_file"] = (file.filename)
#                     records.append(rec)
#                 else:
#                     print("none")
#                     continue

#             except Exception as e:
#                 print(f"Skipping "f"{file.filename}: {e}")

#     if records:
#         merged = merge_by_candidate(records)

#         def sort_key(record):
#             cid = str(record.get("candidate_id",""))

#             return (
#                 (0, int(cid))
#                 if cid.isdigit()
#                 else (1, cid)
#             )

#         merged = sorted(merged, key=sort_key)

#         return {
#             "status": "success",
#             "data": merged
#         }

#     return {
#         "status": "error",
#         "message": "No data found"
#     }

from fastapi import (
    APIRouter,
    UploadFile,
    File
)

from typing import List
import tempfile
import shutil
import os

from app.extractors.extract_text import (
    extract_text_based_fields
)
from app.extractors.merge_records import (
    merge_by_candidate
)
from app.extractors.extract_csv import (
    extract_csv_records
)

router = APIRouter(
    prefix="/upload",
    tags=["Upload"]
)


@router.post("/")
async def process_pdfs(
    files: List[UploadFile] = File(...)
):
    records = []

    with tempfile.TemporaryDirectory() as temp_dir:
        files = sorted(
        files,
        key=lambda f: (
            0 if f.filename.lower().endswith(".csv")
            else 1 if ("aadhaar" in f.filename.lower() or "aadhar" in f.filename.lower())
            else 2 if "pan" in f.filename.lower()
            else 3
        )
    )
        for file in files:
            try:
                temp_path = os.path.join(temp_dir, file.filename)
                #Take the uploaded file stream, save it temporarily on disk, let the extractors read it, and automatically delete it afterward.
                with open(temp_path, "wb") as buffer:
                    shutil.copyfileobj(file.file, buffer)

                extension = os.path.splitext(file.filename)[1].lower()
            
                if extension == ".csv":
                    csv_records = (extract_csv_records(temp_path))
                    records.extend(csv_records)
                    continue

                elif extension == ".pdf":
                    print("pdf")
                    rec = extract_text_based_fields(temp_path)
                    rec["source_file"] = (file.filename)
                    records.append(rec)
                else:
                    print("none")
                    continue

            except Exception as e:
                print(f"Skipping "f"{file.filename}: {e}")

    if records:
        merged = merge_by_candidate(records)

        merged = sorted(merged, key=lambda r: r["candidate_id"])

        return {
            "status": "success",
            "data": merged
        }

    return {
        "status": "error",
        "message": "No data found"
    }