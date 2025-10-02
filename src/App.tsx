import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { Toaster } from './components/ui/toaster';
import Layout from './components/Layout';
import Landing from './pages/Landing';
import Dashboard from './pages/Dashboard';
import Marketplace from './pages/Marketplace';
import Signals from './pages/Signals';
import Analytics from './pages/Analytics';
import Reputation from './pages/Reputation';
import './App.css';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 1,
    },
  },
});

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <Router>
        <Routes>
          {/* Landing page without Layout */}
          <Route path="/" element={<Landing />} />
          
          {/* App routes with Layout */}
          <Route path="/app" element={<Layout><Dashboard /></Layout>} />
          <Route path="/app/marketplace" element={<Layout><Marketplace /></Layout>} />
          <Route path="/app/signals" element={<Layout><Signals /></Layout>} />
          <Route path="/app/analytics" element={<Layout><Analytics /></Layout>} />
          <Route path="/app/reputation" element={<Layout><Reputation /></Layout>} />
        </Routes>
      </Router>
      <Toaster />
    </QueryClientProvider>
  );
}

export default App;
