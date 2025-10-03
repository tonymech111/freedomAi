interface SignalCardProps {
  signal: {
    id: string;
    signal_type: string;
    title: string;
    description: string;
    confidence: number;
    severity: string;
    tags: string[];
  };
}

export default function SignalCard({ signal }: SignalCardProps) {
  const severityColors = {
    high: 'bg-red-500',
    medium: 'bg-yellow-500',
    low: 'bg-green-500',
  };

  return (
    <div className="p-4 rounded-lg bg-gray-700/30 border border-gray-600 hover:border-blue-500 transition-colors">
      <div className="flex items-start justify-between mb-2">
        <span className="text-xs px-2 py-1 rounded bg-blue-600 text-white">
          {signal.signal_type.replace('_', ' ').toUpperCase()}
        </span>
        <div className="flex items-center gap-2">
          <span className={`w-2 h-2 rounded-full ${severityColors[signal.severity as keyof typeof severityColors]}`} />
          <span className="text-xs text-gray-400">{Math.round(signal.confidence * 100)}%</span>
        </div>
      </div>
      <h4 className="font-semibold text-white mb-1">{signal.title}</h4>
      <p className="text-sm text-gray-400 mb-3">{signal.description}</p>
      <div className="flex gap-2 flex-wrap">
        {signal.tags.map((tag) => (
          <span key={tag} className="text-xs px-2 py-1 rounded-full bg-gray-600 text-gray-300">
            #{tag}
          </span>
        ))}
      </div>
    </div>
  );
}
