import React from "react";
import {
  LineChart, Line, XAxis, YAxis, Tooltip, Legend, ResponsiveContainer,
  PieChart, Pie, Cell, BarChart, Bar
} from "recharts";
import { Card } from "react-bootstrap";

const COLORS = ["#008080", "#00C49F", "#FFBB28", "#FF8042", "#AF19FF", "#FF4560"];

export default function ChartsSection({ insights }) {
  const trends = Object.entries(insights.monthly_trends || {}).map(([month, total]) => ({
    month,
    total: parseFloat(total),
  }));

  const expenses = Object.entries(insights.categorized_expenses || {}).map(
    ([category, total]) => ({ name: category, value: parseFloat(total) })
  );

  const merchants = insights.top_merchants.map(([merchant, count]) => ({
    merchant,
    count,
  }));

  return (
    <div className="row">
      <div className="col-md-6">
        <Card className="mb-4 shadow-sm">
          <Card.Body>
            <Card.Title>📈 Monthly Trends</Card.Title>
            <ResponsiveContainer width="100%" height={250}>
              <LineChart data={trends}>
                <XAxis dataKey="month" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Line type="monotone" dataKey="total" stroke="#008080" />
              </LineChart>
            </ResponsiveContainer>
          </Card.Body>
        </Card>
      </div>

      <div className="col-md-6">
        <Card className="mb-4 shadow-sm">
          <Card.Body>
            <Card.Title>🧾 Expense Categories</Card.Title>
            <ResponsiveContainer width="100%" height={250}>
              <PieChart>
                <Pie data={expenses} dataKey="value" nameKey="name" outerRadius={80} label>
                  {expenses.map((_, i) => (
                    <Cell key={`cell-${i}`} fill={COLORS[i % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip />
                <Legend />
              </PieChart>
            </ResponsiveContainer>
          </Card.Body>
        </Card>
      </div>

      <div className="col-md-12">
        <Card className="mb-4 shadow-sm">
          <Card.Body>
            <Card.Title>🏪 Top Merchants</Card.Title>
            <ResponsiveContainer width="100%" height={250}>
              <BarChart data={merchants}>
                <XAxis dataKey="merchant" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Bar dataKey="count" fill="#00A896" />
              </BarChart>
            </ResponsiveContainer>
          </Card.Body>
        </Card>
      </div>
    </div>
  );
}
