import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

interface Account {
  id: string;
  name: string;
  balance: number;
}

interface AccountSummaryProps {
  accounts: Account[];
}

export const AccountSummary = ({ accounts }: AccountSummaryProps) => {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Your Accounts</CardTitle>
      </CardHeader>
      <CardContent>
        <ul className="space-y-4">
          {accounts.map((account) => (
            <li key={account.id} className="flex justify-between items-center">
              <span className="font-medium">{account.name}</span>
              <span className="text-lg font-bold">
                {new Intl.NumberFormat("en-US", { style: "currency", currency: "USD" }).format(account.balance)}
              </span>
            </li>
          ))}
        </ul>
      </CardContent>
    </Card>
  );
};