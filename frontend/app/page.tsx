// "use client";

// import { useState } from "react";

// export default function Home() {
//   const [files, setFiles] = useState<FileList | null>(null);

//   const handleUpload = async () => {
//     if (!files) return;

//     const formData = new FormData();

//     Array.from(files).forEach((file) => {
//       formData.append("files", file);
//     });

//     const response = await fetch(
//       "http://localhost:8000/upload",
//       {
//         method: "POST",
//         body: formData,
//       }
//     );

//     const data = await response.json();

//     console.log(data);
//     alert(JSON.stringify(data, null, 2));
//   };

//   return (
//     <main className="p-10">
//       <h1 className="text-3xl font-bold mb-6">
//         HR Document Extraction
//       </h1>

//       <input
//         type="file"
//         multiple
//         onChange={(e) => setFiles(e.target.files)}
//       />

//       <button
//         onClick={handleUpload}
//         className="mt-4 block border px-4 py-2 rounded"
//       >
//         Upload
//       </button>
//     </main>
//   );
// }
"use client";

import { useState } from "react";
import UploadCard from "./UploadCard";
import CandidateTable from "./Candidatetable";

export default function Home() {
  const [loading, setLoading] =
  useState(false);

  const [candidates, setCandidates] =
    useState<any[]>([]);

  const [csvData, setCsvData] =
    useState<any[]>([]);

  return (
    <main className="min-h-screen bg-[#050810] text-gray-300">
      <div className="max-w-8xl mx-auto p-8 space-y-8">

        {/* Header */}
        <div>
          <h1 className="text-4xl font-bold text-white">
            HR Document Extraction
          </h1>

          <p className="text-gray-500 mt-2">
            Upload candidate PDFs and
            automatically extract and merge
            employee information.
          </p>
        </div>

        {/* Upload Section */}
        <div className="bg-[#111827] border border-gray-800 rounded-xl shadow-xl">
          <UploadCard
            loading={loading}
            setLoading={setLoading}
            setCandidates={setCandidates}
            setCsvData={setCsvData}
          />
        </div>
        <div className="flex justify-end mb-4">

  <button
    onClick={() => {
      if (csvData.length === 0)
        return;

      const headers =
        Object.keys(csvData[0]);

      const rows =
        csvData.map((row) =>
          headers
        .map((h) => {
          const value = row[h] ?? "";

          if (
            h === "aadhar_number" ||
            h === "account_number" ||
            h === "phone_number" || 
            h === "date_of_joining" ||
            h === "ifsc_code"
          ) {
             return `="${value}"`;
          }

          return `"${value}"`;
        })
        .join(",")
        );

      const csv =
        [
          headers.join(","),
          ...rows,
        ].join("\n");

      const blob =
        new Blob(
          [csv],
          {
            type:
              "text/csv",
          }
        );

      const url =
        window.URL.createObjectURL(
          blob
        );

      const a =
        document.createElement(
          "a"
        );

      a.href = url;
      a.download =
        "candidates.csv";

      a.click();
      a.remove();

      window.URL.revokeObjectURL(
        url
      );
    }}
    className="px-4 py-2 rounded-lg bg-blue-600 text-white hover:bg-blue-700"
  >
    Download CSV
  </button>

</div>

        {/* Results */}
        <div className="bg-[#111827] border border-gray-800 rounded-xl shadow-xl overflow-hidden">
          <div className="px-6 py-5 border-b border-gray-800">
            <h2 className="text-xl font-semibold text-white">
              Extraction Results
            </h2>

            <p className="text-sm text-gray-500 mt-1">
              Candidate information extracted
              from uploaded documents.
            </p>
          </div>

          <CandidateTable
            candidates={candidates}
            csvData={csvData}
          />
        </div>

      </div>
    </main>
  );
}