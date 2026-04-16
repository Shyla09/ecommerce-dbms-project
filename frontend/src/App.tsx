import { BrowserRouter, Routes, Route, Link, useLocation } from 'react-router-dom';
import { useContext, useState, useEffect } from 'react';
import { AuthContext } from './context/AuthContext';
import Home from './pages/Home';
import Cart from './pages/Cart';
import Auth from './pages/Auth';
import SellerDashboard from './pages/SellerDashboard';
import OrdersHistory from './pages/OrdersHistory';

function Navbar({ isDarkMode, toggleTheme }: { isDarkMode: boolean, toggleTheme: () => void }) {
  const { user, logout } = useContext(AuthContext);
  const location = useLocation();

  return (
    <nav className="sticky top-0 z-50 glass border-b border-gray-200 dark:border-white/5 px-6 py-4 transition-colors duration-300">
      <div className="container mx-auto flex justify-between items-center">
        <Link to="/" className="text-2xl font-extrabold tracking-tight text-gray-900 dark:text-white flex items-center gap-2 transition-colors duration-300">
           <div className="w-8 h-8 rounded-full bg-gradient-to-tr from-indigo-500 to-pink-500 flex items-center justify-center shadow-lg shadow-purple-500/30">
             <span className="text-white text-sm">S</span>
           </div>
           Shop<span className="text-transparent bg-clip-text bg-gradient-to-r from-purple-500 to-pink-500 dark:from-purple-400 dark:to-pink-500">Sphere</span>
        </Link>
        
        <div className="flex items-center gap-6">
          <button onClick={toggleTheme} className="text-xl p-2 rounded-full hover:bg-gray-200 dark:hover:bg-white/10 transition-colors" aria-label="Toggle Theme">
            {isDarkMode ? '☀️' : '🌙'}
          </button>
          <Link to="/" className={`text-sm font-medium transition-colors ${location.pathname === '/' ? 'text-gray-900 dark:text-white' : 'text-gray-500 hover:text-gray-900 dark:text-gray-400 dark:hover:text-white'}`}>Discover</Link>
          <Link to="/cart" className={`text-sm font-medium transition-colors ${location.pathname === '/cart' ? 'text-gray-900 dark:text-white' : 'text-gray-500 hover:text-gray-900 dark:text-gray-400 dark:hover:text-white'}`}>Cart</Link>
          
          {user ? (
            <div className="flex items-center gap-4 border-l border-gray-300 dark:border-white/10 pl-4 ml-2 transition-colors duration-300">
               <Link to="/history" className={`text-sm font-medium transition-colors ${location.pathname === '/history' ? 'text-gray-900 dark:text-white' : 'text-gray-500 hover:text-gray-900 dark:text-gray-400 dark:hover:text-white'}`}>
                 Orders
               </Link>
               <Link to="/seller" className={`text-sm font-medium transition-colors ${location.pathname === '/seller' ? 'text-purple-600 dark:text-purple-400' : 'text-gray-500 hover:text-purple-600 dark:text-gray-400 dark:hover:text-purple-400'}`}>
                 Seller Hub
               </Link>
               <button onClick={logout} className="text-sm font-medium text-red-500 hover:text-red-600 dark:text-red-400 dark:hover:text-red-300 transition-colors">Logout</button>
               <div className="w-8 h-8 rounded-full bg-gray-200 dark:bg-white/10 flex items-center justify-center border border-gray-300 dark:border-white/20 text-xs font-bold text-gray-800 dark:text-gray-200 transition-colors duration-300">
                 {user.first_name[0]}
               </div>
            </div>
          ) : (
             <div className="flex gap-3 ml-2">
                <Link to="/auth" className="btn-secondary text-sm px-5 py-2">Log In</Link>
             </div>
          )}
        </div>
      </div>
    </nav>
  );
}

function App() {
  // Default to dark mode to match previous styling
  const [isDarkMode, setIsDarkMode] = useState(true);

  useEffect(() => {
    if (isDarkMode) {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  }, [isDarkMode]);

  const toggleTheme = () => setIsDarkMode(!isDarkMode);

  return (
    <BrowserRouter>
      <div className="min-h-screen flex flex-col relative overflow-hidden bg-gray-50 dark:bg-transparent transition-colors duration-300">
        {/* Background ambient light */}
        <div className={`absolute top-0 left-1/2 -translate-x-1/2 w-[800px] h-[500px] ${isDarkMode ? 'bg-purple-600/20' : 'bg-purple-300/30'} blur-[120px] rounded-full pointer-events-none -z-10 transition-colors duration-500`}></div>
        <div className={`absolute top-1/2 left-0 w-[500px] h-[500px] ${isDarkMode ? 'bg-indigo-600/10' : 'bg-indigo-300/20'} blur-[120px] rounded-full pointer-events-none -z-10 transition-colors duration-500`}></div>
        
        <Navbar isDarkMode={isDarkMode} toggleTheme={toggleTheme} />
        <main className="container mx-auto p-6 flex-grow z-10 w-full relative">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/cart" element={<Cart />} />
            <Route path="/auth" element={<Auth />} />
            <Route path="/seller" element={<SellerDashboard />} />
            <Route path="/history" element={<OrdersHistory />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  );
}

export default App;
