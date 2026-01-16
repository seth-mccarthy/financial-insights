// components/Dashboard.tsx
import React from 'react';
import { InsightsData } from '../types';
import { PieChart, Pie, Cell, ResponsiveContainer, Legend, Tooltip } from 'recharts';

interface DashboardProps {
  insights: InsightsData;
  loading: boolean;
}

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884D8'];

const Dashboard: React.FC<DashboardProps> = ({ insights, loading }) => {
  if (loading) {
    return <div className="loading">Loading insights...</div>;
  }

  const chartData = insights.top_categories.map(cat => ({
    name: cat.category,
    value: cat.total,
  }));

  return (
    <div className="dashboard">
      <h2>Your Financial Insights</h2>

      {/* Summary Cards */}
      <div className="summary-cards">
        <div className="card">
          <h3>Total Spending</h3>
          <p className="amount">${insights.total_spending.toFixed(2)}</p>
        </div>
        <div className="card">
          <h3>Monthly Average</h3>
          <p className="amount">${insights.monthly_average.toFixed(2)}</p>
        </div>
        <div className="card">
          <h3>Anomalies Detected</h3>
          <p className="amount">{insights.anomalies.length}</p>
        </div>
      </div>

      {/* Spending by Category */}
      <div className="chart-section">
        <h3>Spending by Category</h3>
        <ResponsiveContainer width="100%" height={300}>
          <PieChart>
            <Pie
              data={chartData}
              cx="50%"
              cy="50%"
              labelLine={false}
              label={(entry) => `${entry.name}: $${entry.value.toFixed(0)}`}
              outerRadius={80}
              fill="#8884d8"
              dataKey="value"
            >
              {chartData.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
              ))}
            </Pie>
            <Tooltip />
            <Legend />
          </PieChart>
        </ResponsiveContainer>
      </div>

      {/* Top Categories */}
      <div className="categories-section">
        <h3>Top Spending Categories</h3>
        <div className="categories-list">
          {insights.top_categories.map((cat, index) => (
            <div key={index} className="category-item">
              <div className="category-info">
                <span className="category-name">{cat.category}</span>
                <span className="category-percentage">{cat.percentage.toFixed(1)}%</span>
              </div>
              <div className="category-amount">${cat.total.toFixed(2)}</div>
            </div>
          ))}
        </div>
      </div>

      {/* Anomalies */}
      {insights.anomalies.length > 0 && (
        <div className="anomalies-section">
          <h3>⚠️ Unusual Transactions</h3>
          <div className="anomalies-list">
            {insights.anomalies.map((anomaly, index) => (
              <div key={index} className="anomaly-item">
                <div className="anomaly-header">
                  <span className="anomaly-date">{anomaly.date}</span>
                  <span className="anomaly-amount">${anomaly.amount.toFixed(2)}</span>
                </div>
                <div className="anomaly-description">{anomaly.description}</div>
                <div className="anomaly-reason">{anomaly.reason}</div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default Dashboard;