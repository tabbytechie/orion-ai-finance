import { DollarSign, TrendingUp, TrendingDown, AlertCircle } from "lucide-react";
import { KPICard } from "@/components/dashboard/KPICard";
import { SpendingChart } from "@/components/dashboard/SpendingChart";
import { CategoryChart } from "@/components/dashboard/CategoryChart";
import { RecentTransactions } from "@/components/dashboard/RecentTransactions";

export default function Dashboard() {
  return (
    <div className="space-y-6 animate-fade-in">
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <KPICard
          title="Total Balance"
          value="$45,231.89"
          change="+20.1% from last month"
          changeType="positive"
          icon={<DollarSign className="w-6 h-6" />}
        />
        <KPICard
          title="Income"
          value="$12,234.00"
          change="+12.5% from last month"
          changeType="positive"
          icon={<TrendingUp className="w-6 h-6" />}
        />
        <KPICard
          title="Expenses"
          value="$4,600.00"
          change="-8.2% from last month"
          changeType="positive"
          icon={<TrendingDown className="w-6 h-6" />}
        />
        <KPICard
          title="Anomalies"
          value="2"
          change="Requires attention"
          changeType="negative"
          icon={<AlertCircle className="w-6 h-6" />}
        />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <SpendingChart />
        <CategoryChart />
      </div>

      <RecentTransactions />
    </div>
  );
}
