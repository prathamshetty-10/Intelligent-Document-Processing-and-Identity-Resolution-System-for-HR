"use client";

import {
  Dispatch,
  SetStateAction,
  useState,
} from "react";
import {
  Upload,
  FileText,
} from "lucide-react";

type Props = {
  loading: boolean;
  setLoading: Dispatch<
    SetStateAction<boolean>
  >;
  setCandidates: Dispatch<
    SetStateAction<any[]>
  >;
  setCsvData: Dispatch<
    SetStateAction<any[]>
  >;
};
export default function UploadCard({
  loading,
  setLoading,
  setCandidates,
  setCsvData,
}: Props) {
  const [files, setFiles] =
    useState<File[]>([]);

  const handleUpload = async () => {
    if (files.length === 0) {
      return;
    }

    setLoading(true);

    try {
      const formData =
        new FormData();

      files.forEach((file) => {
        formData.append(
          "files",
          file
        );
      });

      const response =
        await fetch(
          "http://localhost:8000/upload/",
          {
            method: "POST",
            body: formData,
          }
        );

      const result =
        await response.json();

      if (
        result.status === "success"
      ) {
        setCandidates(result.data);
        setCsvData(result.data);
      } else {
        alert(
          result.message ||
            "Processing failed"
        );
      }
    } catch (err) {
      console.error(err);
      alert("Upload failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-8">

      <h2 className="text-xl font-semibold text-white">
        Upload Documents
      </h2>

      <p className="text-sm text-gray-500 mt-1">
        Select Offer Letters,
Resumes, Aadhar PDFs and
Candidate Form Files
      </p>

      <div className="mt-6 border-2 border-dashed border-gray-700 rounded-xl p-10 bg-[#0b0f1a]">

        <div className="flex flex-col items-center">

          <div className="p-4 rounded-full bg-[#1f2937] text-blue-500">
            <Upload size={32} />
          </div>

          <h3 className="mt-4 text-lg font-medium text-white">
            Upload Candidate PDFs
          </h3>

          <p className="mt-2 text-sm text-gray-500">
            Multiple files supported
          </p>

          <input
            type="file"
            multiple
            accept=".pdf,.csv"
            className="hidden"
            id="fileInput"
            onChange={(e) =>
              setFiles(
                Array.from(
                  e.target.files ?? []
                )
              )
            }
          />

          <div className="flex gap-4 mt-8">

            <label
              htmlFor="fileInput"
              className="cursor-pointer px-5 py-3 rounded-lg bg-[#1f2937] border border-gray-700 text-white hover:bg-[#293548]"
            >
              Choose Files
            </label>

            <button
              onClick={handleUpload}
              disabled={
                loading ||
                files.length === 0
              }
              className="px-5 py-3 rounded-lg bg-blue-600 text-white hover:bg-blue-700 disabled:opacity-50"
            >
              {loading
                ? "Processing..."
                : "Upload & Process"}
            </button>

          </div>

          {files.length > 0 && (
            <div className="mt-8 w-full max-w-8xl grid grid-cols-1 md:grid-cols-2 lg:grid-cols-6 gap-3">
  {files.map((file) => (
    <div
      key={file.name}
      className="flex items-center gap-3 p-3 bg-[#111827] border border-gray-800 rounded-lg min-w-0"
    >
      <FileText
        size={18}
        className="text-blue-500 shrink-0"
      />

      <span
        className="text-sm text-gray-300 truncate"
        title={file.name}
      >
        {file.name}
      </span>
    </div>
  ))}
</div>
          )}

        </div>
      </div>
    </div>
  );
}