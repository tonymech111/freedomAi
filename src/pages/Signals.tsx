import { useQuery } from '@tanstack/react-query';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';
import { api } from '../lib/api';
import SignalCard from '../components/SignalCard';

export default function Signals() {
  const { data: signals } = useQuery({
    queryKey: ['all-signals'],
    queryFn: () => api.getRecentSignals({ limit: 50 }),
  });

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-white">AI Signals</h1>
        <p className="text-gray-400">Real-time trading signals powered by AI</p>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>All Signals</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          {signals?.signals?.map((signal: any) => (
            <SignalCard key={signal.id} signal={signal} />
          )) || (
            <p className="text-gray-400 text-center py-8">No signals available</p>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
