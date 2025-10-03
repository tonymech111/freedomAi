import { useQuery } from '@tanstack/react-query';
import { TrendingUp, Activity, DollarSign, Users } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';
import { api } from '../lib/api';
import SignalCard from '../components/SignalCard';
import WhaleAlert from '../components/WhaleAlert';

export default function Dashboard() {
  const { data: signals } = useQuery({
    queryKey: ['recent-signals'],
    queryFn: () => api.getRecentSignals({ limit: 5 }),
  });

  const { data: whaleAlerts } = useQuery({
    queryKey: ['whale-alerts'],
    queryFn: () => api.getWhaleAlerts({ hours: 24 }),
  });

  const stats = [
    {
      title: 'Market Sentiment',
      value: 'Bullish',
      change: '+12%',
      icon: TrendingUp,
      color: 'text-green-500',
    },
    {
      title: 'Active Signals',
      value: '247',
      change: '+8',
      icon: Activity,
      color: 'text-blue-500',
    },
    {
      title: 'Total Volume',
      value: '12.4M TON',
      change: '+23%',
      icon: DollarSign,
      color: 'text-purple-500',
    },
    {
      title: 'Active Creators',
      value: '1,234',
      change: '+156',
      icon: Users,
      color: 'text-orange-500',
    },
  ];

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold">Dashboard</h1>
        <p className="text-muted-foreground">
          AI-powered DeFi intelligence at your fingertips
        </p>
      </div>

      {/* Stats Grid */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        {stats.map((stat) => {
          const Icon = stat.icon;
          return (
            <Card key={stat.title}>
              <CardHeader className="flex flex-row items-center justify-between pb-2">
                <CardTitle className="text-sm font-medium">
                  {stat.title}
                </CardTitle>
                <Icon className={`h-4 w-4 ${stat.color}`} />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">{stat.value}</div>
                <p className="text-xs text-muted-foreground">
                  {stat.change} from last week
                </p>
              </CardContent>
            </Card>
          );
        })}
      </div>

      {/* Main Content Grid */}
      <div className="grid gap-6 lg:grid-cols-2">
        {/* Recent Signals */}
        <Card>
          <CardHeader>
            <CardTitle>Recent Signals</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            {signals?.signals?.map((signal: any) => (
              <SignalCard key={signal.id} signal={signal} />
            )) || (
              <p className="text-sm text-muted-foreground">
                No recent signals available
              </p>
            )}
          </CardContent>
        </Card>

        {/* Whale Alerts */}
        <Card>
          <CardHeader>
            <CardTitle>🐋 Whale Alerts</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            {whaleAlerts?.alerts?.map((alert: any) => (
              <WhaleAlert key={alert.hash} alert={alert} />
            )) || (
              <p className="text-sm text-muted-foreground">
                No whale alerts in the last 24 hours
              </p>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
