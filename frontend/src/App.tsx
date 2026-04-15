import { BrowserRouter, Routes, Route, Link, useLocation } from 'react-router-dom';
import { useContext } from 'react';
import { AuthContext } from './context/AuthContext';
import Home from './pages/Home';
import Cart from './pages/Cart';
import Auth from './pages/Auth';
import SellerDashboard from './pages/SellerDashboard';

function Navbar() {
  const { user, logout } = useContext(AuthContext);
  const location = useLocation();

  return (
    <nav className="sticky top-0 z-50 glass border-b border-white/5 px-6 py-4">
      <div className="container mx-auto flex justify-between items-center">
        <Link to="/" className="text-2xl font-extrabold tracking-tight text-white flex items-center gap-2">
           <div className="w-8 h-8 rounded-full bg-gradient-to-tr from-indigo-500 to-pink-500 flex items-center justify-center shadow-lg shadow-purple-500/30">
             <span className="text-white text-sm">S</span>
           </div>
           Shop<span className="text-transparent bg-clip-text bg-gradient-to-r from-purple-400 to-pink-500">Sphere</span>
        </Link>
        
        <div className="flex items-center gap-6">
          <Link to="/" className={`text-sm font-medium transition-colors ${location.pathname === '/' ? 'text-white' : 'text-gray-400 hover:text-white'}`}>Discover</Link>
          <Link to="/cart" className={`text-sm font-medium transition-colors ${location.pathname === '/cart' ? 'text-white' : 'text-gray-400 hover:text-white'}`}>Cart</Link>
          
          {user ? (
            <div className="flex items-center gap-4 border-l border-white/10 pl-4 ml-2">
               <Link to="/seller" className={`text-sm font-medium transition-colors ${location.pathname === '/seller' ? 'text-purple-400' : 'text-gray-400 hover:text-purple-400'}`}>
                 Seller Hub
               </Link>
               <button onClick={logout} className="text-sm font-medium text-red-400 hover:text-red-300 transition">Logout</button>
               <div className="w-8 h-8 rounded-full bg-white/10 flex items-center justify-center border border-white/20 text-xs font-bold">
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
  return (
    <BrowserRouter>
      <div className="min-h-screen flex flex-col relative overflow-hidden">
        {/* Background ambient light */}
        <div className="absolute top-0 left-1/2 -translate-x-1/2 w-[800px] h-[500px] bg-purple-600/20 blur-[120px] rounded-full pointer-events-none -z-10"></div>
        <div className="absolute top-1/2 left-0 w-[500px] h-[500px] bg-indigo-600/10 blur-[120px] rounded-full pointer-events-none -z-10"></div>
        
        <Navbar />
        <main className="container mx-auto p-6 flex-grow z-10 w-full relative">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/cart" element={<Cart />} />
            <Route path="/auth" element={<Auth />} />
            <Route path="/seller" element={<SellerDashboard />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  );
}

export default App;
