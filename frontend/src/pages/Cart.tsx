import { useEffect, useState } from 'react';
import api from '../api/axios';

export default function Cart() {
  const [cart, setCart] = useState<any>(null);

  const fetchCart = () => {
    api.get('/cart').then(res => setCart(res.data)).catch(console.error);
  };

  useEffect(() => {
    fetchCart();
  }, []);

  const handleCheckout = async () => {
    try {
      await api.post('/orders/checkout');
      alert('Order Placed Successfully ✨!');
      fetchCart();
    } catch (err: any) {
      alert(err.response?.data?.detail || 'Checkout failed');
    }
  };

  const handleRemove = async (p_id: number) => {
    try {
      await api.delete(`/cart/remove/${p_id}`);
      fetchCart();
    } catch (err: any) {
      console.error("Failed to remove item");
    }
  };

  if (!cart) {
     return <div className="py-20 text-center text-white text-xl">Loading your cart...</div>;
  }

  const orderTotal = cart?.items?.reduce((acc: number, item: any) => acc + (item.product.p_price * item.quantity), 0) || 0;

  return (
    <div className="max-w-5xl mx-auto py-10 animate-in fade-in slide-in-from-bottom-5 duration-500">
      <h1 className="text-4xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-gray-100 to-gray-400 mb-8">
        Your Cart
      </h1>

      {cart.items?.length === 0 ? (
        <div className="glass-card p-16 rounded-3xl text-center">
           <div className="w-24 h-24 bg-white/5 rounded-full flex items-center justify-center mx-auto mb-6 text-4xl">🛒</div>
           <h2 className="text-2xl font-bold text-white mb-2">Cart is empty</h2>
           <p className="text-gray-400 mb-8">Looks like you haven't added anything yet.</p>
           <a href="/" className="btn-secondary">Explore Products</a>
        </div>
      ) : (
        <div className="flex flex-col lg:flex-row gap-8">
          <div className="flex-grow space-y-4">
            {cart.items.map((item: any) => (
              <div key={item.p_id} className="glass-card p-6 rounded-3xl flex items-center gap-6 relative group overflow-hidden">
                <div className="w-24 h-24 rounded-2xl overflow-hidden bg-black/40 flex-shrink-0">
                  {item.product.p_image_url ? (
                     <img src={item.product.p_image_url} alt="item" className="w-full h-full object-cover" />
                  ) : (
                     <div className="w-full h-full bg-gradient-to-tr from-indigo-500/20 to-purple-500/20" />
                  )}
                </div>
                
                <div className="flex-grow">
                   <h3 className="text-lg font-bold text-white mb-1">{item.product.p_name}</h3>
                   <div className="text-sm font-medium text-purple-400 mb-2">Unit Price: ₹{item.product.p_price}</div>
                   <div className="inline-flex items-center gap-4 bg-white/5 px-3 py-1 rounded-lg border border-white/10">
                     <span className="text-sm text-gray-400">Qty:</span>
                     <span className="font-bold text-white">{item.quantity}</span>
                   </div>
                </div>
                
                <div className="text-right">
                  <div className="text-2xl font-extrabold text-white mb-4">
                     ₹{(item.product.p_price * item.quantity).toFixed(2)}
                  </div>
                  <button onClick={() => handleRemove(item.p_id)} className="text-sm text-red-400 hover:text-red-300 transition underline underline-offset-4">
                    Remove
                  </button>
                </div>
              </div>
            ))}
          </div>

          <div className="w-full lg:w-96 flex-shrink-0">
             <div className="glass-card p-8 rounded-3xl sticky top-24">
               <h3 className="text-xl font-bold text-white mb-6">Order Summary</h3>
               
               <div className="space-y-4 border-b border-white/10 pb-6 mb-6">
                 <div className="flex justify-between text-gray-400">
                    <span>Subtotal</span>
                    <span>₹{orderTotal.toFixed(2)}</span>
                 </div>
                 <div className="flex justify-between text-gray-400">
                    <span>Shipping</span>
                    <span className="text-green-400">Free</span>
                 </div>
                 <div className="flex justify-between text-gray-400">
                    <span>Tax Estimate</span>
                    <span>₹{(orderTotal * 0.08).toFixed(2)}</span>
                 </div>
               </div>
               
               <div className="flex justify-between items-end mb-8">
                  <span className="text-gray-300 font-medium">Total</span>
                  <span className="text-4xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-purple-400 to-pink-400">
                    ₹{(orderTotal * 1.08).toFixed(2)}
                  </span>
               </div>
               
               <button onClick={handleCheckout} className="btn-primary w-full py-4 text-lg font-bold shadow-[0_0_40px_rgba(168,85,247,0.4)]">
                 Checkout Securely
               </button>
             </div>
          </div>
        </div>
      )}
    </div>
  );
}
