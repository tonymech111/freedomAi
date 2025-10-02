interface WhaleAlertProps {
  alert: {
    hash: string;
    value_ton: number;
    source: string;
    destination: string;
    severity: string;
  };
}

export default function WhaleAlert({ alert }: WhaleAlertProps) {
  return (
    <div className="p-4 rounded-lg bg-gradient-to-r from-purple-600/20 to-blue-600/20 border border-purple-500/50">
      <div className="flex items-center justify-between mb-2">
        <span className="text-2xl">🐋</span>
        <span className="text-xs px-2 py-1 rounded bg-purple-600 text-white">
          {alert.severity.toUpperCase()}
        </span>
      </div>
      <div className="text-xl font-bold text-white mb-2">
        {alert.value_ton.toLocaleString()} TON
      </div>
      <div className="text-sm text-gray-300 space-y-1">
        <div className="flex items-center gap-2">
          <span className="text-gray-400">From:</span>
          <span className="font-mono">{alert.source.slice(0, 12)}...</span>
        </div>
        <div className="flex items-center gap-2">
          <span className="text-gray-400">To:</span>
          <span className="font-mono">{alert.destination.slice(0, 12)}...</span>
        </div>
      </div>
    </div>
  );
}
