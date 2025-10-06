import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts";

const data = [
  { month: "Jan", spending: 4200, income: 6000 },
  { month: "Feb", spending: 3800, income: 6000 },
  { month: "Mar", spending: 4500, income: 6000 },
  { month: "Apr", spending: 3200, income: 6200 },
  { month: "May", spending: 5100, income: 6200 },
  { month: "Jun", spending: 4600, income: 6200 },
];

export function SpendingChart() {
  return (
    <Card className="shadow-soft">
      <CardHeader>
        <CardTitle className="text-lg font-semibold">Spending Trends</CardTitle>
      </CardHeader>
      <CardContent>
        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={data}>
            <CartesianGrid strokeDasharray="3 3" className="stroke-border" />
            <XAxis dataKey="month" className="text-xs" />
            <YAxis className="text-xs" />
            <Tooltip
              contentStyle={{
                backgroundColor: "hsl(var(--popover))",
                border: "1px solid hsl(var(--border))",
                borderRadius: "8px",
              }}
            />
            <Line
              type="monotone"
              dataKey="spending"
              stroke="hsl(var(--chart-1))"
              strokeWidth={2}
              dot={{ fill: "hsl(var(--chart-1))", r: 4 }}
            />
            <Line
              type="monotone"
              dataKey="income"
              stroke="hsl(var(--chart-3))"
              strokeWidth={2}
              dot={{ fill: "hsl(var(--chart-3))", r: 4 }}
            />
          </LineChart>
        </ResponsiveContainer>
      </CardContent>
    </Card>
  );
}
