import { useState, useCallback, useEffect, useRef } from 'react'
import { useApp } from '../App.jsx'

// Company Research sections
const SECTIONS = [
  { id: 'overview',       num: '01', title: 'Company Overview',       priority: false },
  { id: 'market',         num: '02', title: 'Market Position',        priority: false },
  { id: 'competitors',    num: '03', title: 'Competitor Mapping',     priority: false },
  { id: 'research',       num: '04', title: 'Deep Market Research',   priority: true  },
  { id: 'activity',       num: '05', title: 'Brand Activity 12–24M',  priority: false },
  { id: 'events',         num: '06', title: 'Experiential & Events',  priority: false },
  { id: 'watchouts',      num: '07', title: 'Strategic Watchouts',    priority: false },
  { id: 'decisionmakers', num: '08', title: 'Decision-Maker Intel',   priority: true  },
  { id: 'contacts',       num: '09', title: 'Contact Intelligence',   priority: true  },
  { id: 'outreach',       num: '10', title: 'Personalized Outreach',  priority: true  },
  { id: 'tracking',       num: '11', title: 'Outreach Tracking Plan', priority: true  },
]

// Industry Discovery sections
const INDUSTRY_SECTIONS = [
  { id: 'brands',   num: '01', title: 'Finding brands...',            priority: true },
  { id: 'events',   num: '02', title: 'Finding events...',            priority: true },
  { id: 'contacts', num: '03', title: 'Finding stakeholders...',      priority: true },
  { id: 'activity', num: '04', title: 'Collecting recent activity...', priority: false },
  { id: 'outreach', num: '05', title: 'Generating outreach...',       priority: true },
  { id: 'scores',   num: '06', title: 'Calculating scores...',        priority: true },
]

const STATUS_COLOR = { done: 'var(--green)', running: 'var(--amber)', error: 'var(--red)' }
const STATUS_LABEL = { done: 'Done', running: 'Analyzing…', error: 'Error', '': 'Queued' }

// ── Helpers ───────────────────────────────────────────────────────────────────
function tryJSON(text) {
  try {
    const m = text.match(/\[[\s\S]*\]|\{[\s\S]*\}/)
    return m ? JSON.parse(m[0]) : null
  } catch {
    return null
  }
}

function ensureParsed(data) {
  if (!data) return null
  if (typeof data === 'string') {
    try {
      let clean = data.strip ? data.strip() : data.trim()
      if (clean.startsWith('```')) {
        clean = clean.replace(/^```(?:json)?\n/, '').replace(/\n```$/, '')
      }
      return JSON.parse(clean)
    } catch {
      // Fallback: try parsing regex blocks
      return tryJSON(data)
    }
  }
  return data
}

function copy(text) {
  navigator.clipboard.writeText(text).catch(() => {})
}

// ── Renders a plain object as a key/value table ───────────────────────────────
function ObjectTable({ obj, depth = 0 }) {
  if (!obj) return null
  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 4 }}>
      {Object.entries(obj).map(([k, v]) => {
        const label = k.replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase())
        if (v === null || v === undefined || v === '') return null
        if (typeof v === 'object' && !Array.isArray(v)) {
          return (
            <div key={k} style={{ marginBottom: 6 }}>
              <div style={{ fontSize: 10, color: 'var(--t3)', fontWeight: 600, letterSpacing: .4, marginBottom: 4, textTransform: 'uppercase' }}>{label}</div>
              <div style={{ paddingLeft: 10, borderLeft: '2px solid var(--b1)' }}>
                <ObjectTable obj={v} depth={depth + 1} />
              </div>
            </div>
          )
        }
        if (Array.isArray(v)) {
          return (
            <div key={k} style={{ marginBottom: 6 }}>
              <div style={{ fontSize: 10, color: 'var(--t3)', fontWeight: 600, letterSpacing: .4, marginBottom: 4, textTransform: 'uppercase' }}>{label}</div>
              <div style={{ paddingLeft: 10, borderLeft: '2px solid var(--b1)' }}>
                {v.map((item, i) => (
                  <div key={i} style={{ fontSize: 12, color: 'var(--t1)', lineHeight: 1.6, marginBottom: 3 }}>
                    {typeof item === 'object' ? <ObjectTable obj={item} depth={depth + 1} /> : `• ${String(item)}`}
                  </div>
                ))}
              </div>
            </div>
          )
        }
        return (
          <div key={k} style={{ display: 'flex', gap: 8, flexWrap: 'wrap' }}>
            <span style={{ fontSize: 11, color: 'var(--t3)', minWidth: 110, flexShrink: 0 }}>{label}</span>
            <span style={{ fontSize: 12, color: 'var(--t1)', lineHeight: 1.6, flex: 1 }}>{String(v)}</span>
          </div>
        )
      })}
    </div>
  )
}

// ── Original Company Research Components ──────────────────────────────────────
function ProseBody({ text }) {
  const d = tryJSON(text)

  if (d && Array.isArray(d) && d.length > 0 && typeof d[0] === 'object') {
    return (
      <div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
        {d.map((item, i) => (
          <div key={i} style={{ border: '1px solid var(--b1)', borderRadius: 'var(--r2)', padding: '12px 14px' }}>
            {(() => {
              const titleKey = Object.keys(item).find(k => typeof item[k] === 'string' && item[k].length < 80)
              const title = titleKey ? item[titleKey] : null
              const rest = titleKey ? Object.fromEntries(Object.entries(item).filter(([k]) => k !== titleKey)) : item
              return (
                <>
                  {title && <div style={{ fontSize: 13, fontWeight: 600, color: 'var(--t1)', marginBottom: 8 }}>{title}</div>}
                  <ObjectTable obj={rest} />
                </>
              )
            })()}
          </div>
        ))}
      </div>
    )
  }

  if (d && typeof d === 'object' && !Array.isArray(d)) {
    return <div style={{ border: '1px solid var(--b1)', borderRadius: 'var(--r2)', padding: '12px 14px' }}><ObjectTable obj={d} /></div>
  }

  return (
    <pre style={{
      fontFamily: 'var(--font)', fontSize: 12, lineHeight: 1.85,
      color: 'var(--t1)', whiteSpace: 'pre-wrap', wordBreak: 'break-word', margin: 0
    }}>
      {text}
    </pre>
  )
}

function CompetitorBody({ text }) {
  const d = tryJSON(text)
  if (!d || !Array.isArray(d)) return <ProseBody text={text} />
  return (
    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit,minmax(160px,1fr))', gap: 10 }}>
      {d.map((c, i) => (
        <div key={i} style={{ border: '1px solid var(--b1)', borderRadius: 'var(--r2)', padding: 12 }}>
          <div style={{ fontSize: 13, fontWeight: 600, marginBottom: 6, color: 'var(--t1)' }}>{c.name}</div>
          <div style={{ display: 'flex', gap: 4, flexWrap: 'wrap', marginBottom: 8 }}>
            {c.strength && <span style={{ fontSize: 10, background: 'rgba(62,207,142,.1)', color: 'var(--green)', padding: '1px 7px', borderRadius: 8 }}>{c.strength}</span>}
            {c.gap && <span style={{ fontSize: 10, background: 'rgba(245,166,35,.1)', color: 'var(--amber)', padding: '1px 7px', borderRadius: 8 }}>{c.gap}</span>}
          </div>
          {c.strategy && <div style={{ fontSize: 11, color: 'var(--t2)', lineHeight: 1.55 }}>{c.strategy}</div>}
          {c.activity && <div style={{ fontSize: 10, color: 'var(--t3)', marginTop: 4, fontStyle: 'italic' }}>{c.activity}</div>}
        </div>
      ))}
    </div>
  )
}

function WatchoutsBody({ text }) {
  const d = tryJSON(text)
  if (!d || !Array.isArray(d)) return <ProseBody text={text} />
  return (
    <div>
      {d.map((w, i) => (
        <div key={i} style={{ display: 'flex', gap: 10, padding: '10px 0', borderBottom: i < d.length - 1 ? '1px solid var(--b2)' : 'none' }}>
          <div style={{ width: 18, height: 18, borderRadius: '50%', background: 'rgba(245,166,35,.15)', color: 'var(--amber)', fontSize: 9, fontWeight: 700, display: 'flex', alignItems: 'center', justifyContent: 'center', flexShrink: 0, marginTop: 2 }}>!</div>
          <div style={{ fontSize: 12, lineHeight: 1.65 }}>
            <span style={{ fontWeight: 600, color: 'var(--t1)' }}>{w.risk}</span>
            {w.detail && <span style={{ color: 'var(--t2)' }}>: {w.detail}</span>}
          </div>
        </div>
      ))}
    </div>
  )
}

function DMBody({ text }) {
  const d = tryJSON(text)
  if (!d || !Array.isArray(d)) return <ProseBody text={text} />
  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>
      {d.map((p, i) => {
        const init = (p.name || p.title || 'DM').split(' ').slice(0, 2).map(w => w[0] || '').join('').toUpperCase()
        const liQuery = encodeURIComponent(`${p.name || ''} ${p.department || ''}`.trim())
        return (
          <div key={i} style={{ border: '1px solid var(--b1)', borderRadius: 'var(--r2)', padding: 12, display: 'flex', gap: 10 }}>
            <div style={{ width: 32, height: 32, borderRadius: '50%', background: 'rgba(124,109,250,.15)', color: 'var(--accent2)', fontSize: 11, fontWeight: 600, display: 'flex', alignItems: 'center', justifyContent: 'center', flexShrink: 0 }}>{init}</div>
            <div style={{ flex: 1 }}>
              <div style={{ fontWeight: 600, color: 'var(--t1)' }}>{p.name || 'Stakeholder'}</div>
              <div style={{ fontSize: 11, color: 'var(--t3)', marginBottom: 5 }}>
                {[p.title, p.department, p.seniority].filter(Boolean).join(' · ')}
              </div>
              {p.relevance && <div style={{ fontSize: 12, color: 'var(--t2)', lineHeight: 1.5, marginBottom: 4 }}>{p.relevance}</div>}
              {p.angle && <div style={{ fontSize: 11, color: 'var(--t3)', fontStyle: 'italic' }}>Angle: {p.angle}</div>}
              <div style={{ marginTop: 8, display: 'flex', gap: 6 }}>
                <a href={`https://www.linkedin.com/search/results/people/?keywords=${liQuery}`} target="_blank" rel="noreferrer"
                  style={{ fontSize: 10, padding: '2px 8px', border: '1px solid var(--b1)', borderRadius: 4, color: 'var(--t3)', textDecoration: 'none' }}>
                  Find on LinkedIn
                </a>
                <button onClick={() => copy(`${p.title} at the company`)} style={{ fontSize: 10, padding: '2px 8px', border: '1px solid var(--b1)', borderRadius: 4, color: 'var(--t3)', background: 'none', cursor: 'pointer' }}>
                  Copy title
                </button>
              </div>
            </div>
          </div>
        )
      })}
    </div>
  )
}

