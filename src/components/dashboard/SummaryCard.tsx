import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { cn } from "@/lib/utils";

interface SummaryCardProps {
  title: string;
  value: number;
  icon: React.ReactNode;
  isCurrency?: boolean;
  className?: string;
}

export const SummaryCard = ({ title, value, icon, isCurrency = true, className }: SummaryCardProps) => {
  const formattedValue = isCurrency
    ? new Intl.NumberFormat("en-US", { style: "currency", currency: "USD" }).format(value)
    : value;

  return (
    <Card className={cn("flex flex-col justify-between", className)}>
      <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
        <CardTitle className="text-sm font-medium">{title}</CardTitle>
        {icon}
      </CardHeader>
      <CardContent>
        <div className="text-2xl font-bold">{formattedValue}</div>
      </CardContent>
    </Card>
  );
};