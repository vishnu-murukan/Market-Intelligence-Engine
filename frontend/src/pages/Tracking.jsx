import { useState, useEffect } from 'react'

const STATUS_OPTS = ['Sent', 'Opened', 'Clicked', 'Replied', 'Meeting Booked', 'No Reply', 'Not Interested']
const STATUS_COLOR = {
  'Sent': 'rgba(91,196,255,.8)', 'Opened': 'var(--amber)', 'Clicked': 'var(--purple)',
  'Replied': 'var(--green)', 'Meeting Booked': '#3ecf8e', 'No Reply': 'var(--t4)', 'Not Interested': 'var(--red)'
}
const CH_OPTS = ['Email', 'LinkedIn', 'WhatsApp', 'Phone', 'In Person']

export default function Tracking() {
  const [campaigns, setCampaigns] = useState([])
  const [activeCampaign, setActiveCampaign] = useState(null)
  const [leads, setLeads] = useState([])
  const [stats, setStats] = useState(null)
  const [newCo, setNewCo] = useState('')
  const [showForm, setShowForm] = useState(false)
  const [form, setForm] = useState({ contact: '', email: '', title: '', channel: 'Email', status: 'Sent', notes: '' })
  const [editLead, setEditLead] = useState(null)

  useEffect(() => {
    fetch('/api/tracking/campaigns').then(r => r.json()).then(setCampaigns).catch(() => {})
  }, [])

  async function loadCampaign(cid) {
    const [detail, st] = await Promise.all([
      fetch(`/api/tracking/campaigns/${cid}`).then(r => r.json()),
      fetch(`/api/tracking/campaigns/${cid}/stats`).then(r => r.json())
    ])
    setActiveCampaign(detail)
    setLeads(detail.leads || [])
    setStats(st)
  }

  async function createCampaign() {
    if (!newCo.trim()) return
    const res = await fetch('/api/tracking/campaigns', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ company: newCo.trim() }) })
    const c = await res.json()
    setCampaigns(p => [c, ...p])
    setNewCo('')
    loadCampaign(c.id)
  }

  async function addLead() {
    if (!form.contact || !activeCampaign) return
    const res = await fetch(`/api/tracking/campaigns/${activeCampaign.id}/leads`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(form) })
    const lead = await res.json()
    setLeads(p => [...p, lead])
    setForm({ contact: '', email: '', title: '', channel: 'Email', status: 'Sent', notes: '' })
    setShowForm(false)
    fetch(`/api/tracking/campaigns/${activeCampaign.id}/stats`).then(r => r.json()).then(setStats)
  }

  async function updateStatus(leadId, status) {
    const res = await fetch(`/api/tracking/leads/${leadId}`, { method: 'PATCH', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ status }) })
    const updated = await res.json()
    setLeads(p => p.map(l => l.id === leadId ? updated : l))
    setEditLead(null)
    fetch(`/api/tracking/campaigns/${activeCampaign.id}/stats`).then(r => r.json()).then(setStats)
  }

  const inp = { width: '100%', background: 'var(--bg2)', border: '1px solid var(--b1)', borderRadius: 'var(--r1)', padding: '7px 9px', fontSize: 12, color: 'var(--t1)', fontFamily: 'var(--font)', marginBottom: 8 }
  const sel = { ...inp, marginBottom: 0 }

  return (
    <div style={{ display: 'flex', height: '100%', overflow: 'hidden' }}>
      {/* Campaigns sidebar */}
      <div style={{ width: 220, minWidth: 220, background: 'var(--bg1)', borderRight: '1px solid var(--b2)', display: 'flex', flexDirection: 'column' }}>
        <div style={{ padding: '12px 12px', borderBottom: '1px solid var(--b2)' }}>
          <div style={{ fontSize: 10, color: 'var(--t3)', marginBottom: 6, letterSpacing: .4, fontWeight: 500 }}>NEW CAMPAIGN</div>
          <div style={{ display: 'flex', gap: 6 }}>
            <input value={newCo} onChange={e => setNewCo(e.target.value)} placeholder="Company name"
              style={{ ...inp, marginBottom: 0, flex: 1 }}
              onKeyDown={e => e.key === 'Enter' && createCampaign()} />
            <button onClick={createCampaign} style={{ padding: '7px 10px', background: 'var(--accent)', border: 'none', borderRadius: 'var(--r1)', color: '#fff', cursor: 'pointer', fontSize: 12 }}>+</button>
          </div>
        </div>
        <div style={{ flex: 1, overflow: 'auto' }}>
          {campaigns.length === 0 && <div style={{ padding: '20px 12px', fontSize: 11, color: 'var(--t4)', textAlign: 'center' }}>No campaigns yet</div>}
          {campaigns.map(c => (
            <div key={c.id} onClick={() => loadCampaign(c.id)}
              style={{ padding: '10px 12px', cursor: 'pointer', borderBottom: '1px solid var(--b2)', background: activeCampaign?.id === c.id ? 'var(--bg2)' : 'none' }}
              onMouseEnter={e => { if (activeCampaign?.id !== c.id) e.currentTarget.style.background = 'var(--bg2)' }}
              onMouseLeave={e => { if (activeCampaign?.id !== c.id) e.currentTarget.style.background = 'none' }}>
              <div style={{ fontWeight: 500, fontSize: 12, color: 'var(--t1)' }}>{c.company}</div>
              <div style={{ fontSize: 10, color: 'var(--t3)', marginTop: 2 }}>
                {c.stats?.sent || 0} sent · {c.stats?.replied || 0} replied
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Main */}
      <div style={{ flex: 1, display: 'flex', flexDirection: 'column', overflow: 'hidden' }}>
        {!activeCampaign ? (
          <div style={{ flex: 1, display: 'flex', alignItems: 'center', justifyContent: 'center', flexDirection: 'column', gap: 10, color: 'var(--t3)' }}>
            <div style={{ fontSize: 24, opacity: .3 }}>◎</div>
            <div style={{ fontSize: 13, color: 'var(--t2)' }}>Select or create a campaign</div>
          </div>
        ) : (
          <>
            {/* Stats bar */}
            <div style={{ background: 'var(--bg1)', borderBottom: '1px solid var(--b2)', padding: '12px 20px', display: 'flex', gap: 20, alignItems: 'center' }}>
              <div style={{ fontWeight: 500, color: 'var(--t1)', fontSize: 14 }}>{activeCampaign.company}</div>
              <div style={{ flex: 1, display: 'flex', gap: 16 }}>
                {stats && [
                  { label: 'Sent', val: stats.sent },
                  { label: 'Opened', val: stats.opened },
                  { label: 'Replied', val: stats.replied },
                  { label: 'Meetings', val: stats.meetings },
                  { label: 'Response Rate', val: `${stats.responseRate || 0}%` },
                  { label: 'Open Rate', val: `${stats.openRate || 0}%` },
                ].map(m => (
                  <div key={m.label}>
                    <div style={{ fontSize: 14, fontWeight: 500, color: 'var(--t1)' }}>{m.val}</div>
                    <div style={{ fontSize: 10, color: 'var(--t3)' }}>{m.label}</div>
                  </div>
                ))}
              </div>
              <button onClick={() => setShowForm(p => !p)} style={{ padding: '7px 14px', background: 'var(--accent)', border: 'none', borderRadius: 'var(--r1)', color: '#fff', fontSize: 12, cursor: 'pointer', fontFamily: 'var(--font)' }}>
                + Log Outreach
              </button>
            </div>

            {/* Log form */}
            {showForm && (
              <div style={{ background: 'var(--bg2)', borderBottom: '1px solid var(--b1)', padding: '14px 20px' }}>
                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr 1fr 1fr', gap: 10, marginBottom: 10 }}>
                  <div><div style={{ fontSize: 9, color: 'var(--t3)', marginBottom: 3 }}>CONTACT NAME</div><input style={inp} value={form.contact} onChange={e => setForm(p => ({ ...p, contact: e.target.value }))} placeholder="Jane Smith" /></div>
                  <div><div style={{ fontSize: 9, color: 'var(--t3)', marginBottom: 3 }}>EMAIL</div><input style={inp} value={form.email} onChange={e => setForm(p => ({ ...p, email: e.target.value }))} placeholder="jane@company.com" /></div>
                  <div><div style={{ fontSize: 9, color: 'var(--t3)', marginBottom: 3 }}>ROLE</div><input style={inp} value={form.title} onChange={e => setForm(p => ({ ...p, title: e.target.value }))} placeholder="Marketing Director" /></div>
                  <div><div style={{ fontSize: 9, color: 'var(--t3)', marginBottom: 3 }}>CHANNEL</div><select style={sel} value={form.channel} onChange={e => setForm(p => ({ ...p, channel: e.target.value }))}>{CH_OPTS.map(o => <option key={o}>{o}</option>)}</select></div>
                  <div><div style={{ fontSize: 9, color: 'var(--t3)', marginBottom: 3 }}>STATUS</div><select style={sel} value={form.status} onChange={e => setForm(p => ({ ...p, status: e.target.value }))}>{STATUS_OPTS.map(o => <option key={o}>{o}</option>)}</select></div>
                </div>
                <div style={{ display: 'flex', gap: 8 }}>
                  <input style={{ ...inp, marginBottom: 0, flex: 1 }} value={form.notes} onChange={e => setForm(p => ({ ...p, notes: e.target.value }))} placeholder="Notes (optional)" />
                  <button onClick={addLead} style={{ padding: '7px 16px', background: 'var(--accent)', border: 'none', borderRadius: 'var(--r1)', color: '#fff', fontSize: 12, cursor: 'pointer', fontFamily: 'var(--font)', whiteSpace: 'nowrap' }}>Save</button>
                  <button onClick={() => setShowForm(false)} style={{ padding: '7px 12px', background: 'none', border: '1px solid var(--b1)', borderRadius: 'var(--r1)', color: 'var(--t3)', fontSize: 12, cursor: 'pointer', fontFamily: 'var(--font)' }}>Cancel</button>
                </div>
              </div>
            )}

            {/* Leads table */}
            <div style={{ flex: 1, overflow: 'auto' }}>
              <table style={{ width: '100%', borderCollapse: 'collapse' }}>
                <thead>
                  <tr style={{ background: 'var(--bg2)', borderBottom: '1px solid var(--b1)' }}>
                    {['Contact', 'Role', 'Email', 'Channel', 'Status', 'Date', ''].map(h => (
                      <th key={h} style={{ padding: '8px 14px', fontSize: 10, color: 'var(--t3)', textAlign: 'left', fontWeight: 500, letterSpacing: .3 }}>{h}</th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {leads.length === 0 && (
                    <tr><td colSpan={7} style={{ padding: '32px', textAlign: 'center', fontSize: 12, color: 'var(--t4)' }}>No outreach logged yet. Click "+ Log Outreach" to start.</td></tr>
                  )}
                  {leads.map(l => (
                    <tr key={l.id} style={{ borderBottom: '1px solid var(--b2)' }}
                      onMouseEnter={e => e.currentTarget.style.background = 'var(--bg2)'}
                      onMouseLeave={e => e.currentTarget.style.background = 'none'}>
                      <td style={{ padding: '9px 14px', fontSize: 12, fontWeight: 500, color: 'var(--t1)' }}>{l.contact}</td>
                      <td style={{ padding: '9px 14px', fontSize: 11, color: 'var(--t2)' }}>{l.title || '—'}</td>
                      <td style={{ padding: '9px 14px', fontSize: 11, color: 'var(--t3)', fontFamily: 'var(--mono)' }}>{l.email || '—'}</td>
                      <td style={{ padding: '9px 14px', fontSize: 11, color: 'var(--t2)' }}>{l.channel}</td>
                      <td style={{ padding: '9px 14px' }}>
                        {editLead === l.id ? (
                          <select defaultValue={l.status} onChange={e => updateStatus(l.id, e.target.value)}
                            style={{ background: 'var(--bg3)', border: '1px solid var(--b1)', borderRadius: 'var(--r1)', padding: '3px 6px', fontSize: 11, color: 'var(--t1)', fontFamily: 'var(--font)' }}>
                            {STATUS_OPTS.map(o => <option key={o}>{o}</option>)}
                          </select>
                        ) : (
                          <span style={{ fontSize: 10, padding: '2px 8px', borderRadius: 8, color: STATUS_COLOR[l.status] || 'var(--t3)', background: `${STATUS_COLOR[l.status] || 'var(--t4)'}22`, cursor: 'pointer' }}
                            onClick={() => setEditLead(l.id)}>{l.status}</span>
                        )}
                      </td>
                      <td style={{ padding: '9px 14px', fontSize: 10, color: 'var(--t4)' }}>
                        {new Date(l.createdAt).toLocaleDateString('en-GB', { day: '2-digit', month: 'short' })}
                      </td>
                      <td style={{ padding: '9px 14px' }}>
                        <button onClick={() => setEditLead(editLead === l.id ? null : l.id)} style={{ fontSize: 10, color: 'var(--t4)', background: 'none', border: 'none', cursor: 'pointer' }}>Edit</button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>

            {/* UTM footer */}
            <div style={{ padding: '10px 20px', borderTop: '1px solid var(--b2)', background: 'var(--bg1)', fontSize: 11, color: 'var(--t3)', display: 'flex', alignItems: 'center', gap: 10 }}>
              <span>UTM:</span>
              <code style={{ fontFamily: 'var(--mono)', fontSize: 10, background: 'var(--bg3)', padding: '2px 8px', borderRadius: 4, color: 'var(--t2)' }}>
                ?utm_source=agency_outreach&utm_medium=email&utm_campaign={activeCampaign.company.toLowerCase().replace(/\s+/g, '_')}
              </code>
              <button onClick={() => navigator.clipboard.writeText(`?utm_source=agency_outreach&utm_medium=email&utm_campaign=${activeCampaign.company.toLowerCase().replace(/\s+/g, '_')}`)}
                style={{ fontSize: 10, color: 'var(--t4)', background: 'none', border: 'none', cursor: 'pointer' }}>Copy</button>
            </div>
          </>
        )}
      </div>
    </div>
  )
}
