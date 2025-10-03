import { ReactNode } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Home, TrendingUp, ShoppingBag, BarChart3, Award } from 'lucide-react';

interface LayoutProps {
  children: ReactNode;
}

export default function Layout({ children }: LayoutProps) {
  const location = useLocation();

  const navItems = [
    { path: '/', label: 'Dashboard', icon: Home },
    { path: '/signals', label: 'Signals', icon: TrendingUp },
    { path: '/marketplace', label: 'Marketplace', icon: ShoppingBag },
    { path: '/analytics', label: 'Analytics', icon: BarChart3 },
    { path: '/reputation', label: 'Reputation', icon: Award },
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900">
      {/* Sidebar */}
      <aside className="fixed left-0 top-0 h-full w-64 bg-gray-800/50 backdrop-blur-lg border-r border-gray-700">
        <div className="p-6">
          <h1 className="text-2xl font-bold text-white mb-8">🔮 InfoFi</h1>
          <nav className="space-y-2">
            {navItems.map((item) => {
              const Icon = item.icon;
              const isActive = location.pathname === item.path;
              return (
                <Link
                  key={item.path}
                  to={item.path}
                  className={`flex items-center gap-3 px-4 py-3 rounded-lg transition-colors ${
                    isActive
                      ? 'bg-blue-600 text-white'
                      : 'text-gray-300 hover:bg-gray-700/50'
                  }`}
                >
                  <Icon className="w-5 h-5" />
                  <span>{item.label}</span>
                </Link>
              );
            })}
          </nav>
        </div>
      </aside>

      {/* Main Content */}
      <main className="ml-64 p-8">
        <div className="max-w-7xl mx-auto">
          {children}
        </div>
      </main>
    </div>
  );
}
