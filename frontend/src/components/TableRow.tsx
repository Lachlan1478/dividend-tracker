// src/components/TableRow.tsx

import { Loader2 } from "lucide-react";

type RowData = {
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
};

export default function TableRow({ row }: { row: RowData }) {
  if (row.loading) {
    return (
      <tr className="bg-white rounded shadow">
        <td className="p-3 font-medium">{row.ticker}</td>
        <td className="p-3">{row.shares}</td>
        <td colSpan={4} className="p-3 text-center text-gray-400">
          <Loader2 className="animate-spin inline w-4 h-4" /> Fetching data...
        </td>
      </tr>
    );
  }

  return (
    <tr className="bg-white rounded shadow">
      <td className="p-3 font-medium">{row.ticker}</td>
      <td className="p-3">{row.shares}</td>
      <td className="p-3">{row.data?.ex_dividend_date || "-"}</td>
      <td className="p-3">{row.data?.payment_date || "-"}</td>
      <td className="p-3">
        {typeof row.data?.dividend_amount === "number"
          ? `$${row.data.dividend_amount.toFixed(2)}`
          : "-"}
      </td>
      <td className="p-3">
        {typeof row.data?.franking_percent === "number"
          ? `${row.data.franking_percent}%`
          : "-"}
      </td>
    </tr>
  );
}
