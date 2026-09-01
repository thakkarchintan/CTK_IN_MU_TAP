import { NavLink, Outlet } from "react-router-dom";
import clsx from "clsx";

import { useAuth } from "../hooks/useAuth";

const NAV_ITEMS = [
  { to: "/", label: "Dashboard", end: true },
  { to: "/strategies", label: "Strategies" },
  { to: "/backtests", label: "Backtest" },
  { to: "/deployments", label: "Deployments" },
  { to: "/trade-log", label: "Trade Log" },
  { to: "/audit-log", label: "Audit Log" },
  { to: "/change-log", label: "Change Log" },
  { to: "/build-log", label: "Build Log" },
  { to: "/settings", label: "Settings" },
];

export function AppLayout() {
  const { user, logout } = useAuth();

  return (
    <div className="flex h-screen bg-slate-950">
      <aside className="flex w-56 flex-col border-r border-slate-800 bg-slate-900">
        <div className="px-4 py-5 text-lg font-semibold text-slate-100">V1 Trading</div>
        <nav className="flex-1 space-y-1 px-2">
          {NAV_ITEMS.map((item) => (
            <NavLink
              key={item.to}
              to={item.to}
              end={item.end}
              className={({ isActive }) =>
                clsx(
                  "block rounded-md px-3 py-2 text-sm",
                  isActive
                    ? "bg-slate-800 text-slate-100"
                    : "text-slate-400 hover:bg-slate-800/60 hover:text-slate-200"
                )
              }
            >
              {item.label}
            </NavLink>
          ))}
        </nav>
        <div className="border-t border-slate-800 p-3 text-xs text-slate-500">
          <div className="mb-2 truncate">{user?.email}</div>
          <button onClick={logout} className="text-slate-400 hover:text-slate-200">
            Log out
          </button>
        </div>
      </aside>
      <main className="flex-1 overflow-y-auto p-6">
        <Outlet />
      </main>
    </div>
  );
}