function ContactsBody({ text }) {
  const d = tryJSON(text)
  if (!d || !Array.isArray(d)) return <ProseBody text={text} />
  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>
      {d.map((c, i) => {
        const init = (c.name || 'C').split(' ').slice(0, 2).map(w => w[0] || '').join('').toUpperCase()
        return (
          <div key={i} style={{ border: '1px solid var(--b1)', borderRadius: 'var(--r2)', padding: 14 }}>
            <div style={{ display: 'flex', gap: 10, marginBottom: 10 }}>
              <div style={{ width: 36, height: 36, borderRadius: '50%', background: 'rgba(62,207,142,.12)', color: 'var(--green)', fontSize: 12, fontWeight: 600, display: 'flex', alignItems: 'center', justifyContent: 'center', flexShrink: 0 }}>{init}</div>
              <div>
                <div style={{ fontWeight: 600, fontSize: 13, color: 'var(--t1)' }}>{c.name || 'Contact'}</div>
                <div style={{ fontSize: 11, color: 'var(--t3)' }}>{[c.title, c.company, c.location].filter(Boolean).join(' · ')}</div>
              </div>
            </div>
            <div style={{ display: 'flex', flexDirection: 'column', gap: 5 }}>
              {c.email && (
                <div style={{ display: 'flex', gap: 8, alignItems: 'center' }}>
                  <span style={{ fontSize: 10, color: 'var(--t4)', minWidth: 60 }}>Email</span>
                  <a href={`mailto:${c.email}`} style={{ fontSize: 12, color: 'var(--accent)', textDecoration: 'none' }}>{c.email}</a>
                  <button onClick={() => copy(c.email)} style={{ fontSize: 10, padding: '1px 6px', border: '1px solid var(--b1)', borderRadius: 4, color: 'var(--t4)', background: 'none', cursor: 'pointer' }}>copy</button>
                </div>
              )}
              {c.phone && (
                <div style={{ display: 'flex', gap: 8, alignItems: 'center' }}>
                  <span style={{ fontSize: 10, color: 'var(--t4)', minWidth: 60 }}>Phone</span>
                  <span style={{ fontSize: 12, color: 'var(--t1)' }}>{c.phone}</span>
                </div>
              )}
              {c.linkedin && (
                <div style={{ display: 'flex', gap: 8, alignItems: 'center' }}>
                  <span style={{ fontSize: 10, color: 'var(--t4)', minWidth: 60 }}>LinkedIn</span>
                  <a href={c.linkedin.startsWith('http') ? c.linkedin : `https://${c.linkedin}`} target="_blank" rel="noreferrer" style={{ fontSize: 12, color: 'var(--accent)', textDecoration: 'none' }}>View profile ↗</a>
                </div>
              )}
              {c.notes && <div style={{ fontSize: 11, color: 'var(--t3)', marginTop: 4, fontStyle: 'italic', borderTop: '1px solid var(--b2)', paddingTop: 6 }}>{c.notes}</div>}
              {c.best_time && <div style={{ fontSize: 11, color: 'var(--t3)' }}>Best time: {c.best_time}</div>}
              {c.confidence && (
                <div style={{ display: 'flex', gap: 8, alignItems: 'center', marginTop: 2 }}>
                  <span style={{ fontSize: 10, color: 'var(--t4)', minWidth: 60 }}>Confidence</span>
                  <span style={{ fontSize: 11, padding: '1px 7px', borderRadius: 8, background: c.confidence === 'high' ? 'rgba(62,207,142,.1)' : c.confidence === 'medium' ? 'rgba(245,166,35,.1)' : 'var(--bg3)', color: c.confidence === 'high' ? 'var(--green)' : c.confidence === 'medium' ? 'var(--amber)' : 'var(--t3)' }}>{c.confidence}</span>
                </div>
              )}
            </div>
          </div>
        )
      })}
    </div>
  )
}

function TrackingBody({ text }) {
  const d = tryJSON(text)
  if (!d) return <ProseBody text={text} />

  const steps = Array.isArray(d) ? d : d.steps || d.timeline || d.plan || Object.values(d)

  if (Array.isArray(steps) && steps.length > 0 && typeof steps[0] === 'object') {
    return (
      <div style={{ display: 'flex', flexDirection: 'column', gap: 0 }}>
        {steps.map((step, i) => {
          const dayKey = Object.keys(step).find(k => /day|date|week|step|phase/i.test(k))
          const titleKey = Object.keys(step).find(k => /title|action|task|name|subject/i.test(k))
          const day = dayKey ? step[dayKey] : `Step ${i + 1}`
          const title = titleKey ? step[titleKey] : null
          const rest = Object.fromEntries(Object.entries(step).filter(([k]) => k !== dayKey && k !== titleKey))

          return (
            <div key={i} style={{ display: 'flex', gap: 12, paddingBottom: 16 }}>
              <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', width: 32, flexShrink: 0 }}>
                <div style={{ width: 28, height: 28, borderRadius: '50%', background: 'var(--bg3)', border: '2px solid var(--accent)', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: 9, fontWeight: 700, color: 'var(--accent)', flexShrink: 0 }}>{i + 1}</div>
                {i < steps.length - 1 && <div style={{ width: 1, flex: 1, background: 'var(--b1)', marginTop: 4 }}></div>}
              </div>
              <div style={{ flex: 1, paddingTop: 4 }}>
                <div style={{ fontSize: 10, color: 'var(--t4)', fontWeight: 600, letterSpacing: .4, marginBottom: 3, textTransform: 'uppercase' }}>{day}</div>
                {title && <div style={{ fontSize: 13, fontWeight: 600, color: 'var(--t1)', marginBottom: 6 }}>{title}</div>}
                <ObjectTable obj={rest} />
              </div>
            </div>
          )
        })}
      </div>
    )
  }

  if (typeof d === 'object' && !Array.isArray(d)) {
    return <div style={{ border: '1px solid var(--b1)', borderRadius: 'var(--r2)', padding: '12px 14px' }}><ObjectTable obj={d} /></div>
  }

  return <ProseBody text={text} />
}

function CopyBtn({ label, onClick, copied }) {
  return (
    <button onClick={onClick} style={{
      fontSize: 11, padding: '5px 10px', cursor: 'pointer', fontFamily: 'var(--font)',
      border: `1px solid ${copied ? 'var(--green)' : 'var(--b1)'}`,
      borderRadius: 'var(--r1)', background: 'none',
      color: copied ? 'var(--green)' : 'var(--t3)'
    }}>
      {copied ? '✓ Copied' : label}
    </button>
  )
}

function parseOutreachText(text) {
  const HEADERS = [
    'LINKEDIN MESSAGE',
    'EMAIL SUBJECT',
    'EMAIL BODY',
    'FOLLOW-UP LINKEDIN',
    'FOLLOW-UP EMAIL SUBJECT',
    'FOLLOW-UP EMAIL BODY',
  ]
  const result = {}
  const lines = text.split('\n')
  let currentKey = null
  let buffer = []
  const flush = () => {
    if (currentKey) result[currentKey] = buffer.join('\n').trim()
  }
  for (const raw of lines) {
    const line = raw.trim()
    const matched = HEADERS.find(h => line.toUpperCase().startsWith(h))
    if (matched) {
      flush()
      currentKey = matched
      buffer = []
    } else if (currentKey) {
      buffer.push(raw)
    }
  }
  flush()
  return result
}

