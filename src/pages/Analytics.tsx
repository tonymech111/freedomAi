import { useQuery } from '@tanstack/react-query';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';
import { api } from '../lib/api';

export default function Analytics() {
  const { data: marketAnalysis } = useQuery({
    queryKey: ['market-analysis'],
    queryFn: () => api.analyzeMarket(),
  });

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-white">Analytics</h1>
        <p className="text-gray-400">Deep market insights and analysis</p>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Market Analysis</CardTitle>
        </CardHeader>
        <CardContent>
          {marketAnalysis ? (
            <div className="space-y-4">
              <div>
                <h3 className="text-lg font-semibold text-white mb-2">Market Sentiment</h3>
                <div className="flex items-center gap-4">
                  <span className="text-3xl font-bold text-green-500">
                    {marketAnalysis.market_sentiment.toUpperCase()}
                  </span>
                  <span className="text-gray-400">
                    {Math.round(marketAnalysis.confidence * 100)}% confidence
                  </span>
                </div>
              </div>

              <div>
                <h3 className="text-lg font-semibold text-white mb-2">Key Insights</h3>
                <ul className="space-y-2">
                  {marketAnalysis.key_insights?.map((insight: string, i: number) => (
                    <li key={i} className="text-gray-300 flex items-start gap-2">
                      <span className="text-blue-500">•</span>
                      {insight}
                    </li>
                  ))}
                </ul>
              </div>

              <div>
                <h3 className="text-lg font-semibold text-white mb-2">Recommendations</h3>
                <ul className="space-y-2">
                  {marketAnalysis.recommendations?.map((rec: string, i: number) => (
                    <li key={i} className="text-gray-300 flex items-start gap-2">
                      <span className="text-green-500">✓</span>
                      {rec}
                    </li>
                  ))}
                </ul>
              </div>

              <div>
                <h3 className="text-lg font-semibold text-white mb-2">Risk Level</h3>
                <span className={`px-4 py-2 rounded-full ${
                  marketAnalysis.risk_level === 'low' ? 'bg-green-600' :
                  marketAnalysis.risk_level === 'medium' ? 'bg-yellow-600' :
                  'bg-red-600'
                } text-white`}>
                  {marketAnalysis.risk_level.toUpperCase()}
                </span>
              </div>
            </div>
          ) : (
            <p className="text-gray-400">Loading analysis...</p>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
