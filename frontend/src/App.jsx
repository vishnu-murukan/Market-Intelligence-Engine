import { Routes, Route, NavLink, useNavigate } from 'react-router-dom'
import { createContext, useContext, useState, useCallback } from 'react'

// ── Context ──────────────────────────────────────────────────────────────────
const Ctx = createContext(null)
function AppProvider({ children }) {
  const [apiKey, _setKey] = useState(() => localStorage.getItem('mie_key') || '')
  const [agency, _setAgency] = useState(() => localStorage.getItem('mie_agency') || '')
  const [toast, setToast] = useState(null)

  const setApiKey = k => { _setKey(k); localStorage.setItem('mie_key', k) }
  const setAgency = v => { _setAgency(v); localStorage.setItem('mie_agency', v) }
  const notify = useCallback((msg, type = 'info') => {
    setToast({ msg, type, id: Date.now() })
    setTimeout(() => setToast(null), 3500)
  }, [])

  return <Ctx.Provider value={{ apiKey, setApiKey, agency, setAgency, notify, toast }}>{children}</Ctx.Provider>
}
export const useApp = () => useContext(Ctx)

// ── Layout ────────────────────────────────────────────────────────────────────
const NAV = [
  { to: '/', label: 'Dashboard', ic: '▤' },
  { to: '/research', label: 'Research', ic: '◉' },
  { to: '/tracking', label: 'Tracking', ic: '◎' },
  { to: '/settings', label: 'Settings', ic: '◈' },
]

function Layout({ children }) {
  const { apiKey, toast } = useApp()
  return (
    <div style={{ display: 'flex', height: '100vh', overflow: 'hidden' }}>
      <aside style={{ width: 'var(--sidebar)', minWidth: 'var(--sidebar)', background: 'var(--bg1)', borderRight: '1px solid var(--b2)', display: 'flex', flexDirection: 'column' }}>
        <div style={{ padding: '18px 16px 12px', borderBottom: '1px solid var(--b2)' }}>
          <div style={{ fontSize: 13, fontWeight: 600, color: 'var(--t1)', letterSpacing: '.5px' }}>
            <span style={{ color: 'var(--accent2)' }}>●</span> MIE
          </div>
          <div style={{ fontSize: 10, color: 'var(--t3)', marginTop: 3 }}>Market Intelligence Engine</div>
        </div>
        <div style={{ padding: '8px 12px', borderBottom: '1px solid var(--b2)', display: 'flex', alignItems: 'center', gap: 6 }}>
          <span style={{ width: 5, height: 5, borderRadius: '50%', background: apiKey ? 'var(--green)' : 'var(--t4)', display: 'inline-block', flexShrink: 0 }}></span>
          <span style={{ fontSize: 10, color: 'var(--t3)' }}>{apiKey ? 'Gemini connected' : 'No API key'}</span>
        </div>
        <nav style={{ flex: 1, padding: '8px 8px', display: 'flex', flexDirection: 'column', gap: 1 }}>
          {NAV.map(n => (
            <NavLink key={n.to} to={n.to} end={n.to === '/'}
              style={({ isActive }) => ({
                display: 'flex', alignItems: 'center', gap: 8, padding: '7px 10px',
                borderRadius: 'var(--r2)', fontSize: 13, textDecoration: 'none',
                color: isActive ? 'var(--t1)' : 'var(--t3)',
                background: isActive ? 'var(--bg3)' : 'transparent',
                fontWeight: isActive ? 500 : 400,
              })}>
              <span style={{ fontSize: 12, opacity: .7 }}>{n.ic}</span>{n.label}
            </NavLink>
          ))}
        </nav>
        <div style={{ padding: '10px 16px', borderTop: '1px solid var(--b2)', fontSize: 10, color: 'var(--t4)' }}>
          Branding Agency Suite v1.0
        </div>
      </aside>
      <main style={{ flex: 1, display: 'flex', flexDirection: 'column', overflow: 'hidden', background: 'var(--bg0)' }}>
        {children}
      </main>
      {toast && (
        <div className="fade-up" style={{
          position: 'fixed', bottom: 20, right: 20, padding: '10px 16px',
          borderRadius: 'var(--r2)', fontSize: 12, zIndex: 1000, maxWidth: 340,
          background: toast.type === 'error' ? 'rgba(255,95,95,.15)' : 'rgba(124,109,250,.15)',
          border: `1px solid ${toast.type === 'error' ? 'var(--red)' : 'var(--accent)'}`,
          color: toast.type === 'error' ? 'var(--red)' : 'var(--accent2)'
        }}>{toast.msg}</div>
      )}
    </div>
  )
}

// ── Pages ─────────────────────────────────────────────────────────────────────
import DashboardPage from './pages/Dashboard.jsx'
import ResearchPage from './pages/Research.jsx'
import TrackingPage from './pages/Tracking.jsx'
import SettingsPage from './pages/Settings.jsx'

export default function App() {
  return (
    <AppProvider>
      <Layout>
        <Routes>
          <Route path="/" element={<DashboardPage />} />
          <Route path="/research" element={<ResearchPage />} />
          <Route path="/tracking" element={<TrackingPage />} />
          <Route path="/settings" element={<SettingsPage />} />
        </Routes>
      </Layout>
    </AppProvider>
  )
}
