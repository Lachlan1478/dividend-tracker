import { Input } from "./ui/input";
import { Button } from "./ui/button";

interface TickerInputProps {
  ticker: string;
  shares: string;
  setTicker: (ticker: string) => void;
  setShares: (shares: string) => void;
  onAdd: () => void;
}

export default function TickerInput({
  ticker,
  shares,
  setTicker,
  setShares,
  onAdd,
}: TickerInputProps) {
  return (
    <div className="bg-white p-4 rounded shadow mb-6 w-full max-w-4xl grid grid-cols-5 gap-4 items-end">
      <Input
        placeholder="ASX Ticker (e.g. CBA)"
        value={ticker}
        onChange={(e) => setTicker(e.target.value.toUpperCase())}
        className="col-span-2"
      />
      <Input
        type="number"
        placeholder="Shares"
        min={1}
        value={shares}
        onChange={(e) => setShares(e.target.value)}
        className="col-span-2"
      />
      <Button onClick={onAdd} className="w-full">
        Add
      </Button>
    </div>
  );
}
