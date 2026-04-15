import { useState, useContext, useEffect } from 'react';
import { AuthContext } from '../context/AuthContext';
import api from '../api/axios';
import { Navigate } from 'react-router-dom';

export default function SellerDashboard() {
  const { user } = useContext(AuthContext);
  const [sellerProfile, setSellerProfile] = useState<any>(null);
  const [companyName, setCompanyName] = useState('');
  
  // Product Form
  const [form, setForm] = useState({
    p_name: '',
    p_price: '',
    p_description: '',
    p_image_url: '',
    p_stock: '',
    c_id: '1' // Default Category ID (Electronics)
  });

  const checkSeller = async () => {
    try {
      const res = await api.get('/sellers/me');
      setSellerProfile(res.data);
    } catch {
      setSellerProfile(null);
    }
  };

  useEffect(() => {
    if (user) checkSeller();
  }, [user]);

  if (!user) return <Navigate to="/auth" />;

  const handleRegister = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await api.post('/sellers/register', { company_name: companyName });
      alert('Successfully registered as a Seller!');
      checkSeller();
    } catch (err: any) {
      alert(err.response?.data?.detail || 'Failed to register');
    }
  };

  const handleAddProduct = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await api.post('/products', {
        p_name: form.p_name,
        p_price: parseFloat(form.p_price),
        p_description: form.p_description,
        p_image_url: form.p_image_url || null,
        p_stock: parseInt(form.p_stock),
        c_id: parseInt(form.c_id)
      });
      alert('Product Added Successfully!');
      setForm({ ...form, p_name: '', p_price: '', p_description: '', p_image_url: '', p_stock: '' });
    } catch (err: any) {
      alert(err.response?.data?.detail || 'Failed to add product');
    }
  };

  return (
    <div className="max-w-4xl mx-auto py-10 animate-in slide-in-from-bottom-10 duration-500">
      <h1 className="text-4xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-purple-400 to-pink-400 mb-8">
        Seller Dashboard
      </h1>

      {!sellerProfile ? (
        <div className="glass-card p-10 rounded-3xl border border-purple-500/30 shadow-[0_0_50px_rgba(168,85,247,0.1)]">
          <div className="text-center mb-8">
            <h2 className="text-2xl font-bold text-white mb-2">Partner with ShopSphere</h2>
            <p className="text-gray-400">Launch your products to thousands of daily visitors organically.</p>
          </div>
          <form onSubmit={handleRegister} className="flex flex-col gap-6 max-w-md mx-auto">
            <div>
               <label className="block text-sm font-medium text-purple-300 mb-1">Company Name</label>
               <input 
                 className="input-glass" 
                 placeholder="E.g. Acme Corp" 
                 required 
                 value={companyName}
                 onChange={e => setCompanyName(e.target.value)} 
               />
            </div>
            <button className="btn-primary mt-2">Become a Seller</button>
          </form>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div className="md:col-span-1 glass-card p-6 rounded-3xl h-fit">
            <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-indigo-500 to-purple-500 mb-4 flex items-center justify-center text-2xl font-bold shadow-lg">
              {sellerProfile.company_name[0]}
            </div>
            <h3 className="text-xl font-bold text-white">{sellerProfile.company_name}</h3>
            <p className="text-sm text-gray-400 mb-6">Verified Partner Status</p>
            
            <div className="space-y-4 border-t border-white/10 pt-6">
              <div className="flex justify-between">
                <span className="text-gray-400">Seller ID</span>
                <span className="font-mono text-purple-300">#{sellerProfile.seller_id}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-400">Plan</span>
                <span className="text-indigo-300 font-medium tracking-wide">Enterprise</span>
              </div>
            </div>
          </div>

          <div className="md:col-span-2 glass-card p-8 rounded-3xl">
            <h2 className="text-2xl font-bold text-white mb-6">Create New Listing</h2>
            <form onSubmit={handleAddProduct} className="flex flex-col gap-5">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
                 <div>
                   <label className="block text-xs font-semibold uppercase tracking-wider text-gray-400 mb-2">Product Name</label>
                   <input className="input-glass" required value={form.p_name} onChange={e => setForm({...form, p_name: e.target.value})} placeholder="Nike Air Max..." />
                 </div>
                 <div>
                   <label className="block text-xs font-semibold uppercase tracking-wider text-gray-400 mb-2">Price ($)</label>
                   <input className="input-glass" type="number" step="0.01" required value={form.p_price} onChange={e => setForm({...form, p_price: e.target.value})} placeholder="129.99" />
                 </div>
              </div>
              
              <div>
                 <label className="block text-xs font-semibold uppercase tracking-wider text-gray-400 mb-2">Category</label>
                 <select className="input-glass" value={form.c_id} onChange={e => setForm({...form, c_id: e.target.value})}>
                   <option value="1">Electronics</option>
                   <option value="2">Home Decor</option>
                   <option value="3">Apparel</option>
                   <option value="4">Footwear</option>
                 </select>
              </div>

              <div>
                <label className="block text-xs font-semibold uppercase tracking-wider text-gray-400 mb-2">Image URL</label>
                <input className="input-glass" value={form.p_image_url} onChange={e => setForm({...form, p_image_url: e.target.value})} placeholder="https://unsplash.com/..." />
              </div>

              <div>
                <label className="block text-xs font-semibold uppercase tracking-wider text-gray-400 mb-2">Stock Details</label>
                <input className="input-glass" type="number" required value={form.p_stock} onChange={e => setForm({...form, p_stock: e.target.value})} placeholder="Quantity Available" />
              </div>

              <div>
                <label className="block text-xs font-semibold uppercase tracking-wider text-gray-400 mb-2">Description</label>
                <textarea className="input-glass min-h-[100px] resize-y" value={form.p_description} onChange={e => setForm({...form, p_description: e.target.value})} placeholder="Highlight key features..." />
              </div>

              <div className="pt-4 border-t border-white/5 mt-2">
                 <button className="btn-primary w-full py-4 text-lg">Push to Store</button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
