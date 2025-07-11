import { useState } from "react";
import Header from "components/Header";
import TickerInput from "components/TickerInput";
import HoldingsTable from "components/HoldingsTable";

interface DividendData {
  ex_dividend_date: string;
  payment_date: string;
  dividend_amount: number;
  franking_percent: number;
}

interface HoldingRow {
  id: number;
  ticker: string;
  shares: string;
  loading: boolean;
  data: DividendData | null;
}

export default function DividendTracker() {
  const [rows, setRows] = useState<HoldingRow[]>([]);
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
      <Header />
      <TickerInput
        ticker={ticker}
        shares={shares}
        setTicker={setTicker}
        setShares={setShares}
        onAdd={handleAddHolding}
      />
      <HoldingsTable rows={rows} />
    </main>
  );
}