function OutreachBody({ text }) {
  const [tab, setTab] = useState('linkedin')
  const [copied, setCopied] = useState('')

  const d = parseOutreachText(text)
  const linkedin    = d['LINKEDIN MESSAGE'] || ''
  const emailSubj   = d['EMAIL SUBJECT'] || ''
  const emailBody   = d['EMAIL BODY'] || ''
  const fuLinkedin  = d['FOLLOW-UP LINKEDIN'] || ''
  const fuEmailSubj = d['FOLLOW-UP EMAIL SUBJECT'] || ''
  const fuEmailBody = d['FOLLOW-UP EMAIL BODY'] || ''

  if (!linkedin && !emailSubj && !emailBody) return <ProseBody text={text} />

  const doCopy = (key, val) => {
    copy(val || '')
    setCopied(key)
    setTimeout(() => setCopied(''), 2000)
  }

  const tabStyle = (id) => ({
    padding: '6px 14px', fontSize: 11, cursor: 'pointer',
    borderBottom: tab === id ? '2px solid var(--accent2)' : '2px solid transparent',
    color: tab === id ? 'var(--t1)' : 'var(--t3)',
    background: 'none', border: 'none',
    fontFamily: 'var(--font)', fontWeight: tab === id ? 600 : 400
  })

  const boxStyle = {
    background: 'var(--bg2)', borderRadius: 'var(--r2)',
    padding: '12px 14px', fontSize: 12, lineHeight: 1.8,
    color: 'var(--t1)', whiteSpace: 'pre-wrap', marginBottom: 8, wordBreak: 'break-word'
  }

  return (
    <div>
      <div style={{ display: 'flex', borderBottom: '1px solid var(--b1)', marginBottom: 16, gap: 2 }}>
        {['linkedin', 'email', 'followup'].map(t => (
          <button key={t} style={tabStyle(t)} onClick={() => setTab(t)}>
            {t === 'linkedin' ? '💼 LinkedIn' : t === 'email' ? '✉️ Email' : '🔁 Follow-ups'}
          </button>
        ))}
      </div>

      {tab === 'linkedin' && (
        <div>
          <div style={{ fontSize: 10, color: 'var(--t3)', marginBottom: 6, letterSpacing: .4, fontWeight: 600 }}>
            CONNECTION MESSAGE · {linkedin.length} CHARS
          </div>
          <div style={boxStyle}>{linkedin || 'Not generated'}</div>
          <div style={{ display: 'flex', gap: 6 }}>
            <CopyBtn label="Copy message" onClick={() => doCopy('li', linkedin)} copied={copied === 'li'} />
            <a href="https://www.linkedin.com/messaging/" target="_blank" rel="noreferrer"
              style={{ fontSize: 11, padding: '5px 10px', border: '1px solid var(--b1)', borderRadius: 'var(--r1)', color: 'var(--t3)', textDecoration: 'none' }}>
              Open LinkedIn ↗
            </a>
          </div>
        </div>
      )}

      {tab === 'email' && (
        <div>
          <div style={{ fontSize: 10, color: 'var(--t3)', marginBottom: 5, letterSpacing: .4, fontWeight: 600 }}>SUBJECT LINE</div>
          <div style={{ ...boxStyle, fontWeight: 600, padding: '8px 12px', marginBottom: 12 }}>{emailSubj || 'Not generated'}</div>
          <div style={{ fontSize: 10, color: 'var(--t3)', marginBottom: 5, letterSpacing: .4, fontWeight: 600 }}>EMAIL BODY</div>
          <div style={boxStyle}>{emailBody || 'Not generated'}</div>
          <div style={{ display: 'flex', gap: 6 }}>
            <CopyBtn label="Copy email" onClick={() => doCopy('em', `Subject: ${emailSubj}\n\n${emailBody}`)} copied={copied === 'em'} />
            <a href={`mailto:?subject=${encodeURIComponent(emailSubj)}&body=${encodeURIComponent(emailBody)}`}
              style={{ fontSize: 11, padding: '5px 10px', border: '1px solid var(--b1)', borderRadius: 'var(--r1)', color: 'var(--t3)', textDecoration: 'none' }}>
              Open in Mail ↗
            </a>
          </div>
        </div>
      )}

      {tab === 'followup' && (
        <div>
          <div style={{ fontSize: 10, color: 'var(--t3)', marginBottom: 5, letterSpacing: .4, fontWeight: 600 }}>LINKEDIN FOLLOW-UP · DAY 5</div>
          <div style={boxStyle}>{fuLinkedin || 'Not generated'}</div>
          <CopyBtn label="Copy LinkedIn follow-up" onClick={() => doCopy('fuli', fuLinkedin)} copied={copied === 'fuli'} />
          <div style={{ height: 14 }} />
          <div style={{ fontSize: 10, color: 'var(--t3)', marginBottom: 5, letterSpacing: .4, fontWeight: 600 }}>EMAIL FOLLOW-UP SUBJECT · DAY 8</div>
          <div style={{ ...boxStyle, fontWeight: 600, padding: '8px 12px', marginBottom: 10 }}>{fuEmailSubj || 'Not generated'}</div>
          <div style={{ fontSize: 10, color: 'var(--t3)', marginBottom: 5, letterSpacing: .4, fontWeight: 600 }}>EMAIL FOLLOW-UP BODY · DAY 8</div>
          <div style={boxStyle}>{fuEmailBody || 'Not generated'}</div>
          <CopyBtn label="Copy follow-up email" onClick={() => doCopy('fuem', `Subject: ${fuEmailSubj}\n\n${fuEmailBody}`)} copied={copied === 'fuem'} />
        </div>
      )}
    </div>
  )
}

// ── UPGRADED: Source / Trust Score Badge ─────────────────────────────────────
function SourceTrustBadge({ confidence, url, type }) {
  const cColor = confidence === 'HIGH' ? 'var(--green)' : confidence === 'MEDIUM' ? 'var(--amber)' : 'var(--red)'
  return (
    <div style={{ display: 'flex', flexWrap: 'wrap', gap: 4, alignItems: 'center', marginTop: 4 }}>
      <span style={{ fontSize: 9, padding: '1px 6px', borderRadius: 4, background: `${cColor}18`, color: cColor, border: `1px solid ${cColor}30`, fontWeight: 600 }}>
        {confidence} Trust
      </span>
      {url && url !== 'Public information unavailable' ? (
        <a href={url} target="_blank" rel="noreferrer" style={{
          fontSize: 9, padding: '1px 6px', borderRadius: 4, background: 'rgba(124,109,250,.1)',
          color: 'var(--accent2)', border: '1px solid rgba(124,109,250,.2)', textDecoration: 'none',
          whiteSpace: 'nowrap'
        }}>
          {type || 'Source'} ↗
        </a>
      ) : (
        <span style={{ fontSize: 9, padding: '1px 6px', borderRadius: 4, background: 'var(--bg3)', color: 'var(--t4)' }}>
          Unsourced
        </span>
      )}
    </div>
  )
}

// ── UPGRADED: Industry Discovery Rendering Components ──────────────────────────
function IndustryBrandsBody({ text, notify }) {
  const brands = ensureParsed(text)
  if (!brands || !Array.isArray(brands) || brands.length === 0) {
    return <div style={{ fontSize: 12, color: 'var(--t3)', padding: 14, textAlign: 'center', fontWeight: 500 }}>Public information unavailable</div>
  }

  const addCampaign = async (brandName) => {
    try {
      const res = await fetch('/api/tracking/campaigns', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ company: brandName })
      })
      if (res.ok) {
        notify(`Created campaign for ${brandName}! Log contacts in Tracking.`, 'success')
      } else {
        notify('Failed to create campaign', 'error')
      }
    } catch {
      notify('Failed to create campaign', 'error')
    }
  }

  return (
    <div style={{ overflowX: 'auto', border: '1px solid var(--b1)', borderRadius: 'var(--r2)', background: 'var(--bg2)' }}>
      <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left', minWidth: 600 }}>
        <thead>
          <tr style={{ background: 'var(--bg3)', borderBottom: '1px solid var(--b1)' }}>
            {['Rank & Brand', 'Strategic Alignment (StepOne)', 'Scores', 'Trust / Source', 'Action'].map(h => (
              <th key={h} style={{ padding: '10px 14px', fontSize: 10, color: 'var(--t3)', fontWeight: 600, letterSpacing: .5 }}>{h}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {brands.map((b, idx) => {
            const overall = b.overall_score || 0
            const scoreColor = overall >= 85 ? 'var(--green)' : overall >= 65 ? 'var(--amber)' : 'var(--red)'
            
            return (
              <tr key={idx} style={{ borderBottom: '1px solid var(--b1)' }}>
                {/* Brand & Score */}
                <td style={{ padding: '12px 14px' }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
                    <span style={{ fontSize: 11, color: 'var(--t3)', fontFamily: 'var(--mono)', width: 14 }}>{String(idx + 1).padStart(2, '0')}</span>
                    <div>
                      <div style={{ fontSize: 13, fontWeight: 600, color: 'var(--t1)' }}>{b.brand_name}</div>
                      <div style={{ display: 'flex', alignItems: 'center', gap: 4, marginTop: 2 }}>
                        <span style={{ width: 6, height: 6, borderRadius: '50%', background: scoreColor }} />
                        <span style={{ fontSize: 10, color: 'var(--t2)', fontWeight: 500 }}>Overall: {overall}</span>
                      </div>
                    </div>
                  </div>
                </td>
                
                {/* Alignment Details */}
                <td style={{ padding: '12px 14px', maxWidth: 300 }}>
                  <div style={{ fontSize: 11, color: 'var(--t2)', lineHeight: 1.5 }}>
                    <strong style={{ color: 'var(--t1)' }}>Why StepOne:</strong> {b.why_stepone}
                  </div>
                  <div style={{ fontSize: 11, color: 'var(--t2)', lineHeight: 1.5, marginTop: 4 }}>
                    <strong style={{ color: 'var(--t1)' }}>Why Now:</strong> {b.why_now}
                  </div>
                </td>
                
                {/* Score Stack */}
                <td style={{ padding: '12px 14px', fontSize: 10, fontFamily: 'var(--mono)', color: 'var(--t3)' }}>
                  <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '3px 8px' }}>
                    <div><span style={{ color: 'var(--accent2)' }}>SF:</span> <span style={{ color: 'var(--t2)' }}>{b.strategic_fit_score}</span></div>
                    <div><span style={{ color: 'var(--purple)' }}>GS:</span> <span style={{ color: 'var(--t2)' }}>{b.growth_signal_score}</span></div>
                    <div><span style={{ color: 'var(--blue)' }}>EP:</span> <span style={{ color: 'var(--t2)' }}>{b.event_presence_score}</span></div>
                    <div><span style={{ color: 'var(--green)' }}>RA:</span> <span style={{ color: 'var(--t2)' }}>{b.recent_activity_score}</span></div>
                  </div>
                </td>
                
                {/* Trust and Verification */}
                <td style={{ padding: '12px 14px' }}>
                  <SourceTrustBadge 
                    confidence={b.confidence_label || 'HIGH'} 
                    url={b.source_url} 
                    type={b.source_type || 'Official Website'} 
                  />
                </td>
                
                {/* Direct Action CRM */}
                <td style={{ padding: '12px 14px' }}>
                  <button onClick={() => addCampaign(b.brand_name)} style={{
                    padding: '4px 10px', background: 'none', border: '1px solid var(--accent)',
                    borderRadius: 'var(--r1)', color: 'var(--accent2)', fontSize: 10, cursor: 'pointer',
                    fontWeight: 500, whiteSpace: 'nowrap'
                  }}>
                    + Target
                  </button>
                </td>
              </tr>
            )
          })}
        </tbody>
      </table>
    </div>
  )
}

function IndustryEventsBody({ text }) {
  const events = ensureParsed(text)
  if (!events || !Array.isArray(events)) return <ProseBody text={text} />
  if (events.length === 0) return <div style={{ fontSize: 11, color: 'var(--t3)', textAlign: 'center', padding: '16px' }}>No upcoming events found publicly.</div>

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 14 }}>
      {events.map((e, idx) => (
        <div key={idx} style={{ background: 'var(--bg2)', border: '1px solid var(--b1)', borderRadius: 'var(--r2)', padding: 16 }}>
          {/* Header row */}
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: 8, gap: 8, flexWrap: 'wrap' }}>
            <div>
              <div style={{ fontSize: 13, fontWeight: 700, color: 'var(--t1)' }}>{e.event_name}</div>
              <div style={{ display: 'flex', gap: 12, marginTop: 4, fontSize: 11, color: 'var(--t2)', flexWrap: 'wrap' }}>
                <span>📅 {e.date || 'TBD'}</span>
                <span>📍 {e.location || 'TBD'}</span>
                {e.expected_attendance && e.expected_attendance !== 'Not publicly listed' && (
                  <span>👥 {e.expected_attendance} attendees</span>
                )}
              </div>
            </div>
            {/* Sponsorship badge */}
            {e.sponsorship_available && (
              <span style={{
                fontSize: 9, fontWeight: 700, letterSpacing: .5, padding: '3px 8px',
                borderRadius: 10, flexShrink: 0,
                background: e.sponsorship_available === 'Yes' ? 'rgba(72,199,142,.15)' : 'rgba(255,255,255,.05)',
                color: e.sponsorship_available === 'Yes' ? 'var(--green)' : 'var(--t4)',
                border: `1px solid ${e.sponsorship_available === 'Yes' ? 'rgba(72,199,142,.3)' : 'var(--b2)'}`,
              }}>
                {e.sponsorship_available === 'Yes' ? '✓ SPONSORSHIP OPEN' : 'SPONSORSHIP: ' + e.sponsorship_available}
              </span>
            )}
          </div>

          {/* Description */}
          {e.description && e.description !== 'Not publicly listed' && (
            <div style={{ fontSize: 11, color: 'var(--t2)', lineHeight: 1.6, marginBottom: 10 }}>{e.description}</div>
          )}

          {/* Why StepOne should attend */}
          {e.why_stepone_should_attend && e.why_stepone_should_attend !== 'Not publicly listed' && (
            <div style={{
              background: 'rgba(124,109,250,.07)', border: '1px solid rgba(124,109,250,.18)',
              borderRadius: 'var(--r1)', padding: '7px 10px', marginBottom: 10
            }}>
              <span style={{ fontSize: 9, fontWeight: 700, color: 'var(--accent2)', letterSpacing: .4 }}>WHY STEPONE SHOULD ATTEND  </span>
              <span style={{ fontSize: 11, color: 'var(--t2)' }}>{e.why_stepone_should_attend}</span>
            </div>
          )}

          {/* Likely attending brands */}
          {e.likely_participating_brands && (
            <div style={{ marginBottom: 10 }}>
              <div style={{ fontSize: 9, color: 'var(--t3)', fontWeight: 600, letterSpacing: .3, marginBottom: 5 }}>PROSPECTS LIKELY PRESENT</div>
              <div style={{ display: 'flex', flexWrap: 'wrap', gap: 4 }}>
                {(Array.isArray(e.likely_participating_brands)
                  ? e.likely_participating_brands
                  : e.likely_participating_brands.split(',')
                ).map((b, i) => (
                  <span key={i} style={{ fontSize: 10, background: 'var(--bg3)', border: '1px solid var(--b2)', padding: '2px 8px', borderRadius: 4, color: 'var(--t2)' }}>
                    {b.trim()}
                  </span>
                ))}
              </div>
            </div>
          )}

          <SourceTrustBadge
            confidence={e.confidence_score || e.confidence_label || 'HIGH'}
            url={e.official_url || e.source_url}
            type="Official Event Site"
          />
        </div>
      ))}
    </div>
  )
}

