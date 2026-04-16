import { useState, useEffect, useContext } from 'react';
import { AuthContext } from '../context/AuthContext';
import api from '../api/axios';
import { Navigate } from 'react-router-dom';

export default function OrdersHistory() {
  const { user } = useContext(AuthContext);
  const [history, setHistory] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (user) {
      api.get('/orders/detailed-history')
        .then(res => {
          setHistory(res.data.history || []);
          setLoading(false);
        })
        .catch(err => {
          console.error(err);
          setLoading(false);
        });
    }
  }, [user]);

  if (!user) return <Navigate to="/auth" />;

  return (
    <div className="max-w-5xl mx-auto py-10 animate-in fade-in duration-700">
      <div className="mb-10 text-center">
        <h1 className="text-4xl font-extrabold text-white mb-4">
          Your <span className="text-transparent bg-clip-text bg-gradient-to-r from-indigo-400 to-purple-400">Order History</span>
        </h1>
        <p className="text-gray-400">Track all your past purchases securely joined from our DBMS layer.</p>
      </div>

      {loading ? (
        <div className="flex justify-center items-center h-40">
           <div className="w-10 h-10 border-4 border-purple-500/30 border-t-purple-500 rounded-full animate-spin"></div>
        </div>
      ) : history.length === 0 ? (
        <div className="glass-card p-12 text-center rounded-3xl">
           <div className="w-20 h-20 bg-white/5 rounded-full flex items-center justify-center mx-auto mb-6 shadow-inner">
             <svg className="w-10 h-10 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z"></path></svg>
           </div>
           <h3 className="text-xl font-bold text-white mb-2">No past orders found</h3>
           <p className="text-gray-400 mb-6">Looks like you haven't made any purchases yet.</p>
           <a href="/" className="btn-primary inline-block">Start Shopping</a>
        </div>
      ) : (
        <div className="glass-card rounded-3xl overflow-hidden">
           <table className="glass-table w-full">
             <thead>
               <tr>
                 <th>Order ID</th>
                 <th>Date placed</th>
                 <th>Item</th>
                 <th>Qty</th>
                 <th>Price</th>
                 <th>Total</th>
               </tr>
             </thead>
             <tbody>
               {history.map((order, idx) => (
                 <tr key={`${order.order_id}-${idx}`} className="group hover:bg-white/[0.05] transition-colors">
                   <td className="font-mono text-purple-400">#{order.order_id}</td>
                   <td className="text-gray-300 text-sm">
                      {new Date(order.order_date).toLocaleDateString(undefined, {
                        year: 'numeric', month: 'short', day: 'numeric', hour: '2-digit', minute:'2-digit'
                      })}
                   </td>
                   <td className="font-medium text-white">{order.product_name}</td>
                   <td>
                      <span className="bg-white/10 px-2.5 py-1 rounded-md text-xs font-mono">{order.quantity}</span>
                   </td>
                   <td className="text-gray-400">₹{order.price_at_purchase.toFixed(2)}</td>
                   <td className="text-green-400 font-bold tracking-wide text-lg">
                      ₹{(order.quantity * order.price_at_purchase).toFixed(2)}
                   </td>
                 </tr>
               ))}
             </tbody>
           </table>
        </div>
      )}
    </div>
  );
}
