import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { ArrowRight, TrendingUp, Users, Shield, Zap, Award, ChevronDown, ExternalLink, Twitter, Send, Github } from 'lucide-react';

export default function Landing() {
  const navigate = useNavigate();
  const [activeTab, setActiveTab] = useState('creators');

  const metrics = [
    { label: 'Total Value Locked', value: '$2.4B', change: '+12.5%', trend: 'up' },
    { label: 'Active Creators', value: '15,234', change: '+8.2%', trend: 'up' },
    { label: 'Signals Generated', value: '1.2M+', change: '+24.1%', trend: 'up' },
    { label: 'Community Members', value: '250K+', change: '+15.7%', trend: 'up' },
  ];

  const leaderboard = [
    { rank: 1, name: 'CryptoSage', score: 98.5, signals: 1247, accuracy: '94.2%', avatar: '🏆' },
    { rank: 2, name: 'BlockchainPro', score: 96.8, signals: 1089, accuracy: '92.8%', avatar: '🥈' },
    { rank: 3, name: 'TONMaster', score: 95.2, signals: 987, accuracy: '91.5%', avatar: '🥉' },
    { rank: 4, name: 'DeFiWizard', score: 93.7, signals: 856, accuracy: '90.1%', avatar: '⭐' },
    { rank: 5, name: 'AlphaHunter', score: 92.1, signals: 743, accuracy: '89.3%', avatar: '💎' },
  ];

  const howItWorksSteps = [
    {
      icon: <Users className="w-8 h-8" />,
      title: 'Connect Your Wallet',
      description: 'Link your TON wallet to access the Freedom AI ecosystem and start your journey.',
    },
    {
      icon: <TrendingUp className="w-8 h-8" />,
      title: 'Discover Signals',
      description: 'Browse AI-powered trading signals from top-rated creators in the marketplace.',
    },
    {
      icon: <Award className="w-8 h-8" />,
      title: 'Build Reputation',
      description: 'Create and share signals to earn reputation points and TON rewards.',
    },
    {
      icon: <Zap className="w-8 h-8" />,
      title: 'Earn & Trade',
      description: 'Monetize your insights and trade with confidence using verified signals.',
    },
  ];

  const scrollToSection = (id: string) => {
    document.getElementById(id)?.scrollIntoView({ behavior: 'smooth' });
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-slate-950 via-slate-900 to-slate-950 text-white">
      {/* Navigation */}
      <nav className="fixed top-0 w-full bg-slate-950/80 backdrop-blur-lg border-b border-slate-800 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center space-x-2">
              <div className="w-10 h-10 bg-gradient-to-br from-blue-500 to-purple-600 rounded-lg flex items-center justify-center font-bold text-xl">
                FA
              </div>
              <span className="text-xl font-bold bg-gradient-to-r from-blue-400 to-purple-500 bg-clip-text text-transparent">
                Freedom AI
              </span>
            </div>
            <div className="hidden md:flex space-x-8">
              <button onClick={() => scrollToSection('about')} className="hover:text-blue-400 transition">About</button>
              <button onClick={() => scrollToSection('metrics')} className="hover:text-blue-400 transition">Metrics</button>
              <button onClick={() => scrollToSection('leaderboard')} className="hover:text-blue-400 transition">Leaderboard</button>
              <button onClick={() => scrollToSection('how-it-works')} className="hover:text-blue-400 transition">How It Works</button>
              <button onClick={() => scrollToSection('community')} className="hover:text-blue-400 transition">Community</button>
            </div>
            <button onClick={() => navigate('/app')} className="bg-gradient-to-r from-blue-500 to-purple-600 hover:from-blue-600 hover:to-purple-700 px-6 py-2 rounded-lg font-semibold transition">
              Launch App
            </button>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="pt-32 pb-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto text-center">
          <div className="inline-flex items-center space-x-2 bg-blue-500/10 border border-blue-500/20 rounded-full px-4 py-2 mb-8">
            <span className="w-2 h-2 bg-blue-500 rounded-full animate-pulse"></span>
            <span className="text-sm text-blue-400">Built on TON Blockchain</span>
          </div>
          <h1 className="text-5xl md:text-7xl font-bold mb-6 leading-tight">
            Decentralized Intelligence
            <br />
            <span className="bg-gradient-to-r from-blue-400 via-purple-500 to-pink-500 bg-clip-text text-transparent">
              Powered by Community
            </span>
          </h1>
          <p className="text-xl text-slate-400 mb-12 max-w-3xl mx-auto">
            Freedom AI is the first decentralized marketplace for AI-powered trading signals on TON blockchain. 
            Connect with top creators, share insights, and earn rewards for your expertise.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <button onClick={() => navigate('/app')} className="bg-gradient-to-r from-blue-500 to-purple-600 hover:from-blue-600 hover:to-purple-700 px-8 py-4 rounded-lg font-semibold text-lg flex items-center justify-center space-x-2 transition">
              <span>Get Started</span>
              <ArrowRight className="w-5 h-5" />
            </button>
            <button className="border border-slate-700 hover:border-slate-600 px-8 py-4 rounded-lg font-semibold text-lg transition">
              View Documentation
            </button>
          </div>
          <button 
            onClick={() => scrollToSection('about')}
            className="mt-16 animate-bounce text-slate-400 hover:text-white transition"
          >
            <ChevronDown className="w-8 h-8 mx-auto" />
          </button>
        </div>
      </section>

      {/* About Section */}
      <section id="about" className="py-20 px-4 sm:px-6 lg:px-8 bg-slate-900/50">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-4xl md:text-5xl font-bold mb-6">About Freedom AI</h2>
            <p className="text-xl text-slate-400 max-w-3xl mx-auto">
              A revolutionary platform that democratizes access to trading intelligence through blockchain technology
            </p>
          </div>
          <div className="grid md:grid-cols-3 gap-8">
            <div className="bg-slate-800/50 border border-slate-700 rounded-xl p-8 hover:border-blue-500/50 transition">
              <Shield className="w-12 h-12 text-blue-500 mb-4" />
              <h3 className="text-2xl font-bold mb-4">Trustless & Transparent</h3>
              <p className="text-slate-400">
                All signals and transactions are recorded on TON blockchain, ensuring complete transparency and immutability.
              </p>
            </div>
            <div className="bg-slate-800/50 border border-slate-700 rounded-xl p-8 hover:border-purple-500/50 transition">
              <Users className="w-12 h-12 text-purple-500 mb-4" />
              <h3 className="text-2xl font-bold mb-4">Community-Driven</h3>
              <p className="text-slate-400">
                Built by traders, for traders. Our reputation system ensures quality and rewards top contributors.
              </p>
            </div>
            <div className="bg-slate-800/50 border border-slate-700 rounded-xl p-8 hover:border-pink-500/50 transition">
              <Zap className="w-12 h-12 text-pink-500 mb-4" />
              <h3 className="text-2xl font-bold mb-4">AI-Powered Insights</h3>
              <p className="text-slate-400">
                Leverage cutting-edge AI algorithms combined with human expertise for superior trading signals.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Metrics Section */}
      <section id="metrics" className="py-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-4xl md:text-5xl font-bold mb-6">Platform Metrics</h2>
            <p className="text-xl text-slate-400">Real-time statistics from the Freedom AI ecosystem</p>
          </div>
          <div className="grid md:grid-cols-4 gap-6">
            {metrics.map((metric, index) => (
              <div key={index} className="bg-gradient-to-br from-slate-800 to-slate-900 border border-slate-700 rounded-xl p-6 hover:border-blue-500/50 transition">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-slate-400 text-sm">{metric.label}</span>
                  <span className={`text-xs ${metric.trend === 'up' ? 'text-green-400' : 'text-red-400'}`}>
                    {metric.change}
                  </span>
                </div>
                <div className="text-3xl font-bold mb-1">{metric.value}</div>
                <div className="h-1 bg-slate-700 rounded-full overflow-hidden">
                  <div className="h-full bg-gradient-to-r from-blue-500 to-purple-600 rounded-full" style={{ width: '75%' }}></div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Leaderboard Section */}
      <section id="leaderboard" className="py-20 px-4 sm:px-6 lg:px-8 bg-slate-900/50">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-4xl md:text-5xl font-bold mb-6">Top Creators</h2>
            <p className="text-xl text-slate-400">Leading signal providers ranked by performance and reputation</p>
          </div>
          <div className="bg-slate-800/50 border border-slate-700 rounded-xl overflow-hidden">
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead className="bg-slate-900/50">
                  <tr>
                    <th className="px-6 py-4 text-left text-sm font-semibold text-slate-400">Rank</th>
                    <th className="px-6 py-4 text-left text-sm font-semibold text-slate-400">Creator</th>
                    <th className="px-6 py-4 text-left text-sm font-semibold text-slate-400">Score</th>
                    <th className="px-6 py-4 text-left text-sm font-semibold text-slate-400">Signals</th>
                    <th className="px-6 py-4 text-left text-sm font-semibold text-slate-400">Accuracy</th>
                  </tr>
                </thead>
                <tbody>
                  {leaderboard.map((creator) => (
                    <tr key={creator.rank} className="border-t border-slate-700 hover:bg-slate-800/50 transition">
                      <td className="px-6 py-4">
                        <span className="text-2xl">{creator.avatar}</span>
                      </td>
                      <td className="px-6 py-4">
                        <div className="font-semibold">{creator.name}</div>
                      </td>
                      <td className="px-6 py-4">
                        <div className="flex items-center space-x-2">
                          <div className="text-lg font-bold text-blue-400">{creator.score}</div>
                        </div>
                      </td>
                      <td className="px-6 py-4 text-slate-400">{creator.signals}</td>
                      <td className="px-6 py-4">
                        <span className="text-green-400 font-semibold">{creator.accuracy}</span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </section>

      {/* How It Works Section */}
      <section id="how-it-works" className="py-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-4xl md:text-5xl font-bold mb-6">How It Works</h2>
            <p className="text-xl text-slate-400">Get started in four simple steps</p>
          </div>
          <div className="grid md:grid-cols-4 gap-8">
            {howItWorksSteps.map((step, index) => (
              <div key={index} className="relative">
                <div className="bg-gradient-to-br from-slate-800 to-slate-900 border border-slate-700 rounded-xl p-8 hover:border-blue-500/50 transition">
                  <div className="bg-gradient-to-br from-blue-500 to-purple-600 w-16 h-16 rounded-xl flex items-center justify-center mb-6 text-white">
                    {step.icon}
                  </div>
                  <div className="absolute -top-4 -right-4 w-12 h-12 bg-blue-500 rounded-full flex items-center justify-center font-bold text-xl">
                    {index + 1}
                  </div>
                  <h3 className="text-xl font-bold mb-4">{step.title}</h3>
                  <p className="text-slate-400">{step.description}</p>
                </div>
                {index < howItWorksSteps.length - 1 && (
                  <div className="hidden md:block absolute top-1/2 -right-4 w-8 h-0.5 bg-gradient-to-r from-blue-500 to-purple-600"></div>
                )}
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Community & Creator Section */}
      <section id="community" className="py-20 px-4 sm:px-6 lg:px-8 bg-slate-900/50">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-4xl md:text-5xl font-bold mb-6">Join the Community</h2>
            <p className="text-xl text-slate-400">Connect with creators and traders worldwide</p>
          </div>
          
          <div className="flex justify-center space-x-4 mb-12">
            <button
              onClick={() => setActiveTab('creators')}
              className={`px-6 py-3 rounded-lg font-semibold transition ${
                activeTab === 'creators'
                  ? 'bg-gradient-to-r from-blue-500 to-purple-600'
                  : 'bg-slate-800 hover:bg-slate-700'
              }`}
            >
              For Creators
            </button>
            <button
              onClick={() => setActiveTab('traders')}
              className={`px-6 py-3 rounded-lg font-semibold transition ${
                activeTab === 'traders'
                  ? 'bg-gradient-to-r from-blue-500 to-purple-600'
                  : 'bg-slate-800 hover:bg-slate-700'
              }`}
            >
              For Traders
            </button>
          </div>

          <div className="grid md:grid-cols-2 gap-8">
            {activeTab === 'creators' ? (
              <>
                <div className="bg-slate-800/50 border border-slate-700 rounded-xl p-8">
                  <Award className="w-12 h-12 text-yellow-500 mb-4" />
                  <h3 className="text-2xl font-bold mb-4">Monetize Your Expertise</h3>
                  <p className="text-slate-400 mb-4">
                    Share your trading signals and earn TON tokens based on performance. Build your reputation and grow your following.
                  </p>
                  <ul className="space-y-2 text-slate-400">
                    <li className="flex items-center space-x-2">
                      <div className="w-1.5 h-1.5 bg-blue-500 rounded-full"></div>
                      <span>Earn up to 80% revenue share</span>
                    </li>
                    <li className="flex items-center space-x-2">
                      <div className="w-1.5 h-1.5 bg-blue-500 rounded-full"></div>
                      <span>Build verifiable track record</span>
                    </li>
                    <li className="flex items-center space-x-2">
                      <div className="w-1.5 h-1.5 bg-blue-500 rounded-full"></div>
                      <span>Access creator tools & analytics</span>
                    </li>
                  </ul>
                </div>
                <div className="bg-slate-800/50 border border-slate-700 rounded-xl p-8">
                  <TrendingUp className="w-12 h-12 text-green-500 mb-4" />
                  <h3 className="text-2xl font-bold mb-4">Grow Your Influence</h3>
                  <p className="text-slate-400 mb-4">
                    Leverage our platform to reach thousands of traders and establish yourself as a thought leader.
                  </p>
                  <ul className="space-y-2 text-slate-400">
                    <li className="flex items-center space-x-2">
                      <div className="w-1.5 h-1.5 bg-purple-500 rounded-full"></div>
                      <span>Direct access to 250K+ traders</span>
                    </li>
                    <li className="flex items-center space-x-2">
                      <div className="w-1.5 h-1.5 bg-purple-500 rounded-full"></div>
                      <span>Reputation-based ranking system</span>
                    </li>
                    <li className="flex items-center space-x-2">
                      <div className="w-1.5 h-1.5 bg-purple-500 rounded-full"></div>
                      <span>Community engagement tools</span>
                    </li>
                  </ul>
                </div>
              </>
            ) : (
              <>
                <div className="bg-slate-800/50 border border-slate-700 rounded-xl p-8">
                  <Shield className="w-12 h-12 text-blue-500 mb-4" />
                  <h3 className="text-2xl font-bold mb-4">Trade with Confidence</h3>
                  <p className="text-slate-400 mb-4">
                    Access verified signals from top-rated creators. All performance metrics are transparent and on-chain.
                  </p>
                  <ul className="space-y-2 text-slate-400">
                    <li className="flex items-center space-x-2">
                      <div className="w-1.5 h-1.5 bg-blue-500 rounded-full"></div>
                      <span>Verified creator track records</span>
                    </li>
                    <li className="flex items-center space-x-2">
                      <div className="w-1.5 h-1.5 bg-blue-500 rounded-full"></div>
                      <span>Real-time signal notifications</span>
                    </li>
                    <li className="flex items-center space-x-2">
                      <div className="w-1.5 h-1.5 bg-blue-500 rounded-full"></div>
                      <span>Risk management tools</span>
                    </li>
                  </ul>
                </div>
                <div className="bg-slate-800/50 border border-slate-700 rounded-xl p-8">
                  <Zap className="w-12 h-12 text-purple-500 mb-4" />
                  <h3 className="text-2xl font-bold mb-4">Discover Alpha</h3>
                  <p className="text-slate-400 mb-4">
                    Find hidden gems and trending opportunities curated by expert traders and AI algorithms.
                  </p>
                  <ul className="space-y-2 text-slate-400">
                    <li className="flex items-center space-x-2">
                      <div className="w-1.5 h-1.5 bg-purple-500 rounded-full"></div>
                      <span>AI-powered signal filtering</span>
                    </li>
                    <li className="flex items-center space-x-2">
                      <div className="w-1.5 h-1.5 bg-purple-500 rounded-full"></div>
                      <span>Personalized recommendations</span>
                    </li>
                    <li className="flex items-center space-x-2">
                      <div className="w-1.5 h-1.5 bg-purple-500 rounded-full"></div>
                      <span>Portfolio tracking & analytics</span>
                    </li>
                  </ul>
                </div>
              </>
            )}
          </div>

          <div className="mt-16 text-center">
            <h3 className="text-2xl font-bold mb-8">Connect With Us</h3>
            <div className="flex justify-center space-x-6">
              <a href="#" className="w-12 h-12 bg-slate-800 hover:bg-blue-500 rounded-lg flex items-center justify-center transition">
                <Twitter className="w-6 h-6" />
              </a>
              <a href="#" className="w-12 h-12 bg-slate-800 hover:bg-blue-500 rounded-lg flex items-center justify-center transition">
                <Send className="w-6 h-6" />
              </a>
              <a href="#" className="w-12 h-12 bg-slate-800 hover:bg-blue-500 rounded-lg flex items-center justify-center transition">
                <Github className="w-6 h-6" />
              </a>
              <a href="#" className="w-12 h-12 bg-slate-800 hover:bg-blue-500 rounded-lg flex items-center justify-center transition">
                <ExternalLink className="w-6 h-6" />
              </a>
            </div>
          </div>
        </div>
      </section>

      {/* Disclaimer Section */}
      <section className="py-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-4xl mx-auto">
          <div className="bg-slate-800/50 border border-yellow-500/30 rounded-xl p-8">
            <div className="flex items-start space-x-4">
              <div className="flex-shrink-0">
                <div className="w-12 h-12 bg-yellow-500/20 rounded-lg flex items-center justify-center">
                  <Shield className="w-6 h-6 text-yellow-500" />
                </div>
              </div>
              <div>
                <h3 className="text-2xl font-bold mb-4 text-yellow-500">Important Disclaimer</h3>
                <div className="space-y-3 text-slate-400">
                  <p>
                    <strong className="text-white">Risk Warning:</strong> Trading cryptocurrencies involves substantial risk and may result in the loss of your invested capital. You should not invest more than you can afford to lose.
                  </p>
                  <p>
                    <strong className="text-white">Not Financial Advice:</strong> The signals and information provided on Freedom AI are for informational purposes only and should not be considered as financial advice. Always conduct your own research (DYOR) before making investment decisions.
                  </p>
                  <p>
                    <strong className="text-white">Performance Disclaimer:</strong> Past performance is not indicative of future results. Signal accuracy rates are historical and do not guarantee future performance.
                  </p>
                  <p>
                    <strong className="text-white">Regulatory Compliance:</strong> Users are responsible for complying with their local laws and regulations regarding cryptocurrency trading and taxation.
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Call-to-Action Section */}
      <section className="py-20 px-4 sm:px-6 lg:px-8 bg-gradient-to-r from-blue-900/20 to-purple-900/20">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-4xl md:text-5xl font-bold mb-6">
            Ready to Start Your Journey?
          </h2>
          <p className="text-xl text-slate-400 mb-12">
            Join thousands of traders and creators building the future of decentralized intelligence on TON blockchain.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <button onClick={() => navigate('/app')} className="bg-gradient-to-r from-blue-500 to-purple-600 hover:from-blue-600 hover:to-purple-700 px-10 py-5 rounded-lg font-semibold text-lg flex items-center justify-center space-x-2 transition">
              <span>Launch App Now</span>
              <ArrowRight className="w-5 h-5" />
            </button>
            <button className="border border-slate-700 hover:border-slate-600 px-10 py-5 rounded-lg font-semibold text-lg transition">
              Read Documentation
            </button>
          </div>
          <div className="mt-12 flex items-center justify-center space-x-8 text-sm text-slate-500">
            <div className="flex items-center space-x-2">
              <div className="w-2 h-2 bg-green-500 rounded-full"></div>
              <span>All systems operational</span>
            </div>
            <div className="flex items-center space-x-2">
              <Shield className="w-4 h-4" />
              <span>Audited by CertiK</span>
            </div>
            <div className="flex items-center space-x-2">
              <Users className="w-4 h-4" />
              <span>250K+ users</span>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-slate-800 py-12 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          <div className="grid md:grid-cols-4 gap-8 mb-8">
            <div>
              <div className="flex items-center space-x-2 mb-4">
                <div className="w-10 h-10 bg-gradient-to-br from-blue-500 to-purple-600 rounded-lg flex items-center justify-center font-bold text-xl">
                  FA
                </div>
                <span className="text-xl font-bold">Freedom AI</span>
              </div>
              <p className="text-slate-400 text-sm">
                Decentralized intelligence marketplace built on TON blockchain.
              </p>
            </div>
            <div>
              <h4 className="font-semibold mb-4">Product</h4>
              <ul className="space-y-2 text-slate-400 text-sm">
                <li><a href="#" className="hover:text-white transition">Marketplace</a></li>
                <li><a href="#" className="hover:text-white transition">Signals</a></li>
                <li><a href="#" className="hover:text-white transition">Analytics</a></li>
                <li><a href="#" className="hover:text-white transition">Reputation</a></li>
              </ul>
            </div>
            <div>
              <h4 className="font-semibold mb-4">Resources</h4>
              <ul className="space-y-2 text-slate-400 text-sm">
                <li><a href="#" className="hover:text-white transition">Documentation</a></li>
                <li><a href="#" className="hover:text-white transition">API</a></li>
                <li><a href="#" className="hover:text-white transition">Blog</a></li>
                <li><a href="#" className="hover:text-white transition">Support</a></li>
              </ul>
            </div>
            <div>
              <h4 className="font-semibold mb-4">Legal</h4>
              <ul className="space-y-2 text-slate-400 text-sm">
                <li><a href="#" className="hover:text-white transition">Terms of Service</a></li>
                <li><a href="#" className="hover:text-white transition">Privacy Policy</a></li>
                <li><a href="#" className="hover:text-white transition">Cookie Policy</a></li>
                <li><a href="#" className="hover:text-white transition">Disclaimer</a></li>
              </ul>
            </div>
          </div>
          <div className="border-t border-slate-800 pt-8 flex flex-col md:flex-row justify-between items-center">
            <p className="text-slate-400 text-sm">© 2025 Freedom AI. All rights reserved.</p>
            <div className="flex items-center space-x-4 mt-4 md:mt-0">
              <span className="text-slate-400 text-sm">Powered by</span>
              <div className="flex items-center space-x-2 text-blue-400 font-semibold">
                <div className="w-6 h-6 bg-blue-500 rounded-full"></div>
                <span>TON</span>
              </div>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}
