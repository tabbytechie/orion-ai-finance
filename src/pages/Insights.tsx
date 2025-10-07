import { SpendingOverTimeChart } from "@/components/insights/SpendingOverTimeChart";
import { CategorySpendingChart } from "@/components/insights/CategorySpendingChart";
import { recentTransactions } from "@/lib/mock-data";

export default function Insights() {
  return (
    <div className="space-y-6 animate-fade-in">
      <div>
        <h1 className="text-3xl font-bold text-foreground">Financial Insights</h1>
        <p className="text-muted-foreground">Visualize your spending habits and patterns.</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <SpendingOverTimeChart transactions={recentTransactions} />
        <CategorySpendingChart transactions={recentTransactions} />
      </div>
    </div>
  );
}