function IndustryContactsBody({ text }) {
  const contacts = ensureParsed(text)
  const [copiedId, setCopiedId] = useState('')
  
  if (!contacts || !Array.isArray(contacts)) return <ProseBody text={text} />
  if (contacts.length === 0) return <div style={{ fontSize: 11, color: 'var(--t3)', textAlign: 'center', padding: '16px' }}>No public decision makers found.</div>

  const isAvailable = v => v && v !== 'Not publicly listed' && v !== 'Public information unavailable'

  const doCopy = (id, val) => { copy(val || ''); setCopiedId(id); setTimeout(() => setCopiedId(''), 2000) }

  // Group by brand
  const grouped = contacts.reduce((acc, c) => {
    const key = c.brand_name || 'Unknown'
    if (!acc[key]) acc[key] = []
    acc[key].push(c)
    return acc
  }, {})

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 20 }}>
      {Object.entries(grouped).map(([brand, people]) => (
        <div key={brand}>
          {/* Brand header */}
          <div style={{ fontSize: 10, fontWeight: 700, color: 'var(--accent2)', letterSpacing: .6, marginBottom: 8, textTransform: 'uppercase' }}>
            {brand}
          </div>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: 10 }}>
            {people.map((c, idx) => {
              const init = (c.name || 'DM').split(' ').slice(0, 2).map(w => w[0] || '').join('').toUpperCase()
              const contactId = `${brand}-${idx}`
              const linkedinSearchUrl = `https://www.linkedin.com/search/results/people/?keywords=${encodeURIComponent((c.name || '') + ' ' + (c.brand_name || brand))}`
              const hasLinkedIn = isAvailable(c.linkedin)
              const hasEmail = isAvailable(c.email) && c.email.includes('@')
              
              return (
                <div key={idx} style={{ background: 'var(--bg2)', border: '1px solid var(--b1)', borderRadius: 'var(--r2)', padding: 14 }}>
                  {/* Person header */}
                  <div style={{ display: 'flex', gap: 10, marginBottom: 12 }}>
                    <div style={{ width: 40, height: 40, borderRadius: '50%', background: 'rgba(124,109,250,.15)', color: 'var(--accent2)', fontSize: 13, fontWeight: 700, display: 'flex', alignItems: 'center', justifyContent: 'center', flexShrink: 0 }}>{init}</div>
                    <div style={{ flex: 1 }}>
                      <div style={{ fontWeight: 600, fontSize: 14, color: 'var(--t1)' }}>{c.name}</div>
                      <div style={{ fontSize: 11, color: 'var(--t3)', marginTop: 1 }}>{c.role}</div>
                      <div style={{ fontSize: 10, color: 'var(--t4)', marginTop: 2 }}>{brand}</div>
                    </div>
                  </div>

                  {/* Contact fields */}
                  <div style={{ display: 'flex', flexDirection: 'column', gap: 8, fontSize: 11, borderBottom: '1px solid var(--b2)', paddingBottom: 12, marginBottom: 10 }}>
                    {/* Email row */}
                    <div style={{ display: 'flex', justifyContent: 'space-between', gap: 8, alignItems: 'center' }}>
                      <span style={{ color: 'var(--t4)', fontWeight: 600, minWidth: 55, fontSize: 10 }}>✉️ Email</span>
                      {hasEmail ? (
                        <div style={{ display: 'flex', gap: 4, alignItems: 'center', flex: 1, justifyContent: 'flex-end' }}>
                          <a href={`mailto:${c.email}`} style={{ color: 'var(--accent2)', textDecoration: 'none', wordBreak: 'break-all', textAlign: 'right', fontSize: 11 }}>{c.email}</a>
                          <button onClick={() => doCopy(`email-${contactId}`, c.email)} style={{ fontSize: 9, padding: '1px 5px', border: '1px solid var(--b1)', borderRadius: 3, background: 'none', color: copiedId === `email-${contactId}` ? 'var(--green)' : 'var(--t4)', cursor: 'pointer', flexShrink: 0 }}>
                            {copiedId === `email-${contactId}` ? '✓' : 'copy'}
                          </button>
                        </div>
                      ) : (
                        <span style={{ color: 'var(--t4)', fontStyle: 'italic', fontSize: 10 }}>Not publicly listed</span>
                      )}
                    </div>
                    {/* Phone row */}
                    <div style={{ display: 'flex', justifyContent: 'space-between', gap: 8, alignItems: 'center' }}>
                      <span style={{ color: 'var(--t4)', fontWeight: 600, minWidth: 55, fontSize: 10 }}>📞 Phone</span>
                      {isAvailable(c.phone) ? (
                        <div style={{ display: 'flex', gap: 4, alignItems: 'center', flex: 1, justifyContent: 'flex-end' }}>
                          <span style={{ color: 'var(--t1)', textAlign: 'right', fontSize: 11 }}>{c.phone}</span>
                          <button onClick={() => doCopy(`phone-${contactId}`, c.phone)} style={{ fontSize: 9, padding: '1px 5px', border: '1px solid var(--b1)', borderRadius: 3, background: 'none', color: copiedId === `phone-${contactId}` ? 'var(--green)' : 'var(--t4)', cursor: 'pointer', flexShrink: 0 }}>
                            {copiedId === `phone-${contactId}` ? '✓' : 'copy'}
                          </button>
                        </div>
                      ) : (
                        <span style={{ color: 'var(--t4)', fontStyle: 'italic', fontSize: 10 }}>Not publicly listed</span>
                      )}
                    </div>
                    {/* LinkedIn row */}
                    <div style={{ display: 'flex', justifyContent: 'space-between', gap: 8, alignItems: 'center' }}>
                      <span style={{ color: 'var(--t4)', fontWeight: 600, minWidth: 55, fontSize: 10 }}>💼 LinkedIn</span>
                      {hasLinkedIn ? (
                        <a href={c.linkedin} target="_blank" rel="noreferrer" style={{ color: 'var(--accent2)', textDecoration: 'none', fontSize: 11 }}>View Profile ↗</a>
                      ) : (
                        <span style={{ color: 'var(--t4)', fontStyle: 'italic', fontSize: 10 }}>Not publicly listed</span>
                      )}
                    </div>
                  </div>

                  {/* ── ACTION BUTTONS: Direct outreach ── */}
                  <div style={{ display: 'flex', gap: 6, flexWrap: 'wrap', marginBottom: 10 }}>
                    {/* LinkedIn Search — always available, searches by name + company */}
                    <a 
                      href={hasLinkedIn ? c.linkedin : linkedinSearchUrl} 
                      target="_blank" rel="noreferrer"
                      style={{
                        fontSize: 10, padding: '5px 10px', borderRadius: 'var(--r1)',
                        background: 'rgba(0,119,181,.12)', border: '1px solid rgba(0,119,181,.3)',
                        color: '#0077B5', textDecoration: 'none', fontWeight: 600,
                        display: 'flex', alignItems: 'center', gap: 4, cursor: 'pointer'
                      }}
                    >
                      <span style={{ fontSize: 12 }}>🔗</span>
                      {hasLinkedIn ? 'Open LinkedIn Profile' : 'Search on LinkedIn'}
                    </a>
                    
                    {/* Direct Email — opens mail client with To: pre-filled */}
                    {hasEmail && (
                      <a 
                        href={`mailto:${c.email}`}
                        style={{
                          fontSize: 10, padding: '5px 10px', borderRadius: 'var(--r1)',
                          background: 'rgba(62,207,142,.1)', border: '1px solid rgba(62,207,142,.3)',
                          color: 'var(--green)', textDecoration: 'none', fontWeight: 600,
                          display: 'flex', alignItems: 'center', gap: 4, cursor: 'pointer'
                        }}
                      >
                        <span style={{ fontSize: 12 }}>📧</span>
                        Send Email
                      </a>
                    )}

                    {/* Search LinkedIn by name+company — always available as fallback */}
                    {!hasLinkedIn && (
                      <a 
                        href={linkedinSearchUrl} 
                        target="_blank" rel="noreferrer"
                        style={{
                          fontSize: 10, padding: '5px 10px', borderRadius: 'var(--r1)',
                          background: 'rgba(124,109,250,.08)', border: '1px solid rgba(124,109,250,.2)',
                          color: 'var(--accent2)', textDecoration: 'none', fontWeight: 500,
                          display: 'flex', alignItems: 'center', gap: 4, cursor: 'pointer'
                        }}
                      >
                        <span style={{ fontSize: 12 }}>🔍</span>
                        Find {c.name?.split(' ')[0] || 'Contact'} on LinkedIn
                      </a>
                    )}
                  </div>

                  <SourceTrustBadge
                    confidence={c.confidence_label || 'MEDIUM'}
                    url={c.source_url}
                    type="Web / LinkedIn"
                  />
                </div>
              )
            })}
          </div>
        </div>
      ))}
    </div>
  )
}

