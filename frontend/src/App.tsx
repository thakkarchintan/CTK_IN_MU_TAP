import { Routes, Route } from "react-router-dom";

import { AppLayout } from "./layouts/AppLayout";
import { ProtectedRoute } from "./components/ProtectedRoute";
import { Login } from "./pages/Login";
import { Dashboard } from "./pages/Dashboard";
import { BuildLog } from "./pages/BuildLog";
import { Placeholder } from "./pages/Placeholder";

export default function App() {
  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route
        element={
          <ProtectedRoute>
            <AppLayout />
          </ProtectedRoute>
        }
      >
        <Route path="/" element={<Dashboard />} />
        <Route path="/strategies" element={<Placeholder title="Strategies" step="Step 2" />} />
        <Route path="/strategies/:id" element={<Placeholder title="Strategy Detail" step="Step 2" />} />
        <Route path="/strategies/:id/edit" element={<Placeholder title="Create / Edit Strategy" step="Step 2" />} />
        <Route path="/strategies/new" element={<Placeholder title="Create / Edit Strategy" step="Step 2" />} />
        <Route path="/backtests" element={<Placeholder title="Backtest" step="Step 3" />} />
        <Route path="/backtests/:id" element={<Placeholder title="Backtest Results" step="Step 3" />} />
        <Route path="/deployments/new" element={<Placeholder title="Deploy Strategy" step="Step 4" />} />
        <Route path="/deployments" element={<Placeholder title="Deployments" step="Step 4" />} />
        <Route path="/deployments/:id" element={<Placeholder title="Deployment Detail" step="Step 4" />} />
        <Route path="/trade-log" element={<Placeholder title="Trade Log" step="Step 4" />} />
        <Route path="/audit-log" element={<Placeholder title="Audit Log" step="Step 2" />} />
        <Route path="/change-log" element={<Placeholder title="Change Log" step="Step 2" />} />
        <Route path="/build-log" element={<BuildLog />} />
        <Route path="/settings" element={<Placeholder title="Settings / Zerodha Connection" step="Step 6" />} />
      </Route>
    </Routes>
  );
}
