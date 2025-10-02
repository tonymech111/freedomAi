import { useQuery } from '@tanstack/react-query';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';
import { api } from '../lib/api';

export default function Marketplace() {
  const { data: assets } = useQuery({
    queryKey: ['marketplace-assets'],
    queryFn: () => api.browseMarketplace({ limit: 20 }),
  });

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-white">Marketplace</h1>
        <p className="text-gray-400">Browse and purchase tokenized intelligence</p>
      </div>

      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
        {assets?.assets?.map((asset: any) => (
          <Card key={asset.id} className="hover:border-blue-500 transition-colors cursor-pointer">
            <CardHeader>
              <div className="flex items-start justify-between">
                <CardTitle className="text-lg">{asset.title}</CardTitle>
                <span className="text-xs px-2 py-1 rounded bg-blue-600 text-white">
                  {asset.type.toUpperCase()}
                </span>
              </div>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-gray-400 mb-4">{asset.description}</p>
              <div className="flex items-center justify-between">
                <span className="text-2xl font-bold text-white">{asset.price} TON</span>
                <div className="text-right">
                  <div className="text-sm text-yellow-500">★ {asset.rating}</div>
                  <div className="text-xs text-gray-400">{asset.purchases} sales</div>
                </div>
              </div>
            </CardContent>
          </Card>
        )) || (
          <div className="col-span-3 text-center text-gray-400 py-12">
            No assets available
          </div>
        )}
      </div>
    </div>
  );
}
