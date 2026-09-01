import { ReactNode } from "react";

export function Card({ title, children }: { title?: string; children: ReactNode }) {
  return (
    <div className="rounded-lg border border-slate-800 bg-slate-900 p-4">
      {title && <h3 className="mb-3 text-sm font-medium text-slate-400">{title}</h3>}
      {children}
    </div>
  );
}
