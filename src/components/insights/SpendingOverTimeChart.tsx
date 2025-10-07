import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { ResponsiveContainer, LineChart, CartesianGrid, XAxis, YAxis, Tooltip, Legend, Line } from 'recharts';

interface Transaction {
  id: string;
  date: string;
  description: string;
  category: string;
  amount: number;
  status: "Completed" | "Pending";
}

interface SpendingOverTimeChartProps {
  transactions: Transaction[];
}

const processDataForSpendingChart = (transactions: Transaction[]) => {
  const spendingData = transactions
    .filter(t => t.amount < 0 && t.status === 'Completed')
    .reduce((acc, t) => {
      const date = new Date(t.date).toLocaleDateString("en-US", { month: 'short', day: 'numeric' });
      const spending = Math.abs(t.amount);
      if (!acc[date]) {
        acc[date] = { date, spending: 0 };
      }
      acc[date].spending += spending;
      return acc;
    }, {} as Record<string, { date: string; spending: number }>);

  return Object.values(spendingData).sort((a, b) => new Date(a.date).getTime() - new Date(b.date).getTime());
};


export const SpendingOverTimeChart = ({ transactions }: SpendingOverTimeChartProps) => {
  const chartData = processDataForSpendingChart(transactions);

  return (
    <Card>
      <CardHeader>
        <CardTitle>Spending Over Time</CardTitle>
        <CardDescription>A look at your daily spending trends.</CardDescription>
      </CardHeader>
      <CardContent>
        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={chartData} isAnimationActive={false}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="date" />
            <YAxis tickFormatter={(value) => `$${value}`} />
            <Tooltip formatter={(value: number) => new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(value)} />
            <Legend />
            <Line type="monotone" dataKey="spending" stroke="#ef4444" activeDot={{ r: 8 }} />
          </LineChart>
        </ResponsiveContainer>
      </CardContent>
    </Card>
  );
};