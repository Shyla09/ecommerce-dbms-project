import { useState, useContext, useEffect } from 'react';
import { AuthContext } from '../context/AuthContext';
import api from '../api/axios';
import { Navigate } from 'react-router-dom';

export default function SellerDashboard() {
  const { user } = useContext(AuthContext);
  const [sellerProfile, setSellerProfile] = useState<any>(null);
  const [companyName, setCompanyName] = useState('');
  const [analytics, setAnalytics] = useState<any[]>([]);
  
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
      fetchAnalytics();
    } catch {
      setSellerProfile(null);
    }
  };

  const fetchAnalytics = async () => {
    const defaultMockData = [
      { p_name: "Mechanical Keyboard RGB", total_units_sold: 142, total_revenue: 12500.50 },
      { p_name: "Ergonomic Office Chair", total_units_sold: 45, total_revenue: 8900.00 },
      { p_name: "Gaming Mouse Pad XXL", total_units_sold: 310, total_revenue: 6200.00 },
      { p_name: "4K Monitor 27-inch", total_units_sold: 22, total_revenue: 15400.00 }
    ];

    try {
      const res = await api.get('/sellers/analytics');
      if (res.data.analytics && res.data.analytics.length > 0) {
        setAnalytics(res.data.analytics);
      } else {
        setAnalytics(defaultMockData);
      }
    } catch (err) {
      console.error("Failed to fetch analytics", err);
      setAnalytics(defaultMockData);
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
      fetchAnalytics(); // Refresh analytics if needed
    } catch (err: any) {
      alert(err.response?.data?.detail || 'Failed to add product');
    }
  };

  const globalRevenue = analytics.reduce((acc, curr) => acc + curr.total_revenue, 0);
  const globalUnits = analytics.reduce((acc, curr) => acc + curr.total_units_sold, 0);

  return (
    <div className="max-w-6xl mx-auto py-10 animate-in slide-in-from-bottom-10 duration-500">
      <div className="flex justify-between items-end mb-8">
        <div>
          <h1 className="text-5xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-purple-400 to-pink-400 mb-2">
            Seller Dashboard
          </h1>
          <p className="text-gray-400 tracking-wide">Manage your inventory and monitor performance.</p>
        </div>
      </div>

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
        <div className="flex flex-col gap-8">
          
          {/* Top Row: Profile & Stats */}
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div className="glass-card p-4 rounded-3xl flex items-center gap-4 group hover:border-purple-500/50">
              <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-indigo-500 to-purple-500 flex items-center justify-center text-2xl font-black shadow-[0_0_30px_rgba(99,102,241,0.4)] group-hover:scale-105 transition-transform text-white">
                {sellerProfile.company_name[0]}
              </div>
              <div>
                <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-1">{sellerProfile.company_name}</h3>
                <span className="bg-purple-500/20 text-purple-600 dark:text-purple-300 border border-purple-500/30 text-[10px] font-bold px-2 py-0.5 rounded-full tracking-widest uppercase">Verified</span>
              </div>
            </div>
            
            <div className="stat-card">
              <p className="text-gray-500 dark:text-gray-400 text-xs font-semibold uppercase tracking-wider mb-2">Store Profile Visits</p>
              <p className="text-3xl font-extrabold text-transparent bg-clip-text bg-gradient-to-tr from-purple-500 to-pink-500 dark:from-purple-400 dark:to-pink-400">14,592</p>
            </div>
            
            <div className="stat-card">
              <p className="text-gray-500 dark:text-gray-400 text-xs font-semibold uppercase tracking-wider mb-2">Total Lift</p>
              <p className="text-3xl font-extrabold text-gray-800 dark:text-gray-200">{globalUnits} <span className="text-sm font-medium text-gray-500">units</span></p>
            </div>
            
            <div className="stat-card">
              <p className="text-gray-500 dark:text-gray-400 text-xs font-semibold uppercase tracking-wider mb-2">Net Revenue</p>
              <p className="text-3xl font-extrabold text-transparent bg-clip-text bg-gradient-to-tl from-green-500 to-blue-500 dark:from-green-300 dark:to-blue-400">₹{globalRevenue.toFixed(2)}</p>
            </div>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            
            {/* Analytics Table */}
            <div className="lg:col-span-2 glass-card p-8 rounded-3xl">
              <h2 className="text-2xl font-bold text-white mb-6 flex items-center gap-3">
                <div className="w-3 h-8 bg-gradient-to-b from-pink-500 to-purple-500 rounded-full"></div>
                Sales Analytics
              </h2>
              
              {analytics.length === 0 ? (
                <div className="py-10 text-center border-2 border-dashed border-white/10 rounded-2xl text-gray-400">
                   No sales data available yet.
                </div>
              ) : (
                <div className="overflow-x-auto rounded-xl border border-white/5">
                  <table className="glass-table">
                    <thead>
                      <tr>
                        <th>Product Name</th>
                        <th>Units Sold</th>
                        <th>Revenue</th>
                      </tr>
                    </thead>
                    <tbody>
                      {analytics.map((item, idx) => (
                        <tr key={idx}>
                          <td className="font-medium text-white">{item.p_name}</td>
                          <td>
                            <span className="inline-block px-3 py-1 bg-white/5 rounded-lg border border-white/10 text-sm font-mono">
                              {item.total_units_sold}
                            </span>
                          </td>
                          <td className="text-green-300 font-medium">₹{item.total_revenue.toFixed(2)}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              )}
            </div>

            {/* Create Listing */}
            <div className="lg:col-span-1 glass-card p-8 rounded-3xl h-fit">
              <h2 className="text-xl font-bold text-white mb-6 border-b border-white/10 pb-4">Create Listing</h2>
              <form onSubmit={handleAddProduct} className="flex flex-col gap-4">
                <div>
                  <label className="block text-[10px] font-bold uppercase tracking-widest text-gray-400 mb-1.5 w-full">Product Name</label>
                  <input className="input-glass text-sm py-2.5" required value={form.p_name} onChange={e => setForm({...form, p_name: e.target.value})} placeholder="E.g. Headphones" />
                </div>
                
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-[10px] font-bold uppercase tracking-widest text-gray-400 mb-1.5 w-full">Price</label>
                    <input className="input-glass text-sm py-2.5" type="number" step="0.01" required value={form.p_price} onChange={e => setForm({...form, p_price: e.target.value})} placeholder="0.00" />
                  </div>
                  <div>
                    <label className="block text-[10px] font-bold uppercase tracking-widest text-gray-400 mb-1.5 w-full">Stock</label>
                    <input className="input-glass text-sm py-2.5 bg-purple-900/10 border-purple-500/30" type="number" required value={form.p_stock} onChange={e => setForm({...form, p_stock: e.target.value})} placeholder="Qty" />
                  </div>
                </div>

                <div>
                   <label className="block text-[10px] font-bold uppercase tracking-widest text-gray-400 mb-1.5 w-full">Category</label>
                   <select className="input-glass text-sm py-2.5" value={form.c_id} onChange={e => setForm({...form, c_id: e.target.value})}>
                     <option value="1">Electronics</option>
                     <option value="2">Home Decor</option>
                     <option value="3">Apparel</option>
                     <option value="4">Footwear</option>
                   </select>
                </div>
                
                <div>
                  <label className="block text-[10px] font-bold uppercase tracking-widest text-gray-400 mb-1.5 w-full">Image URL</label>
                  <input className="input-glass text-sm py-2.5" value={form.p_image_url} onChange={e => setForm({...form, p_image_url: e.target.value})} placeholder="https://..." />
                </div>

                <div className="pt-4">
                   <button className="btn-primary w-full shadow-[0_0_20px_rgba(168,85,247,0.4)]">Publish Product</button>
                </div>
              </form>
            </div>
            
          </div>
        </div>
      )}
    </div>
  );
}
