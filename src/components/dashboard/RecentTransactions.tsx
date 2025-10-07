import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { cn } from "@/lib/utils";

interface Transaction {
  id: string;
  date: string;
  description: string;
  category: string;
  amount: number;
  status: "Completed" | "Pending";
}

interface RecentTransactionsProps {
  transactions: Transaction[];
}

export const RecentTransactions = ({ transactions }: RecentTransactionsProps) => {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Recent Transactions</CardTitle>
      </CardHeader>
      <CardContent>
        <ul className="space-y-4">
          {transactions.map((transaction) => (
            <li key={transaction.id} className="flex justify-between items-center">
              <div className="flex items-center space-x-4">
                <div className="text-sm text-muted-foreground">{new Date(transaction.date).toLocaleDateString("en-US", { month: "short", day: "numeric" })}</div>
                <div>
                  <div className="font-medium">{transaction.description}</div>
                  <div className="text-sm text-muted-foreground">{transaction.category}</div>
                </div>
              </div>
              <div className="flex items-center space-x-4">
                <span
                  className={cn(
                    "text-lg font-bold",
                    transaction.amount > 0 ? "text-green-500" : "text-red-500"
                  )}
                >
                  {new Intl.NumberFormat("en-US", {
                    style: "currency",
                    currency: "USD",
                  }).format(transaction.amount)}
                </span>
                <Badge
                  variant={transaction.status === "Completed" ? "default" : "secondary"}
                  className="hidden sm:inline-flex"
                >
                  {transaction.status}
                </Badge>
              </div>
            </li>
          ))}
        </ul>
      </CardContent>
    </Card>
  );
};