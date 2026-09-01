import { Card } from "../components/Card";

export function Dashboard() {
  return (
    <div>
      <h1 className="mb-6 text-xl font-semibold text-slate-100">Dashboard</h1>
      <div className="grid grid-cols-1 gap-4 md:grid-cols-3">
        <Card title="Strategies">
          <p className="text-sm text-slate-500">
            Total strategies, active deployments, and recent backtests will appear here starting Step 2/3.
          </p>
        </Card>
        <Card title="Trading">
          <p className="text-sm text-slate-500">
            Today's P&amp;L, open positions, recent trades, and running strategies will appear here starting
            Step 4.
          </p>
        </Card>
        <Card title="Recent Activity">
          <p className="text-sm text-slate-500">
            Recent strategy changes, deployments, orders, and errors will appear here as those features land.
          </p>
        </Card>
      </div>
    </div>
  );
}
