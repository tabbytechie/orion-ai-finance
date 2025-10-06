import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { ArrowDownRight, ArrowUpRight } from "lucide-react";
import { cn } from "@/lib/utils";

interface Transaction {
  id: string;
  description: string;
  amount: number;
  type: "income" | "expense";
  date: string;
  category: string;
}

const transactions: Transaction[] = [
  { id: "1", description: "Salary Deposit", amount: 6000, type: "income", date: "2025-10-01", category: "Income" },
  { id: "2", description: "Grocery Store", amount: -125.50, type: "expense", date: "2025-10-02", category: "Food" },
  { id: "3", description: "Gas Station", amount: -65.00, type: "expense", date: "2025-10-03", category: "Transportation" },
  { id: "4", description: "Netflix Subscription", amount: -15.99, type: "expense", date: "2025-10-04", category: "Entertainment" },
  { id: "5", description: "Freelance Project", amount: 850, type: "income", date: "2025-10-05", category: "Income" },
];

export function RecentTransactions() {
  return (
    <Card className="shadow-soft">
      <CardHeader>
        <CardTitle className="text-lg font-semibold">Recent Transactions</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          {transactions.map((transaction) => (
            <div
              key={transaction.id}
              className="flex items-center justify-between p-3 rounded-lg hover:bg-muted/50 transition-colors"
            >
              <div className="flex items-center gap-3">
                <div
                  className={cn(
                    "w-10 h-10 rounded-full flex items-center justify-center",
                    transaction.type === "income" ? "bg-success/10" : "bg-destructive/10"
                  )}
                >
                  {transaction.type === "income" ? (
                    <ArrowUpRight className="w-5 h-5 text-success" />
                  ) : (
                    <ArrowDownRight className="w-5 h-5 text-destructive" />
                  )}
                </div>
                <div>
                  <p className="font-medium text-card-foreground">{transaction.description}</p>
                  <p className="text-sm text-muted-foreground">{transaction.category}</p>
                </div>
              </div>
              <div className="text-right">
                <p
                  className={cn(
                    "font-semibold",
                    transaction.type === "income" ? "text-success" : "text-card-foreground"
                  )}
                >
                  {transaction.type === "income" ? "+" : ""}${Math.abs(transaction.amount).toFixed(2)}
                </p>
                <p className="text-sm text-muted-foreground">{transaction.date}</p>
              </div>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  );
}