function IndustryActivityBody({ text }) {
  const activities = ensureParsed(text)
  if (!activities || !Array.isArray(activities)) return <ProseBody text={text} />
  if (activities.length === 0) return <div style={{ fontSize: 11, color: 'var(--t3)', textAlign: 'center', padding: '16px' }}>No recent activity found.</div>

  const typeColor = {
    'Funding': 'var(--green)', 'Product Launch': 'var(--accent2)', 'Campaign': 'var(--purple)',
    'Partnership': 'var(--blue)', 'Expansion': 'var(--amber)', 'Rebrand': 'var(--accent)',
    'Executive Hire': 'var(--t2)', 'Other': 'var(--t3)',
  }

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
      {activities.map((a, idx) => {
        const tColor = typeColor[a.activity_type] || 'var(--t3)'
        return (
          <div key={idx} style={{ borderLeft: '3px solid var(--accent)', paddingLeft: 14 }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 4, flexWrap: 'wrap' }}>
              <span style={{ fontSize: 12, fontWeight: 700, color: 'var(--t1)' }}>{a.brand_name}</span>
              {a.activity_type && (
                <span style={{ fontSize: 9, fontWeight: 700, letterSpacing: .4, padding: '2px 7px', borderRadius: 8, background: 'rgba(255,255,255,.05)', color: tColor, border: `1px solid ${tColor}`, opacity: .85 }}>
                  {a.activity_type.toUpperCase()}
                </span>
              )}
              {a.date && <span style={{ fontSize: 10, color: 'var(--t4)' }}>{a.date}</span>}
            </div>
            <div style={{ fontSize: 11, color: 'var(--t2)', lineHeight: 1.6, marginBottom: 4 }}>{a.activity}</div>
            {a.impact_on_brand && (
              <div style={{ fontSize: 10, color: 'var(--accent2)', fontStyle: 'italic', marginBottom: 6 }}>
                💡 {a.impact_on_brand}
              </div>
            )}
            <SourceTrustBadge
              confidence={a.confidence_score || a.confidence_label || 'HIGH'}
              url={a.source_url}
              type="News / Press"
            />
          </div>
        )
      })}
    </div>
  )
}

function IndustryOutreachBody({ text, brands }) {
  const outreach = ensureParsed(text)
  const [selectedBrand, setSelectedBrand] = useState('')
  const [tab, setTab] = useState('linkedin')
  const [copied, setCopied] = useState('')

  useEffect(() => {
    if (outreach && outreach.length > 0 && !selectedBrand) {
      setSelectedBrand(outreach[0].brand_name)
    }
  }, [outreach, selectedBrand])

  if (!outreach || !Array.isArray(outreach)) return <ProseBody text={text} />
  const activeOutreach = outreach.find(o => o.brand_name === selectedBrand) || outreach[0]
  if (!activeOutreach) return <div style={{ fontSize: 11, color: 'var(--t3)', textAlign: 'center' }}>No outreach drafts available.</div>

  const doCopy = (key, val) => { copy(val || ''); setCopied(key); setTimeout(() => setCopied(''), 2000) }

  const tabStyle = id => ({
    padding: '6px 14px', fontSize: 11, cursor: 'pointer',
    borderBottom: tab === id ? '2px solid var(--accent2)' : '2px solid transparent',
    color: tab === id ? 'var(--t1)' : 'var(--t3)',
    background: 'none', border: 'none', fontFamily: 'var(--font)', fontWeight: tab === id ? 600 : 400
  })
  const boxStyle = {
    background: 'var(--bg2)', borderRadius: 'var(--r2)', padding: '12px 14px',
    fontSize: 12, lineHeight: 1.8, color: 'var(--t1)', whiteSpace: 'pre-wrap',
    marginBottom: 8, wordBreak: 'break-word'
  }
  const btnStyle = { fontSize: 11, padding: '5px 10px', border: '1px solid var(--accent)', borderRadius: 'var(--r1)', color: 'var(--accent2)', textDecoration: 'none', fontWeight: 500, cursor: 'pointer', background: 'none' }

  // Resolve action URLs — demo data has pre-built mailto_link with To+Subject+Body encoded
  const recipientEmail  = (activeOutreach.contact_email || '').trim()
  const hasRealEmail    = recipientEmail.length > 0
                       && recipientEmail.includes('@')
                       && !recipientEmail.toLowerCase().includes('not publicly')
                       && !recipientEmail.toLowerCase().includes('unavailable')
  const mailtoHref   = activeOutreach.mailto_link || `mailto:${encodeURIComponent(recipientEmail)}?subject=${encodeURIComponent(activeOutreach.email_subject || '')}&body=${encodeURIComponent(activeOutreach.email_body || '')}`
  const linkedinHref = activeOutreach.linkedin_url || 'https://www.linkedin.com/messaging/'

  // Sender strip fields
  const senderName    = activeOutreach.sender_name    || ''
  const senderTitle   = activeOutreach.sender_title   || ''
  const senderCompany = activeOutreach.sender_company || ''
  const senderEmail   = activeOutreach.sender_email   || ''

  // Urgency color
  const urgencyColor = { HIGH: 'var(--red)', MEDIUM: 'var(--amber)', LOW: 'var(--green)' }

  return (
    <div>
      {/* ── Sender strip ── */}
      {(senderName || senderEmail) && (
        <div style={{ display: 'flex', gap: 12, flexWrap: 'wrap', alignItems: 'center', background: 'rgba(124,109,250,.06)', border: '1px solid rgba(124,109,250,.18)', borderRadius: 'var(--r2)', padding: '8px 12px', marginBottom: 12, fontSize: 11 }}>
          <span style={{ color: 'var(--t4)', fontWeight: 700, letterSpacing: .4 }}>FROM</span>
          {senderName    && <span style={{ color: 'var(--t1)', fontWeight: 600 }}>{senderName}</span>}
          {senderTitle   && <span style={{ color: 'var(--t3)' }}>{senderTitle}</span>}
          {senderCompany && <span style={{ color: 'var(--accent2)' }}>{senderCompany}</span>}
          {senderEmail   && <span style={{ color: 'var(--t4)' }}>{senderEmail}</span>}
        </div>
      )}

      {/* ── Brand selector + tabs ── */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 10, flexWrap: 'wrap', gap: 8 }}>
        <div style={{ display: 'flex', gap: 6, alignItems: 'center', flexWrap: 'wrap' }}>
          <span style={{ fontSize: 11, color: 'var(--t3)' }}>Target:</span>
          <select value={selectedBrand} onChange={e => setSelectedBrand(e.target.value)} style={{ background: 'var(--bg2)', border: '1px solid var(--b1)', borderRadius: 'var(--r1)', padding: '4px 8px', fontSize: 12, color: 'var(--t1)' }}>
            {outreach.map((o, i) => <option key={i} value={o.brand_name}>{o.brand_name}</option>)}
          </select>
          {/* Urgency badge */}
          {activeOutreach.urgency_level && (
            <span style={{ fontSize: 9, fontWeight: 700, padding: '2px 8px', borderRadius: 8, color: urgencyColor[activeOutreach.urgency_level] || 'var(--t3)', border: `1px solid ${urgencyColor[activeOutreach.urgency_level] || 'var(--b2)'}`, background: 'rgba(255,255,255,.03)' }}>
              {activeOutreach.urgency_level} URGENCY
            </span>
          )}
          {/* Recommended service */}
          {activeOutreach.recommended_service && (
            <span style={{ fontSize: 9, fontWeight: 600, padding: '2px 8px', borderRadius: 8, color: 'var(--accent2)', border: '1px solid rgba(124,109,250,.3)', background: 'rgba(124,109,250,.07)' }}>
              {activeOutreach.recommended_service}
            </span>
          )}
        </div>
        <div style={{ display: 'flex', borderBottom: '1px solid var(--b1)', gap: 2 }}>
          {['linkedin', 'email'].map(t => (
            <button key={t} style={tabStyle(t)} onClick={() => setTab(t)}>
              {t === 'linkedin' ? '💼 LinkedIn' : '✉️ Email'}
            </button>
          ))}
        </div>
      </div>

      {/* ── Pitch hook ── */}
      {activeOutreach.pitch_hook && (
        <div style={{ background: 'rgba(124,109,250,.07)', border: '1px solid rgba(124,109,250,.2)', borderRadius: 'var(--r1)', padding: '8px 12px', marginBottom: 12, fontSize: 11 }}>
          <span style={{ color: 'var(--t4)', fontWeight: 700, fontSize: 9, letterSpacing: .4 }}>PITCH HOOK  </span>
          <span style={{ color: 'var(--t1)', fontStyle: 'italic' }}>"{activeOutreach.pitch_hook}"</span>
        </div>
      )}

      {/* ── LinkedIn tab ── */}
      {tab === 'linkedin' && (
        <div className="fade-up">
          <div style={{ fontSize: 10, color: 'var(--t3)', marginBottom: 6, letterSpacing: .4, fontWeight: 600 }}>
            CONNECTION MESSAGE · {(activeOutreach.linkedin_message || '').length} / 300 CHARS
          </div>
          <div style={boxStyle}>{activeOutreach.linkedin_message || 'Draft empty'}</div>
          <div style={{ display: 'flex', gap: 6 }}>
            <CopyBtn label="Copy message" onClick={() => doCopy('li', activeOutreach.linkedin_message)} copied={copied === 'li'} />
            <a href={linkedinHref} target="_blank" rel="noreferrer"
              onClick={() => copy(activeOutreach.linkedin_message || '')}
              style={btnStyle} title="Message auto-copied — paste it in LinkedIn compose">
              Open LinkedIn ↗
            </a>
          </div>
          <div style={{ fontSize: 10, color: 'var(--t4)', marginTop: 5, fontStyle: 'italic' }}>
            💡 Message is copied to clipboard when you click "Open LinkedIn" — just paste it.
          </div>
        </div>
      )}

      {/* ── Email tab ── */}
      {tab === 'email' && (
        <div className="fade-up">
          {/* To: row */}
          <div style={{ display: 'flex', gap: 8, alignItems: 'center', marginBottom: 10, padding: '7px 10px', background: 'var(--bg2)', borderRadius: 'var(--r1)', border: '1px solid var(--b1)' }}>
            <span style={{ fontSize: 10, color: 'var(--t4)', fontWeight: 700, letterSpacing: .3, minWidth: 22 }}>TO</span>
            {hasRealEmail ? (
              <>
                <span style={{ fontSize: 12, color: 'var(--green)', fontWeight: 500 }}>{recipientEmail}</span>
                <button onClick={() => doCopy('to', recipientEmail)} style={{ fontSize: 10, padding: '1px 6px', border: '1px solid var(--b1)', borderRadius: 4, background: 'none', color: 'var(--t4)', cursor: 'pointer', marginLeft: 'auto' }}>copy</button>
              </>
            ) : (
              <span style={{ fontSize: 11, color: 'var(--amber)', fontStyle: 'italic' }}>
                Email not found publicly — enter recipient manually
              </span>
            )}
          </div>

          <div style={{ fontSize: 10, color: 'var(--t3)', marginBottom: 5, letterSpacing: .4, fontWeight: 600 }}>SUBJECT</div>
          <div style={{ ...boxStyle, fontWeight: 600, padding: '8px 12px', marginBottom: 10 }}>{activeOutreach.email_subject || 'Draft empty'}</div>

          <div style={{ fontSize: 10, color: 'var(--t3)', marginBottom: 5, letterSpacing: .4, fontWeight: 600 }}>BODY</div>
          <div style={boxStyle}>{activeOutreach.email_body || 'Draft empty'}</div>

          <div style={{ fontSize: 10, color: 'var(--t3)', marginBottom: 5, letterSpacing: .4, fontWeight: 600 }}>CTA</div>
          <div style={{ ...boxStyle, padding: '8px 12px', marginBottom: 12 }}>{activeOutreach.email_cta || 'Draft empty'}</div>

          <div style={{ display: 'flex', gap: 6 }}>
            <CopyBtn label="Copy full email" onClick={() => doCopy('em', `Subject: ${activeOutreach.email_subject}\n\n${activeOutreach.email_body}`)} copied={copied === 'em'} />
            {/* mailto: pre-fills To:, Subject:, Body: */}
            <a href={mailtoHref} style={btnStyle}>Open in Mail ↗</a>
          </div>
          {hasRealEmail && (
            <div style={{ fontSize: 10, color: 'var(--green)', marginTop: 6, fontStyle: 'italic' }}>
              ✅ To: pre-filled with {recipientEmail}
            </div>
          )}
        </div>
      )}
    </div>
  )
}

