import { useState } from "react";
import { Card, CardContent } from "components/ui/card";
import { Input } from "components/ui/input";
import { Button } from "components/ui/button";
import { Loader2 } from "lucide-react";


type RowData = {
  id: number;
  ticker: string;
  shares: string;
  loading: boolean;
  data: {
    ex_dividend_date: string | null;
    payment_date: string | null;
    dividend_amount: number | null;
    franking_percent: number | null;
  } | null;
};

export default function App() {
  const [rows, setRows] = useState<RowData[]>([]);
  const [ticker, setTicker] = useState("");
  const [shares, setShares] = useState("");

  const handleAddHolding = async () => {
    if (!ticker || !shares) return;
    const newRow = {
      id: Date.now(),
      ticker,
      shares,
      loading: true,
      data: null,
    };
    setRows([newRow, ...rows]);
    setTicker("");
    setShares("");

    try {
      const res = await fetch(`http://localhost:8000/dividends/fetch/${ticker}`);
      if (!res.ok) throw new Error(`HTTP error! status: ${res.status}`);
      const data = await res.json();

      setRows((prev) =>
        prev.map((row) =>
          row.id === newRow.id ? { ...row, loading: false, data } : row
        )
      );
    } catch (err) {
      console.error("Error fetching dividend info", err);
      setRows((prev) =>
        prev.map((row) =>
          row.id === newRow.id ? { ...row, loading: false, data: null } : row
        )
      );
    }
  };

  return (
    <main className="min-h-screen bg-gray-100 flex flex-col items-center p-6">
      <header className="w-full max-w-5xl mb-8">
        <h1 className="text-3xl font-bold text-gray-800">Divstream</h1>
      </header>

      <Card className="w-full max-w-5xl shadow-xl rounded-2xl">
        <CardContent className="p-6">
          <div className="grid grid-cols-4 gap-4 mb-6">
            <Input
              placeholder="ASX Ticker (e.g. CBA)"
              value={ticker}
              onChange={(e) => setTicker(e.target.value.toUpperCase())}
              className="col-span-2"
            />
            <Input
              placeholder="Shares"
              type="number"
              min={1}
              value={shares}
              onChange={(e) => setShares(e.target.value)}
            />
            <Button onClick={handleAddHolding}>Add</Button>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-left border-separate border-spacing-y-2">
              <thead>
                <tr className="text-sm text-gray-600">
                  <th>Ticker</th>
                  <th>Shares</th>
                  <th>Ex-Date</th>
                  <th>Pay Date</th>
                  <th>Dividend</th>
                  <th>Franking</th>
                </tr>
              </thead>
              <tbody>
                {rows.map((row) => (
                  <tr key={row.id} className="bg-white rounded shadow">
                    <td className="p-3 font-medium">{row.ticker}</td>
                    <td className="p-3">{row.shares}</td>
                    {row.loading ? (
                      <td colSpan={4} className="p-3 text-center text-gray-400">
                        <Loader2 className="animate-spin inline w-4 h-4" /> Fetching data...
                      </td>
                    ) : row.data ? (
                      <>
                        <td className="p-3">{row.data.ex_dividend_date || "-"}</td>
                        <td className="p-3">{row.data.payment_date || "-"}</td>
                        <td className="p-3">
                          {typeof row.data.dividend_amount === "number"
                            ? `$${row.data.dividend_amount.toFixed(2)}`
                            : "-"}
                        </td>
                        <td className="p-3">
                          {typeof row.data.franking_percent === "number"
                            ? `${row.data.franking_percent}%`
                            : "-"}
                        </td>
                      </>
                    ) : (
                      <td colSpan={4} className="p-3 text-red-500 text-center">
                        Error fetching data
                      </td>
                    )}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </CardContent>
      </Card>
    </main>
  );
}
