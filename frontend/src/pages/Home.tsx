import { useEffect, useState, useContext } from 'react';
import api from '../api/axios';
import { AuthContext } from '../context/AuthContext';

export default function Home() {
  const [products, setProducts] = useState<any[]>([]);
  const { user } = useContext(AuthContext);

  useEffect(() => {
    api.get('/products').then(res => setProducts(res.data)).catch(console.error);
  }, []);

  const addToCart = async (p_id: number) => {
    try {
      await api.post('/cart/add', { p_id, quantity: 1 });
      alert('Added to cart!');
    } catch {
      alert('Please login first to add to cart!');
    }
  };

  return (
    <div className="py-8 animate-in fade-in duration-700">
      <div className="flex justify-between items-end mb-10">
         <div>
            <h1 className="text-5xl font-extrabold mb-2 bg-clip-text text-transparent bg-gradient-to-r from-gray-100 to-gray-500">
              Trending Drops
            </h1>
            <p className="text-gray-400 text-lg max-w-xl">
              Curated goods matching today's lifestyle. Minimal. Impactful.
            </p>
         </div>
      </div>
      
      {products.length === 0 ? (
         <div className="flex flex-col items-center justify-center py-32 glass-card rounded-3xl mt-10">
            <span className="text-4xl mb-4">🛍️</span>
            <h2 className="text-2xl font-bold text-white mb-2">The store is completely empty!</h2>
            <p className="text-gray-400 mb-6">Nobody line-up any drops yet. Register as a seller and add the first product!</p>
            <a href="/seller" className="btn-primary">Become a Seller</a>
         </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {products.map((p, index) => (
            <div 
              key={p.p_id} 
              className="glass-card rounded-[2rem] overflow-hidden group hover:-translate-y-2"
              style={{ animationDelay: `${index * 100}ms` }}
            >
              <div className="h-64 overflow-hidden relative bg-black/40">
                 {p.p_image_url ? (
                   <img src={p.p_image_url} alt={p.p_name} className="w-full h-full object-cover opacity-90 group-hover:opacity-100 group-hover:scale-105 transition-all duration-700 ease-out" />
                 ) : (
                   <div className="w-full h-full bg-gradient-to-br from-indigo-900 via-purple-900 to-black group-hover:scale-105 transition-all duration-700 ease-out flex items-center justify-center">
                     <span className="text-4xl text-white/50">✦</span>
                   </div>
                 )}
                 <div className="absolute top-4 right-4 bg-black/50 backdrop-blur-md px-3 py-1 rounded-full border border-white/10 text-xs font-bold tracking-wider text-pink-300">
                   NEW
                 </div>
              </div>
              
              <div className="p-6">
                <div className="flex justify-between items-start mb-3">
                  <h2 className="text-xl font-bold text-white leading-tight">{p.p_name}</h2>
                  <span className="text-xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-purple-400 to-pink-400 ml-4">${p.p_price}</span>
                </div>
                <p className="text-gray-400 text-sm mb-6 line-clamp-2 h-10">{p.p_description}</p>
                
                <div className="flex justify-between items-center">
                  <span className="text-xs text-gray-500 font-medium tracking-wide shadow-inner px-3 py-1 bg-white/5 rounded-full border border-white/5 uppercase">
                    Stock: {p.p_stock}
                  </span>
                  <button 
                    onClick={() => addToCart(p.p_id)}
                    className="relative overflow-hidden group/btn bg-white/10 hover:bg-white/20 border border-white/20 text-white font-semibold py-2 px-6 rounded-full transition-all duration-300 active:scale-95"
                  >
                    <span className="relative z-10">Add to Cart</span>
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