function IndustryScoresBody({ text }) {
  const data = ensureParsed(text)
  if (!data) return <ProseBody text={text} />

  const prospects = data.prospects || []
  const top3 = prospects.slice(0, 3)

  // Calculate statistics
  const highTrustCount = prospects.filter(p => p.confidence_label === 'HIGH').length
  const trustPercentage = prospects.length ? Math.round((highTrustCount / prospects.length) * 100) : 0

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 14 }}>
      {/* Metrics Row */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))', gap: 10 }}>
        <div style={{ background: 'var(--bg2)', border: '1px solid var(--b1)', borderRadius: 'var(--r2)', padding: 12 }}>
          <div style={{ fontSize: 18, fontWeight: 600, color: 'var(--accent2)' }}>{prospects.length}</div>
          <div style={{ fontSize: 10, color: 'var(--t3)', marginTop: 2 }}>PROSPECTS DISCOVERED</div>
        </div>
        <div style={{ background: 'var(--bg2)', border: '1px solid var(--b1)', borderRadius: 'var(--r2)', padding: 12 }}>
          <div style={{ fontSize: 18, fontWeight: 600, color: 'var(--green)' }}>{trustPercentage}%</div>
          <div style={{ fontSize: 10, color: 'var(--t3)', marginTop: 2 }}>DATA TRANSPARENCY (HIGH TRUST)</div>
        </div>
        <div style={{ background: 'var(--bg2)', border: '1px solid var(--b1)', borderRadius: 'var(--r2)', padding: 12 }}>
          <div style={{ fontSize: 18, fontWeight: 600, color: 'var(--blue)' }}>{data.events?.length || 0}</div>
          <div style={{ fontSize: 10, color: 'var(--t3)', marginTop: 2 }}>REAL CONFERENCES MAPPED</div>
        </div>
      </div>

      {/* Top Recommendations */}
      <div>
        <div style={{ fontSize: 11, color: 'var(--t3)', fontWeight: 600, textTransform: 'uppercase', letterSpacing: .4, marginBottom: 8 }}>
          Top Strategic recommendations
        </div>
        <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
          {top3.map((p, idx) => (
            <div key={idx} style={{ background: 'rgba(124,109,250,.04)', border: '1px solid rgba(124,109,250,.15)', borderRadius: 'var(--r2)', padding: 12 }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 4 }}>
                <span style={{ fontSize: 12, fontWeight: 600, color: 'var(--t1)' }}>🏆 #{idx + 1} {p.brand_name}</span>
                <span style={{ fontSize: 11, fontWeight: 600, color: 'var(--accent2)' }}>Score: {p.overall_score}</span>
              </div>
              <div style={{ fontSize: 11, color: 'var(--t2)', lineHeight: 1.5 }}>
                {p.why_now}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}

// ── Upgraded Section Body Router ──────────────────────────────────────────────
function SectionBody({ id, text, isIndustry, notify, results }) {
  if (isIndustry) {
    if (id === 'brands') {
      const scoredData = results && results.scores ? ensureParsed(results.scores) : null;
      const brandsData = (scoredData && scoredData.prospects && scoredData.prospects.length > 0)
        ? scoredData.prospects
        : text;
      return <IndustryBrandsBody text={brandsData} notify={notify} />;
    }
    if (id === 'events')   return <IndustryEventsBody text={text} />
    if (id === 'contacts') return <IndustryContactsBody text={text} />
    if (id === 'activity') return <IndustryActivityBody text={text} />
    if (id === 'outreach') return <IndustryOutreachBody text={text} />
    if (id === 'scores')   return <IndustryScoresBody text={text} />
  }

  if (id === 'competitors')    return <CompetitorBody text={text} />
  if (id === 'watchouts')      return <WatchoutsBody text={text} />
  if (id === 'decisionmakers') return <DMBody text={text} />
  if (id === 'contacts')       return <ContactsBody text={text} />
  if (id === 'tracking')       return <TrackingBody text={text} />
  if (id === 'outreach')       return <OutreachBody text={text} />
  return <ProseBody text={text} />
}

// ── Main Research Page ────────────────────────────────────────────────────────
export default function Research() {
  const { apiKey, agency, notify } = useApp()
  const [mode, setMode] = useState('industry') // Defaulting to industry mode for hackathon wow impact
  const [co, setCo] = useState('')
  const [cat, setCat] = useState('')
  const [ind, setInd] = useState('')
  const [demoMode, setDemoMode] = useState(false)
  const [running, setRunning] = useState(false)
  const [results, setResults] = useState({})
  const [statuses, setStatuses] = useState({})
  const [progress, setProgress] = useState({ done: 0, total: 6 })
  const [open, setOpen] = useState({})
  const [company, setCompany] = useState('')
  const [presentationMode, setPresentationMode] = useState(false)
  const [demoSafeActive, setDemoSafeActive] = useState(false)
  const [sourceMode, setSourceMode] = useState('')
  
  // Auto-scroll logic for presentation mode
  const autoScrollInterval = useRef(null)
  const [isAutoScrolling, setIsAutoScrolling] = useState(false)

  const currentSections = mode === 'industry' ? INDUSTRY_SECTIONS : SECTIONS

  // Smooth scroll helper
  const scrollTo = (id) => {
    const el = document.getElementById('sec-' + id)
    if (el) {
      el.scrollIntoView({ behavior: 'smooth', block: 'center' })
    }
  }

  // Auto-scrolling sequence logic
  const toggleAutoScroll = () => {
    if (isAutoScrolling) {
      clearInterval(autoScrollInterval.current)
      setIsAutoScrolling(false)
    } else {
      setIsAutoScrolling(true)
      let index = 0
      autoScrollInterval.current = setInterval(() => {
        const sectionsToScroll = currentSections.filter(s => statuses[s.id] === 'done')
        if (sectionsToScroll.length === 0) return
        
        scrollTo(sectionsToScroll[index % sectionsToScroll.length].id)
        index++
      }, 7000)
    }
  }

  // Cleanup auto-scroll on unmount
  useEffect(() => {
    return () => {
      if (autoScrollInterval.current) clearInterval(autoScrollInterval.current)
    }
  }, [])

  const run = useCallback(async () => {
    if (mode === 'company') {
      if (!apiKey) { notify('Add your Gemini API key in Settings', 'error'); return }
      if (!co.trim() || !cat.trim()) { notify('Enter company name and category', 'error'); return }
      setCompany(co.trim())
    } else {
      // In industry mode, if api key is missing we automatically run in demo mode
      if (!apiKey && !demoMode) {
        notify('No API key detected. Running in Demo Safe Mode.', 'info')
        setDemoMode(true)
      }
      if (!ind.trim()) { notify('Enter industry name', 'error'); return }
      setCompany(ind.trim())
    }

    setResults({}); setStatuses({}); setOpen({}); setDemoSafeActive(false); setSourceMode('')
    setRunning(true); 
    setProgress({ done: 0, total: currentSections.length })
    
    const initialOpen = {}
    currentSections.forEach(s => { initialOpen[s.id] = false })
    setOpen(initialOpen)

    const url = mode === 'company' ? '/api/intelligence/run' : '/api/intelligence/run_industry'
    const payload = mode === 'company' 
      ? { company: co.trim(), category: cat.trim(), agency, apiKey }
      : { industry: ind.trim(), agency, apiKey, demoMode: demoMode || !apiKey }

    try {
      const res = await fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      })
      if (!res.ok) { const e = await res.json(); throw new Error(e.error || 'API error'); }

      const reader = res.body.getReader()
      const dec = new TextDecoder()
      let buf = ''

      const handle = (event, data) => {
        if (data.sourceMode) {
          setSourceMode(data.sourceMode)
        }
        if (event === 'session') {
          if (data.demoSafeMode === 'active') {
            setDemoSafeActive(true)
          }
        } else if (event === 'section_start') {
          setStatuses(p => ({ ...p, [data.sectionId]: 'running' }))
          setOpen(p => ({ ...p, [data.sectionId]: true }))
          
          if (data.demoMode) {
            setDemoSafeActive(true)
          }
        } else if (event === 'section_done') {
          setStatuses(p => ({ ...p, [data.sectionId]: 'done' }))
          setResults(p => ({ ...p, [data.sectionId]: data.result }))
          setProgress({ done: data.index, total: data.total })
          
          // Auto scroll to newly loaded section card
          scrollTo(data.sectionId)
        } else if (event === 'section_error') {
          setStatuses(p => ({ ...p, [data.sectionId]: 'error' }))
          setResults(p => ({ ...p, [data.sectionId]: `Error: ${data.error}` }))
          setProgress({ done: data.index, total: data.total })
          
          if (data.demoFallback) {
            setDemoSafeActive(true)
            notify('API Latency high. Engaged Demo Safe Mode.', 'warning')
          }
        }
      }

      while (true) {
        const { value, done } = await reader.read()
        if (done) break
        buf += dec.decode(value, { stream: true })
        const chunks = buf.split('\n\n')
        buf = chunks.pop()
        for (const chunk of chunks) {
          const lines = chunk.split('\n')
          let ev = '', dt = ''
          for (const l of lines) {
            if (l.startsWith('event: ')) ev = l.slice(7).trim()
            if (l.startsWith('data: ')) dt = l.slice(6).trim()
          }
          if (ev && dt) { try { handle(ev, JSON.parse(dt)) } catch {} }
        }
      }
    } catch (e) {
      const msg = e.message || ''
      if (msg.includes('quota') || msg.includes('Quota') || msg.includes('429')) {
        notify('Rate limit hit — backend will auto-retry. If it keeps failing, wait 60s and run again.', 'error')
      } else {
        notify(`Research failed: ${msg}`, 'error')
      }
    } finally {
      setRunning(false)
    }
  }, [co, cat, ind, demoMode, mode, apiKey, agency, notify, currentSections, statuses])

  const exportJSON = () => {
    const filename = `${company.replace(/\s+/g, '_')}_intelligence.json`
    const blob = new Blob([JSON.stringify({ 
      search_mode: mode,
      search_term: company, 
      generated: new Date().toISOString(), 
      demo_safe_mode_active: demoSafeActive,
      results 
    }, null, 2)], { type: 'application/json' })
    const a = document.createElement('a'); a.href = URL.createObjectURL(blob); a.download = filename; a.click()
  }

  const exportCSV = () => {
    if (mode === 'company') {
      notify('CSV export is only available in Industry Discovery mode.', 'info')
      return
    }
    const scoresData = results.scores
    if (!scoresData || !scoresData.prospects) {
      notify('No scored prospects to export yet.', 'warning')
      return
    }
    
    const prospects = scoresData.prospects
    const headers = ["Rank", "Brand Name", "Overall Score", "Strategic Fit", "Growth Signal", "Event Presence", "Recent Activity", "Why StepOne", "Why Now", "Source URL"]
    const rows = prospects.map((p, idx) => [
      idx + 1,
      `"${p.brand_name}"`,
      p.overall_score,
      p.strategic_fit_score,
      p.growth_signal_score,
      p.event_presence_score,
      p.recent_activity_score,
      `"${(p.why_stepone || '').replace(/"/g, '""')}"`,
      `"${(p.why_now || '').replace(/"/g, '""')}"`,
      p.source_url || 'N/A'
    ])
    
    const csvContent = [headers.join(","), ...rows.map(e => e.join(","))].join("\n")
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' })
    const a = document.createElement('a'); a.href = URL.createObjectURL(blob); a.download = `${company.replace(/\s+/g, '_')}_prospects.csv`; a.click()
  }

  const exportTXT = () => {
    const lines = [`MARKET INTELLIGENCE REPORT\nType: ${mode === 'company' ? 'Company Deep Dive' : 'Industry Discovery'}\nSearch Term: ${company}\n${'='.repeat(50)}\n`]
    currentSections.forEach(s => {
      const val = results[s.id]
      const renderedText = typeof val === 'object' ? JSON.stringify(val, null, 2) : val
      lines.push(`## ${s.num}. ${s.title.toUpperCase()}\n\n${renderedText || 'Not generated'}\n\n`)
    })
    const blob = new Blob([lines.join('\n')], { type: 'text/plain' })
    const a = document.createElement('a'); a.href = URL.createObjectURL(blob); a.download = `${company.replace(/\s+/g, '_')}_report.txt`; a.click()
  }

  const pct = (progress.done / progress.total) * 100

  // Styles for Presentation mode
  const presStyles = presentationMode ? {
    position: 'fixed', top: 0, left: 0, right: 0, bottom: 0,
    zIndex: 9999, background: 'var(--bg0)', padding: '36px 48px',
    overflowY: 'auto', display: 'flex', flexDirection: 'column', gap: 16
  } : {}

  return (
    <div style={{ display: 'flex', height: '100%', overflow: 'hidden' }}>
      
      {/* ── Left Sidebar (Hidden in Presentation Mode) ── */}
      {!presentationMode && (
        <div style={{
          width: 220, minWidth: 220, background: 'var(--bg1)', borderRight: '1px solid var(--b2)',
          display: 'flex', flexDirection: 'column', height: '100%', overflow: 'hidden'
        }}>
          {/* Mode toggle */}
          <div style={{ display: 'flex', borderBottom: '1px solid var(--b2)', flexShrink: 0 }}>
            <button onClick={() => { if(!running) setMode('industry') }} style={{
              flex: 1, padding: '10px 0', border: 'none', background: mode === 'industry' ? 'var(--bg3)' : 'none',
              color: mode === 'industry' ? 'var(--accent2)' : 'var(--t3)', fontSize: 11, fontWeight: 600, cursor: running ? 'not-allowed' : 'pointer',
              borderBottom: mode === 'industry' ? '2px solid var(--accent2)' : 'none'
            }}>
              Industry Mode
            </button>
            <button onClick={() => { if(!running) setMode('company') }} style={{
              flex: 1, padding: '10px 0', border: 'none', background: mode === 'company' ? 'var(--bg3)' : 'none',
              color: mode === 'company' ? 'var(--accent2)' : 'var(--t3)', fontSize: 11, fontWeight: 600, cursor: running ? 'not-allowed' : 'pointer',
              borderBottom: mode === 'company' ? '2px solid var(--accent2)' : 'none'
            }}>
              Company Mode
            </button>
          </div>

          {/* Inputs */}
          <div style={{ padding: '14px 12px', borderBottom: '1px solid var(--b2)', flexShrink: 0 }}>
            {mode === 'company' ? (
              <>
                <div style={{ fontSize: 10, color: 'var(--t3)', marginBottom: 6, letterSpacing: .4, fontWeight: 500 }}>COMPANY NAME</div>
                <input value={co} onChange={e => setCo(e.target.value)} placeholder="Nike, Notion, Zomato…"
                  style={{ width: '100%', background: 'var(--bg2)', border: '1px solid var(--b1)', borderRadius: 'var(--r1)', padding: '6px 9px', fontSize: 12, color: 'var(--t1)', marginBottom: 8, boxSizing: 'border-box' }} />
                <div style={{ fontSize: 10, color: 'var(--t3)', marginBottom: 6, letterSpacing: .4, fontWeight: 500 }}>CATEGORY</div>
                <input value={cat} onChange={e => setCat(e.target.value)} placeholder="D2C sportswear brand"
                  style={{ width: '100%', background: 'var(--bg2)', border: '1px solid var(--b1)', borderRadius: 'var(--r1)', padding: '6px 9px', fontSize: 12, color: 'var(--t1)', marginBottom: 10, boxSizing: 'border-box' }} />
              </>
            ) : (
              <>
                <div style={{ fontSize: 10, color: 'var(--t3)', marginBottom: 6, letterSpacing: .4, fontWeight: 500 }}>INDUSTRY NAME</div>
                <input value={ind} onChange={e => setInd(e.target.value)} placeholder="Electric Vehicles, FinTech…"
                  style={{ width: '100%', background: 'var(--bg2)', border: '1px solid var(--b1)', borderRadius: 'var(--r1)', padding: '6px 9px', fontSize: 12, color: 'var(--t1)', marginBottom: 10, boxSizing: 'border-box' }} />
                <div style={{ display: 'flex', alignItems: 'center', gap: 6, marginBottom: 10 }}>
                  <input type="checkbox" id="chkDemo" checked={demoMode} onChange={e => setDemoMode(e.target.checked)} style={{ cursor: 'pointer' }} />
                  <label htmlFor="chkDemo" style={{ fontSize: 10, color: 'var(--t2)', cursor: 'pointer' }}>Demo Safe Mode</label>
                </div>
              </>
            )}

            <button onClick={run} disabled={running}
              style={{ width: '100%', padding: '8px', background: running ? 'var(--bg3)' : 'var(--accent)', color: running ? 'var(--t3)' : '#fff', border: 'none', borderRadius: 'var(--r1)', fontSize: 12, fontWeight: 500, cursor: running ? 'not-allowed' : 'pointer' }}>
              {running ? 'Streaming Engine…' : 'Run Pipeline ↗'}
            </button>
          </div>

          {/* Progress bar */}
          {running && (
            <div style={{ padding: '10px 12px', borderBottom: '1px solid var(--b2)', flexShrink: 0 }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: 10, color: 'var(--t3)', marginBottom: 5 }}>
                <span>Progress</span><span>{progress.done}/{progress.total}</span>
              </div>
              <div style={{ height: 2, background: 'var(--b1)', borderRadius: 2, overflow: 'hidden' }}>
                <div style={{ height: '100%', width: `${pct}%`, background: 'var(--accent)', transition: 'width .5s ease' }}></div>
              </div>
            </div>
          )}

          {/* Navigation Dot List */}
          <div style={{ flex: 1, overflowY: 'auto', padding: '6px 0' }}>
            <div style={{ fontSize: 9, color: 'var(--t4)', padding: '6px 12px 3px', letterSpacing: .5, fontWeight: 500 }}>PRIORITY</div>
            {currentSections.filter(s => s.priority).map(s => (
              <NavDot key={s.id} s={s} status={statuses[s.id]} onClick={() => scrollTo(s.id)} />
            ))}
            <div style={{ fontSize: 9, color: 'var(--t4)', padding: '10px 12px 3px', letterSpacing: .5, fontWeight: 500 }}>SUPPORTING</div>
            {currentSections.filter(s => !s.priority).map(s => (
              <NavDot key={s.id} s={s} status={statuses[s.id]} onClick={() => scrollTo(s.id)} />
            ))}
          </div>

          {/* Export buttons */}
          {Object.keys(results).length > 0 && (
            <div style={{ padding: '10px 12px', borderTop: '1px solid var(--b2)', display: 'flex', gap: 4, flexShrink: 0 }}>
              <button onClick={exportJSON} style={{ flex: 1, padding: '5px 0', fontSize: 9, border: '1px solid var(--b1)', borderRadius: 'var(--r1)', background: 'none', color: 'var(--t3)', cursor: 'pointer' }}>JSON</button>
              {mode === 'industry' && (
                <button onClick={exportCSV} style={{ flex: 1, padding: '5px 0', fontSize: 9, border: '1px solid var(--b1)', borderRadius: 'var(--r1)', background: 'none', color: 'var(--t3)', cursor: 'pointer' }}>CSV</button>
              )}
              <button onClick={exportTXT} style={{ flex: 1, padding: '5px 0', fontSize: 9, border: '1px solid var(--b1)', borderRadius: 'var(--r1)', background: 'none', color: 'var(--t3)', cursor: 'pointer' }}>TXT</button>
            </div>
          )}
        </div>
      )}

      {/* ── Main panel Content Area ── */}
      <div style={{
        flex: 1, overflowY: 'auto', height: '100%', padding: '20px 24px',
        display: 'flex', flexDirection: 'column', gap: 12, boxSizing: 'border-box',
        ...presStyles
      }}>
        
        {/* Header Controls (Presentation toggler, Demo notification) */}
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexShrink: 0 }}>
          {company ? (
            <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
              <div style={{ width: 30, height: 30, borderRadius: 6, background: 'var(--bg3)', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: 13, fontWeight: 700, color: 'var(--accent2)' }}>
                {company[0]?.toUpperCase()}
              </div>
              <div>
                <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                  <div style={{ fontWeight: 600, color: 'var(--t1)', fontSize: presentationMode ? 20 : 13 }}>
                    {company} {mode === 'industry' ? 'Prospecting Report' : 'Deep Dive'}
                  </div>
                  {mode === 'industry' && sourceMode && (
                    <span style={{
                      fontSize: 9, padding: '2px 8px', borderRadius: 10,
                      fontWeight: 700, textTransform: 'uppercase',
                      background: sourceMode === 'LIVE DATA' ? 'rgba(62,207,142,.12)' : sourceMode === 'CACHED VERIFIED DATA' ? 'rgba(124,109,250,.12)' : 'rgba(245,166,35,.12)',
                      color: sourceMode === 'LIVE DATA' ? 'var(--green)' : sourceMode === 'CACHED VERIFIED DATA' ? 'var(--accent2)' : 'var(--amber)',
                      border: `1px solid ${sourceMode === 'LIVE DATA' ? 'var(--green)' : sourceMode === 'CACHED VERIFIED DATA' ? 'var(--accent)' : 'var(--amber)'}30`,
                      letterSpacing: '.3px'
                    }}>
                      {sourceMode}
                    </span>
                  )}
                </div>
                <div style={{ fontSize: 11, color: 'var(--t3)' }}>
                  {mode === 'industry' ? 'Dynamic Market Discovery' : cat}
                </div>
              </div>
            </div>
          ) : (
            <div />
          )}

          {/* Presentation control buttons */}
          {Object.keys(results).length > 0 && (
            <div style={{ display: 'flex', gap: 8, alignItems: 'center' }}>
              {presentationMode && (
                <button onClick={toggleAutoScroll} style={{
                  padding: '6px 12px', background: isAutoScrolling ? 'var(--green)' : 'var(--bg2)',
                  border: '1px solid var(--b1)', borderRadius: 'var(--r2)', color: '#fff', fontSize: 11, cursor: 'pointer'
                }}>
                  {isAutoScrolling ? '⏸ Pause Scroll' : '▶ Auto-Scroll'}
                </button>
              )}
              <button onClick={() => setPresentationMode(!presentationMode)} style={{
                padding: '6px 12px', background: 'var(--accent)', border: 'none', borderRadius: 'var(--r2)',
                color: '#fff', fontSize: 11, fontWeight: 500, cursor: 'pointer'
              }}>
                {presentationMode ? 'Exit Presentation Mode' : '🖥️ Presentation Mode'}
              </button>
            </div>
          )}
        </div>

        {/* Demo Safe Mode active flag indicator banner */}
        {demoSafeActive && (
          <div className="fade-up" style={{
            background: 'rgba(245,166,35,.07)', border: '1px solid rgba(245,166,35,.25)',
            color: 'var(--amber)', borderRadius: 'var(--r2)', padding: '8px 12px', fontSize: 11,
            display: 'flex', alignItems: 'center', gap: 6, fontWeight: 500, flexShrink: 0
          }}>
            <span>🛡️</span>
            <span>DEMO SAFE MODE: Using previously validated intelligence</span>
          </div>
        )}

        {/* Placeholder before running */}
        {!company && (
          <div style={{ textAlign: 'center', padding: '120px 20px', color: 'var(--t3)', flex: 1, display: 'flex', flexDirection: 'column', justifyContent: 'center' }}>
            <div style={{ fontSize: 36, marginBottom: 12, opacity: .3 }}>◉</div>
            <div style={{ fontSize: 16, fontWeight: 600, color: 'var(--t2)', marginBottom: 6 }}>Market Intelligence Engine</div>
            <div style={{ fontSize: 12, lineHeight: 1.7, maxWidth: 360, margin: '0 auto' }}>
              {mode === 'industry' 
                ? 'Enter an industry name (e.g. Electric Vehicles, FinTech) to discover 10+ prospects, analyze upcoming events, locate decision makers, and score them.'
                : 'Enter a company name and brand category to compile a targeted 11-section research blueprint.'}
            </div>
          </div>
        )}

        {/* Section Cards */}
        {company && currentSections.map(s => (
          <SectionCard
            key={s.id}
            s={s}
            status={statuses[s.id]}
            result={results[s.id]}
            isOpen={!!open[s.id]}
            onToggle={() => setOpen(p => ({ ...p, [s.id]: !p[s.id] }))}
            results={results}
            mode={mode}
          />
        ))}

        <div style={{ height: 60, flexShrink: 0 }} />
      </div>
    </div>
  )
}

