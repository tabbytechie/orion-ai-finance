export const summaryData = {
  totalBalance: 12345.67,
  totalIncome: 5000.0,
  totalExpenses: 2500.0,
  accounts: [
    { id: "acc1", name: "Checking", balance: 8765.43 },
    { id: "acc2", name: "Savings", balance: 3580.24 },
  ],
};

export const recentTransactions = [
  {
    id: "txn1",
    date: "2023-10-26",
    description: "Spotify Subscription",
    category: "Entertainment",
    amount: -10.99,
    status: "Completed",
  },
  {
    id: "txn2",
    date: "2023-10-25",
    description: "Paycheck",
    category: "Income",
    amount: 2500.0,
    status: "Completed",
  },
  {
    id: "txn3",
    date: "2023-10-24",
    description: "Groceries from Whole Foods",
    category: "Food",
    amount: -75.5,
    status: "Completed",
  },
  {
    id: "txn4",
    date: "2023-10-23",
    description: "Transfer to Savings",
    category: "Transfers",
    amount: -500.0,
    status: "Completed",
  },
  {
    id: "txn5",
    date: "2023-10-22",
    description: "Dinner with friends",
    category: "Food",
    amount: -55.0,
    status: "Pending",
  },
];