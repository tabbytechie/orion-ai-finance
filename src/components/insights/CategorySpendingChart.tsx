import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { ResponsiveContainer, PieChart, Pie, Cell, Tooltip, Legend } from 'recharts';

interface Transaction {
  id: string;
  date: string;
  description: string;
  category: string;
  amount: number;
  status: "Completed" | "Pending";
}

interface CategorySpendingChartProps {
  transactions: Transaction[];
}

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#AF19FF', '#FF4560'];

const processDataForCategoryChart = (transactions: Transaction[]) => {
  const categoryData = transactions
    .filter(t => t.amount < 0 && t.status === 'Completed' && t.category !== 'Transfers')
    .reduce((acc, t) => {
      const category = t.category;
      const spending = Math.abs(t.amount);
      if (!acc[category]) {
        acc[category] = { name: category, value: 0 };
      }
      acc[category].value += spending;
      return acc;
    }, {} as Record<string, { name: string; value: number }>);

  return Object.values(categoryData);
};

export const CategorySpendingChart = ({ transactions }: CategorySpendingChartProps) => {
  const chartData = processDataForCategoryChart(transactions);

  return (
    <Card>
      <CardHeader>
        <CardTitle>Spending by Category</CardTitle>
        <CardDescription>A breakdown of your spending by category.</CardDescription>
      </CardHeader>
      <CardContent>
        <ResponsiveContainer width="100%" height={300}>
          <PieChart>
            <Pie
              isAnimationActive={false}
              data={chartData}
              cx="50%"
              cy="50%"
              labelLine={false}
              outerRadius={80}
              fill="#8884d8"
              dataKey="value"
              nameKey="name"
              label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
            >
              {chartData.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
              ))}
            </Pie>
            <Tooltip formatter={(value: number) => new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(value)} />
            <Legend />
          </PieChart>
        </ResponsiveContainer>
      </CardContent>
    </Card>
  );
};