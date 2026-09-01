export function Placeholder({ title, step }: { title: string; step: string }) {
  return (
    <div>
      <h1 className="mb-2 text-xl font-semibold text-slate-100">{title}</h1>
      <p className="text-sm text-slate-500">This screen will be built in {step}.</p>
    </div>
  );
}
