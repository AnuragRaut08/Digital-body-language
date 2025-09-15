import React from "react";

export default function ResultCard({ result }) {
  if (!result || !result.score) {
    return <div>Invalid result</div>;
  }
  return (
    <div className="mt-3 p-4 bg-gradient-to-r from-yellow-50 to-white rounded shadow-sm">
      <h3 className="text-lg font-semibold">Engagement Score: {Math.round(result.score)}</h3>
      <p className="text-sm text-gray-600">Label: {result.label}</p>
      <pre className="text-xs mt-2 bg-gray-50 p-2 rounded">{JSON.stringify(result.details, null, 2)}</pre>
    </div>
  );
}

