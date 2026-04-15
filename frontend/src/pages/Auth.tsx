import { useState, useContext } from 'react';
import { AuthContext } from '../context/AuthContext';
import { useNavigate } from 'react-router-dom';
import api from '../api/axios';

export default function Auth() {
  const [isLogin, setIsLogin] = useState(true);
  const [form, setForm] = useState({email: '', password: '', first_name: '', last_name: ''});
  const { login } = useContext(AuthContext);
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      if (isLogin) {
        const formData = new URLSearchParams();
        formData.append('username', form.email);
        formData.append('password', form.password);
        const res = await api.post('/auth/login', formData);
        login(res.data.access_token);
      } else {
        await api.post('/auth/signup', form);
        alert('Signup successful! Please login.');
        setIsLogin(true);
        return;
      }
      navigate('/');
    } catch (err: any) {
      alert(err.response?.data?.detail || 'Error occurred');
    }
  };

  return (
    <div className="flex items-center justify-center min-h-[80vh] animate-in zoom-in-95 duration-500">
      <div className="glass-card w-full max-w-md p-10 rounded-[2.5rem] relative overflow-hidden">
        {/* Glow effect behind the form */}
        <div className="absolute top-0 right-0 w-64 h-64 bg-indigo-500/20 blur-[80px] rounded-full pointer-events-none"></div>
        <div className="absolute bottom-0 left-0 w-64 h-64 bg-pink-500/20 blur-[80px] rounded-full pointer-events-none"></div>

        <div className="relative z-10">
          <div className="text-center mb-10">
            <h2 className="text-3xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-white to-gray-400 mb-2">
              {isLogin ? 'Welcome Back' : 'Join ShopSphere'}
            </h2>
            <p className="text-gray-400">
              {isLogin ? 'Enter your details to access your account.' : 'Create an account to start shopping.'}
            </p>
          </div>

          <form onSubmit={handleSubmit} className="flex flex-col gap-5">
            {!isLogin && (
              <div className="flex gap-4">
                <input 
                  className="input-glass w-1/2" 
                  placeholder="First Name" 
                  required 
                  onChange={e => setForm({...form, first_name: e.target.value})} 
                />
                <input 
                  className="input-glass w-1/2" 
                  placeholder="Last Name" 
                  required 
                  onChange={e => setForm({...form, last_name: e.target.value})} 
                />
              </div>
            )}
            
            <div className="space-y-1">
              <label className="text-sm font-medium text-gray-300 ml-1">Email Address</label>
              <input 
                className="input-glass" 
                type="email" 
                placeholder="you@example.com" 
                required 
                onChange={e => setForm({...form, email: e.target.value})} 
              />
            </div>

            <div className="space-y-1 mb-2">
              <label className="text-sm font-medium text-gray-300 ml-1">Password</label>
              <input 
                className="input-glass" 
                type="password" 
                placeholder="••••••••" 
                required 
                onChange={e => setForm({...form, password: e.target.value})} 
              />
            </div>

            <button className="btn-primary w-full py-4 text-lg font-bold shadow-[0_0_30px_rgba(79,70,229,0.3)] hover:shadow-[0_0_40px_rgba(79,70,229,0.5)]">
              {isLogin ? 'Sign In' : 'Create Account'}
            </button>
          </form>

          <div className="mt-8 text-center border-t border-white/10 pt-6">
            <button 
              type="button"
              className="text-gray-400 hover:text-white transition group border-none bg-transparent"
              onClick={() => setIsLogin(!isLogin)}
            >
              {isLogin ? (
                 <>Don't have an account? <span className="text-indigo-400 font-semibold group-hover:underline underline-offset-4">Sign up</span></>
              ) : (
                 <>Already have an account? <span className="text-purple-400 font-semibold group-hover:underline underline-offset-4">Sign in</span></>
              )}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
