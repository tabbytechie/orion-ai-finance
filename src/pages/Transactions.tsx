import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Search, Filter, Download, Plus } from "lucide-react";
import { Badge } from "@/components/ui/badge";

const transactions = [
  { id: "1", date: "2025-10-06", description: "Salary Deposit", category: "Income", amount: 6000, status: "completed" },
  { id: "2", date: "2025-10-05", description: "Amazon Purchase", category: "Shopping", amount: -234.50, status: "completed" },
  { id: "3", date: "2025-10-04", description: "Restaurant", category: "Food", amount: -85.20, status: "completed" },
  { id: "4", date: "2025-10-03", description: "Electric Bill", category: "Utilities", amount: -120.00, status: "completed" },
  { id: "5", date: "2025-10-02", description: "Freelance Payment", category: "Income", amount: 850.00, status: "pending" },
  { id: "6", date: "2025-10-01", description: "Gas Station", category: "Transportation", amount: -65.00, status: "completed" },
];

export default function Transactions() {
  const [search, setSearch] = useState("");
  const [category, setCategory] = useState("all");

  const filteredTransactions = transactions.filter((t) => {
    const matchesSearch = t.description.toLowerCase().includes(search.toLowerCase());
    const matchesCategory = category === "all" || t.category === category;
    return matchesSearch && matchesCategory;
  });

  return (
    <div className="space-y-6 animate-fade-in">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-foreground">Transactions</h1>
          <p className="text-muted-foreground">Manage and track all your financial transactions</p>
        </div>
        <Button className="bg-gradient-primary">
          <Plus className="w-4 h-4 mr-2" />
          Add Transaction
        </Button>
      </div>

      <Card className="shadow-soft">
        <CardHeader>
          <div className="flex flex-col sm:flex-row gap-4 items-start sm:items-center justify-between">
            <CardTitle>All Transactions</CardTitle>
            <div className="flex gap-2 w-full sm:w-auto">
              <div className="relative flex-1 sm:w-64">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-muted-foreground" />
                <Input
                  placeholder="Search transactions..."
                  value={search}
                  onChange={(e) => setSearch(e.target.value)}
                  className="pl-10"
                />
              </div>
              <Select value={category} onValueChange={setCategory}>
                <SelectTrigger className="w-40">
                  <Filter className="w-4 h-4 mr-2" />
                  <SelectValue placeholder="Category" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">All Categories</SelectItem>
                  <SelectItem value="Income">Income</SelectItem>
                  <SelectItem value="Food">Food</SelectItem>
                  <SelectItem value="Shopping">Shopping</SelectItem>
                  <SelectItem value="Transportation">Transportation</SelectItem>
                  <SelectItem value="Utilities">Utilities</SelectItem>
                </SelectContent>
              </Select>
              <Button variant="outline" size="icon">
                <Download className="w-4 h-4" />
              </Button>
            </div>
          </div>
        </CardHeader>
        <CardContent>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Date</TableHead>
                <TableHead>Description</TableHead>
                <TableHead>Category</TableHead>
                <TableHead>Status</TableHead>
                <TableHead className="text-right">Amount</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {filteredTransactions.map((transaction) => (
                <TableRow key={transaction.id} className="hover:bg-muted/50">
                  <TableCell className="font-medium">{transaction.date}</TableCell>
                  <TableCell>{transaction.description}</TableCell>
                  <TableCell>
                    <Badge variant="secondary">{transaction.category}</Badge>
                  </TableCell>
                  <TableCell>
                    <Badge variant={transaction.status === "completed" ? "default" : "outline"}>
                      {transaction.status}
                    </Badge>
                  </TableCell>
                  <TableCell
                    className={`text-right font-semibold ${
                      transaction.amount > 0 ? "text-success" : "text-foreground"
                    }`}
                  >
                    {transaction.amount > 0 ? "+" : ""}${Math.abs(transaction.amount).toFixed(2)}
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </CardContent>
      </Card>
    </div>
  );
}
