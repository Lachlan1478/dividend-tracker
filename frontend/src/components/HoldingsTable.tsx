// src/components/HoldingsTable.tsx
import TableRow from "./TableRow";

interface RowData {
  id: number;
  ticker: string;
  shares: string;
  loading: boolean;
  data: {
    ex_dividend_date?: string;
    payment_date?: string;
    dividend_amount?: number;
    franking_percent?: number;
  } | null;
}

export default function HoldingsTable({ rows }: { rows: RowData[] }) {
  return (
    <table className="w-full mt-8 text-left border-collapse">
      <thead>
        <tr className="text-sm text-gray-600 uppercase">
          <th className="p-3">Ticker</th>
          <th className="p-3">Shares</th>
          <th className="p-3">Ex-Date</th>
          <th className="p-3">Payment Date</th>
          <th className="p-3">Amount</th>
          <th className="p-3">Franking</th>
        </tr>
      </thead>
      <tbody>
        {rows.map((row) => (
          <TableRow key={row.id} row={row} />
        ))}
      </tbody>
    </table>
  );
}
