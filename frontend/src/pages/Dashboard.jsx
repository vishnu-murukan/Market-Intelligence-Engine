import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useApp } from '../App.jsx'

const S = {
  page: { flex: 1, overflow: 'auto', padding: '28px 32px' },
  header: { display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: 28 },
  h1: { fontSize: 20, fontWeight: 600, color: 'var(--t1)' },
  sub: { fontSize: 12, color: 'var(--t3)', marginTop: 3 },
  btn: { padding: '8px 16px', background: 'var(--accent)', color: '#fff', border: 'none', borderRadius: 'var(--r2)', fontSize: 12, fontWeight: 500, cursor: 'pointer' },
  warn: { background: 'rgba(245,166,35,.08)', border: '1px solid rgba(245,166,35,.3)', color: 'var(--amber)', borderRadius: 'var(--r2)', padding: '10px 14px', fontSize: 12, marginBottom: 20, display: 'flex', gap: 8 },
  stats: { display: 'grid', gridTemplateColumns: 'repeat(4,1fr)', gap: 12, marginBottom: 28 },
  stat: { background: 'var(--bg2)', border: '1px solid var(--b1)', borderRadius: 'var(--r3)', padding: '16px 18px' },
  statVal: { fontSize: 24, fontWeight: 600, color: 'var(--t1)' },
  statLabel: { fontSize: 11, color: 'var(--t3)', marginTop: 2 },
  cols: { display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 16 },
  card: { background: 'var(--bg1)', border: '1px solid var(--b1)', borderRadius: 'var(--r3)', overflow: 'hidden' },
  cardHead: { padding: '12px 16px', borderBottom: '1px solid var(--b2)', display: 'flex', justifyContent: 'space-between', alignItems: 'center' },
  cardTitle: { fontSize: 12, fontWeight: 500, color: 'var(--t2)' },
  ghost: { background: 'none', border: '1px solid var(--b1)', color: 'var(--t3)', padding: '4px 10px', borderRadius: 'var(--r1)', fontSize: 11, cursor: 'pointer' },
  row: { padding: '10px 16px', borderBottom: '1px solid var(--b2)', display: 'flex', alignItems: 'center', gap: 10, cursor: 'pointer' },
  init: { width: 28, height: 28, borderRadius: 'var(--r1)', background: 'var(--bg3)', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: 11, fontWeight: 500, color: 'var(--t2)', flexShrink: 0 },
  name: { fontSize: 13, color: 'var(--t1)', fontWeight: 500 },
  meta: { fontSize: 11, color: 'var(--t3)' },
  empty: { padding: '24px 16px', fontSize: 12, color: 'var(--t4)', textAlign: 'center' },
}

function fmt(iso) {
  return new Date(iso).toLocaleDateString('en-GB', { day: '2-digit', month: 'short' })
}

export default function Dashboard() {
  const { apiKey } = useApp()
  const nav = useNavigate()
  const [sessions, setSessions] = useState([])
  const [campaigns, setCampaigns] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    Promise.all([
      fetch('/api/intelligence/sessions').then(r => r.json()).catch(() => []),
      fetch('/api/tracking/campaigns').then(r => r.json()).catch(() => []),
    ]).then(([s, c]) => { setSessions(s); setCampaigns(c) }).finally(() => setLoading(false))
  }, [])

  const totalSent    = campaigns.reduce((a, c) => a + (c.stats?.sent    || 0), 0)
  const totalReplied = campaigns.reduce((a, c) => a + (c.stats?.replied || 0), 0)
  const rate = totalSent ? Math.round((totalReplied / totalSent) * 100) : 0

  return (
    <div style={S.page}>
      <div style={S.header}>
        <div><div style={S.h1}>Dashboard</div><div style={S.sub}>Market intelligence & outreach overview</div></div>
        <button style={S.btn} onClick={() => nav('/research')}>+ New Research Run</button>
      </div>

      {!apiKey && (
        <div style={S.warn}>
          <span>⚠</span>
          <span>No Gemini API key. <a onClick={() => nav('/settings')} style={{ cursor: 'pointer', color: 'var(--amber)' }}>Add it in Settings →</a></span>
        </div>
      )}

      <div style={S.stats}>
        {[
          { label: 'Research Runs', val: sessions.length, c: 'var(--accent2)' },
          { label: 'Campaigns', val: campaigns.length, c: 'var(--blue)' },
          { label: 'Contacts Logged', val: totalSent, c: 'var(--purple)' },
          { label: 'Response Rate', val: `${rate}%`, c: 'var(--green)' },
        ].map(s => (
          <div key={s.label} style={S.stat}>
            <div style={{ ...S.statVal, color: s.c }}>{s.val}</div>
            <div style={S.statLabel}>{s.label}</div>
          </div>
        ))}
      </div>

      <div style={S.cols}>
        <div style={S.card}>
          <div style={S.cardHead}>
            <span style={S.cardTitle}>RECENT RESEARCH RUNS</span>
            <button style={S.ghost} onClick={() => nav('/research')}>New run</button>
          </div>
          {loading ? <SkList /> : sessions.length === 0 ? <div style={S.empty}>No runs yet. Start your first research run.</div> : (
            sessions.map(s => {
              const isInd = s.category && (s.category.startsWith('Industry') || s.category.includes('Industry'))
              const totalSecs = isInd ? 6 : 11
              return (
                <div key={s.id} style={S.row} onClick={() => nav('/research')}>
                  <div style={S.init}>{s.company?.[0]?.toUpperCase()}</div>
                  <div style={{ flex: 1 }}>
                    <div style={S.name}>{s.company}</div>
                    <div style={S.meta}>{s.category}</div>
                  </div>
                  <div style={{ textAlign: 'right' }}>
                    <div style={{ fontSize: 11, color: 'var(--t2)' }}>{s.sectionsCompleted}/{totalSecs}</div>
                    <div style={{ fontSize: 10, color: 'var(--t4)' }}>{fmt(s.createdAt)}</div>
                  </div>
                </div>
              )
            })
          )}
        </div>

        <div style={S.card}>
          <div style={S.cardHead}>
            <span style={S.cardTitle}>OUTREACH CAMPAIGNS</span>
            <button style={S.ghost} onClick={() => nav('/tracking')}>View all</button>
          </div>
          {loading ? <SkList n={2} /> : campaigns.length === 0 ? <div style={S.empty}>No campaigns. Log outreach from the Tracking page.</div> : (
            campaigns.map(c => {
              const rr = c.stats?.sent ? Math.round((c.stats.replied / c.stats.sent) * 100) : 0
              return (
                <div key={c.id} style={S.row} onClick={() => nav('/tracking')}>
                  <div style={{ ...S.init, background: 'rgba(91,196,255,.1)', color: 'var(--blue)' }}>{c.company?.[0]?.toUpperCase()}</div>
                  <div style={{ flex: 1 }}>
                    <div style={S.name}>{c.company}</div>
                    <div style={S.meta}>{c.stats?.sent || 0} sent · {c.stats?.replied || 0} replied</div>
                  </div>
                  <span style={{ fontSize: 11, fontWeight: 500, color: rr >= 15 ? 'var(--green)' : rr >= 5 ? 'var(--amber)' : 'var(--t3)' }}>{rr}%</span>
                </div>
              )
            })
          )}
        </div>
      </div>
    </div>
  )
}

function SkList({ n = 3 }) {
  return (
    <div style={{ padding: '10px 16px', display: 'flex', flexDirection: 'column', gap: 8 }}>
      {Array.from({ length: n }).map((_, i) => <div key={i} className="skeleton" style={{ height: 36 }}></div>)}
    </div>
  )
}
