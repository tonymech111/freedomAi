import { useQuery } from '@tanstack/react-query';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';
import { api } from '../lib/api';

export default function Reputation() {
  const { data: leaderboard } = useQuery({
    queryKey: ['leaderboard'],
    queryFn: () => api.getLeaderboard({ limit: 50 }),
  });

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-white">Reputation</h1>
        <p className="text-gray-400">Top signal creators and their rankings</p>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Leaderboard</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {leaderboard?.leaderboard?.map((creator: any) => (
              <div
                key={creator.address}
                className="flex items-center justify-between p-4 rounded-lg bg-gray-700/30 border border-gray-600"
              >
                <div className="flex items-center gap-4">
                  <div className="w-10 h-10 rounded-full bg-gradient-to-r from-blue-600 to-purple-600 flex items-center justify-center text-white font-bold">
                    #{creator.rank}
                  </div>
                  <div>
                    <div className="font-mono text-white">{creator.address}</div>
                    <div className="text-sm text-gray-400">
                      {creator.total_signals} signals • {Math.round(creator.accuracy * 100)}% accuracy
                    </div>
                  </div>
                </div>
                <div className="text-right">
                  <div className="text-2xl font-bold text-white">{creator.reputation_score}</div>
                  <div className="text-xs text-gray-400">reputation</div>
                </div>
              </div>
            )) || (
              <p className="text-gray-400 text-center py-8">No data available</p>
            )}
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
