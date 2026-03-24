import { useEffect, useState } from 'react';
import { BrowserRouter, Routes, Route, Link, useLocation } from 'react-router-dom';
import { syncEvents, type SyncResult } from './db/loader';
import { TimelineTable } from './components/visualization/TimelineTable';
import { LayoutDashboard, Clock } from 'lucide-react';
import { TimelineView } from './components/visualization/TimelineView';

function App() {
  const [init, setInit] = useState<{ initialized: boolean; count: number; error?: string }>({
    initialized: false,
    count: 0
  });

  useEffect(() => {
    syncEvents()
      .then((res: SyncResult) => setInit({ initialized: true, count: res.count }))
      .catch((err) => setInit({ initialized: true, count: 0, error: err.message }));
  }, []);

  if (!init.initialized) {
    return (
      <div className="loading-screen">
        <div className="loading-text">Loading Capture Cascade Timeline...</div>
      </div>
    );
  }

  if (init.error) {
    return (
      <div className="error-screen">
        <h2>Failed to load</h2>
        <p>{init.error}</p>
        <button onClick={() => window.location.reload()}>Retry</button>
      </div>
    );
  }

  return (
    <BrowserRouter basename="/viewer">
      <div className="app-shell">
        <Sidebar count={init.count} />
        <main className="app-main">
          <Routes>
            <Route path="/" element={<TimelineTable />} />
            <Route path="/d3" element={<TimelineView />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  );
}

function Sidebar({ count }: { count: number }) {
  const location = useLocation();
  const isActive = (path: string) => location.pathname === path;

  const navItems = [
    { path: '/', icon: LayoutDashboard, label: 'Timeline' },
    { path: '/d3', icon: Clock, label: 'Visual Timeline' },
  ];

  return (
    <aside className="sidebar">
      <div className="sidebar-header">
        <a href="/site/cascade-timeline" className="sidebar-brand">
          <span className="brand-mark">CC</span>
          <div>
            <div className="brand-name">Capture Cascade</div>
            <div className="brand-sub">{count.toLocaleString()} events</div>
          </div>
        </a>
      </div>
      <nav className="sidebar-nav">
        {navItems.map(item => (
          <Link
            key={item.path}
            to={item.path}
            className={`nav-item ${isActive(item.path) ? 'active' : ''}`}
          >
            <item.icon size={18} />
            {item.label}
          </Link>
        ))}
      </nav>
      <div className="sidebar-footer">
        <a href="/site/cascade-timeline" className="nav-item">
          Browse KB
        </a>
      </div>
    </aside>
  );
}

export default App;
