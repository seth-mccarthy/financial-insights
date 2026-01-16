// types.ts - TypeScript interfaces and types

export interface Transaction {
  date: string;
  description: string;
  amount: number;
  category: string;
}

export interface SpendingInsight {
  category: string;
  total: number;
  percentage: number;
  trend: 'up' | 'down' | 'stable';
}

export interface AnomalyAlert {
  date: string;
  description: string;
  amount: number;
  reason: string;
}

export interface InsightsData {
  total_spending: number;
  top_categories: SpendingInsight[];
  anomalies: AnomalyAlert[];
  monthly_average: number;
}

export interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
}

export interface UploadResponse {
  message: string;
  transactions_count: number;
}