// ── Nav dot ───────────────────────────────────────────────────────────────────
function NavDot({ s, status, onClick }) {
  return (
    <div
      onClick={onClick}
      style={{ display: 'flex', alignItems: 'center', gap: 7, padding: '5px 12px', cursor: 'pointer', fontSize: 11, color: 'var(--t3)' }}
      onMouseEnter={e => e.currentTarget.style.background = 'var(--bg2)'}
      onMouseLeave={e => e.currentTarget.style.background = 'none'}
    >
      <span style={{ fontSize: 9, color: 'var(--t4)', minWidth: 14 }}>{s.num}</span>
      <span style={{ flex: 1 }}>{s.title}</span>
      <span style={{
        width: 6, height: 6, borderRadius: '50%',
        background: STATUS_COLOR[status] || 'var(--b1)',
        flexShrink: 0,
        animation: status === 'running' ? 'blink 1s infinite' : 'none'
      }}></span>
    </div>
  )
}

// ── Section card ──────────────────────────────────────────────────────────────
function SectionCard({ s, status, result, isOpen, onToggle, results, mode }) {
  const isIndustry = mode === 'industry'
  return (
    <div
      id={`sec-${s.id}`}
      style={{ background: 'var(--bg1)', border: '1px solid var(--b1)', borderRadius: 'var(--r3)', overflow: 'hidden', flexShrink: 0 }}
      className="fade-up"
    >
      <div
        onClick={onToggle}
        style={{
          padding: '12px 14px',
          borderBottom: isOpen ? '1px solid var(--b2)' : 'none',
          display: 'flex', alignItems: 'center', gap: 8,
          cursor: 'pointer', userSelect: 'none'
        }}
      >
        <span style={{ fontSize: 9, color: 'var(--t4)', minWidth: 18, fontFamily: 'var(--mono)' }}>{s.num}</span>
        <span style={{ flex: 1, fontSize: 12, fontWeight: 500, color: 'var(--t1)' }}>{s.title}</span>
        {s.priority && (
          <span style={{ fontSize: 9, padding: '1px 6px', borderRadius: 6, background: 'rgba(124,109,250,.1)', color: 'var(--accent2)', border: '1px solid rgba(124,109,250,.2)' }}>Priority</span>
        )}
        <span style={{
          fontSize: 9, padding: '1px 7px', borderRadius: 6,
          background: status === 'done' ? 'rgba(62,207,142,.1)' : status === 'running' ? 'rgba(245,166,35,.1)' : 'var(--bg3)',
          color: STATUS_COLOR[status] || 'var(--t4)',
          border: `1px solid ${STATUS_COLOR[status] ? STATUS_COLOR[status] + '40' : 'var(--b1)'}`,
          animation: status === 'running' ? 'blink 1.2s infinite' : 'none'
        }}>
          {STATUS_LABEL[status || '']}
        </span>
        <span style={{ fontSize: 9, color: 'var(--t4)' }}>{isOpen ? '▲' : '▼'}</span>
      </div>

      {isOpen && (
        <div style={{ padding: 16 }}>
          {!result && status === 'running' && <SkeletonLines />}
          {!result && !status && (
            <div style={{ fontSize: 11, color: 'var(--t4)', textAlign: 'center', padding: '14px 0' }}>Queued…</div>
          )}
          {result && <SectionBody id={s.id} text={result} isIndustry={isIndustry} notify={useApp().notify} results={results} />}
        </div>
      )}
    </div>
  )
}

function SkeletonLines() {
  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 7 }}>
      {[90, 72, 83, 65, 78].map((w, i) => (
        <div key={i} className="skeleton" style={{ height: 11, width: `${w}%` }}></div>
      ))}
    </div>
  )
}