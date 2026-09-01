import { useEffect, useState } from "react";

import { api } from "../services/api";
import { formatIST } from "../services/format";
import { BuildLogEntry } from "../types";

export function BuildLog() {
  const [entries, setEntries] = useState<BuildLogEntry[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    api
      .get<BuildLogEntry[]>("/build-log")
      .then((res) => setEntries(res.data))
      .catch(() => setError("Could not load build log"))
      .finally(() => setLoading(false));
  }, []);

  return (
    <div>
      <h1 className="mb-1 text-xl font-semibold text-slate-100">Build Log</h1>
      <p className="mb-6 text-sm text-slate-500">
        A running record of what has been built into this application, step by step.
      </p>

      {loading && <p className="text-sm text-slate-500">Loading...</p>}
      {error && <p className="text-sm text-red-400">{error}</p>}

      <div className="space-y-4">
        {entries.map((entry) => (
          <div key={entry.id} className="rounded-lg border border-slate-800 bg-slate-900 p-4">
            <div className="mb-1 flex items-center justify-between">
              <span className="rounded bg-blue-950 px-2 py-0.5 text-xs font-medium text-blue-300">
                {entry.step}
              </span>
              <span className="text-xs text-slate-500">{formatIST(entry.timestamp)}</span>
            </div>
            <h3 className="mb-1 text-sm font-medium text-slate-100">{entry.title}</h3>
            <p className="text-sm text-slate-400">{entry.description}</p>
          </div>
        ))}
      </div>
    </div>
  );
}
