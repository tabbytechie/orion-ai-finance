import { DollarSign, TrendingUp, TrendingDown } from "lucide-react";
import { SummaryCard } from "@/components/dashboard/SummaryCard";
import { AccountSummary } from "@/components/dashboard/AccountSummary";
import { RecentTransactions } from "@/components/dashboard/RecentTransactions";
import { summaryData, recentTransactions } from "@/lib/mock-data";

export default function Dashboard() {
  return (
    <div className="space-y-6 animate-fade-in">
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <SummaryCard
          title="Total Balance"
          value={summaryData.totalBalance}
          icon={<DollarSign className="w-6 h-6 text-muted-foreground" />}
        />
        <SummaryCard
          title="Monthly Income"
          value={summaryData.totalIncome}
          icon={<TrendingUp className="w-6 h-6 text-muted-foreground" />}
          className="text-green-500"
        />
        <SummaryCard
          title="Monthly Expenses"
          value={summaryData.totalExpenses}
          icon={<TrendingDown className="w-6 h-6 text-muted-foreground" />}
          className="text-red-500"
        />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-1">
          <AccountSummary accounts={summaryData.accounts} />
        </div>
        <div className="lg:col-span-2">
          <RecentTransactions transactions={recentTransactions} />
        </div>
      </div>
    </div>
  );
}