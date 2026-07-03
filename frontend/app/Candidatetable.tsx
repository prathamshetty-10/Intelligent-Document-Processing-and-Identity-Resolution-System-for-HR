import { useMemo, useState } from "react";

type Props = {
  candidates: any[];
};

const columns = [
  { key: "candidate_id", label: "ID" },
  { key: "full_name", label: "Name" },
  { key: "email", label: "Email" },
  { key: "phone_number", label: "Phone" },
  { key: "date_of_birth", label: "DOB" },
  { key: "age", label: "Age" },
  { key: "address", label: "Address" },
  { key: "role", label: "Role" },
  { key: "location", label: "Location" },
  { key: "date_of_joining", label: "DOJ" },
  { key: "reporting_manager", label: "Manager" },
  { key: "salary", label: "Salary" },
  { key: "company_name", label: "Company" },
  { key: "education", label: "Education" },
  { key: "experience_years", label: "Experience" },
  { key: "cgpa", label: "CGPA" },
  { key: "aadhaar_number", label: "Aadhaar" },
  { key: "pan_number", label: "PAN" },
  { key: "bank_name", label: "Bank" },
  { key: "account_number", label: "Account" },
  { key: "ifsc_code", label: "IFSC" },
  {
    key: "account_holder_address",
    label: "Account Address",
  },
  { key: "t_shirt_size", label: "T-Shirt" },
];

const defaultColumns = [
  "candidate_id",
  "full_name",
  "email",
  "phone_number",
  "role",
  "company_name",
];

export default function CandidateTable({
  candidates,
}: Props) {
  const [showColumns, setShowColumns] =
    useState(false);

  const [visibleColumns, setVisibleColumns] =
    useState<string[]>(defaultColumns);

  const visibleColumnDefs = useMemo(
    () =>
      columns.filter((col) =>
        visibleColumns.includes(col.key)
      ),
    [visibleColumns]
  );

  const toggleColumn = (key: string) => {
    setVisibleColumns((prev) =>
      prev.includes(key)
        ? prev.filter((c) => c !== key)
        : [...prev, key]
    );
  };

  if (candidates.length === 0) {
    return (
      <div className="p-12 text-center text-gray-500">
        No candidate data available.
        Upload PDFs to begin.
      </div>
    );
  }

  return (
    <div className="p-6">
      {/* Toolbar */}
      <div className="mb-4 flex justify-end relative">
        <button
          onClick={() =>
            setShowColumns((prev) => !prev)
          }
          className="rounded-lg border border-gray-700 bg-[#111827] px-4 py-2 text-sm text-white hover:bg-[#1f2937]"
        >
          Filter Columns
        </button>

        {showColumns && (
          <div className="absolute top-12 right-0 z-20 w-64 rounded-xl border border-gray-700 bg-[#111827] p-4 shadow-xl">
            <div className="mb-3 flex items-center justify-between">
              <p className="text-sm font-medium text-gray-300">
                Show Columns
              </p>

              <button
                onClick={() =>
                  setVisibleColumns(defaultColumns)
                }
                className="text-xs text-blue-400 hover:text-blue-300"
              >
                Reset
              </button>
            </div>

            <div className="max-h-80 space-y-2 overflow-y-auto">
              {columns.map((col) => (
                <label
                  key={col.key}
                  className="flex cursor-pointer items-center gap-3 text-sm text-gray-300"
                >
                  <input
                    type="checkbox"
                    checked={visibleColumns.includes(
                      col.key
                    )}
                    onChange={() =>
                      toggleColumn(col.key)
                    }
                    className="h-4 w-4"
                  />

                  {col.label}
                </label>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* Table */}
      <div className="overflow-x-auto rounded-xl border border-gray-800">
        <table className="min-w-full text-sm">
          <thead className="bg-[#1f2937] text-gray-400">
            <tr>
              {visibleColumnDefs.map((col) => (
                <th
                  key={col.key}
                  className="whitespace-nowrap px-6 py-4 text-left"
                >
                  {col.label}
                </th>
              ))}

              <th className="whitespace-nowrap px-6 py-4 text-left">
                Status
              </th>
            </tr>
          </thead>

          <tbody className="divide-y divide-gray-800">
            {candidates.map(
              (candidate, index) => {
                const complete =
                  candidate.full_name &&
                  candidate.email &&
                  candidate.phone_number &&
                  candidate.date_of_birth &&
                  candidate.role &&
                  candidate.date_of_joining &&
                  candidate.bank_name &&
                  candidate.account_number &&
                  candidate.ifsc_code &&
                  candidate.aadhaar_number &&
                  candidate.pan_number;

                return (
                  <tr
                    key={index}
                    className="hover:bg-[#0b0f1a]"
                  >
                    {visibleColumnDefs.map(
                      (col) => (
                        <td
                          key={col.key}
                          className={`px-6 py-4 ${
                            col.key ===
                            "full_name"
                              ? "font-medium text-white"
                              : ""
                          }`}
                        >
                          {candidate[col.key] ??
                            "-"}
                        </td>
                      )
                    )}

                    <td className="px-6 py-4">
                      {complete ? (
                        <span className="rounded-full border border-green-900 bg-green-900/30 px-3 py-1 text-xs text-green-400">
                          Complete
                        </span>
                      ) : (
                        <span className="rounded-full border border-yellow-900 bg-yellow-900/30 px-3 py-1 text-xs text-yellow-400">
                          Partial
                        </span>
                      )}
                    </td>
                  </tr>
                );
              }
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
