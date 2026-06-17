import { useState } from 'react'
import { useApp } from '../App.jsx'

export default function Settings() {
  const { apiKey, setApiKey, agency, setAgency, notify } = useApp()
  const [key, setKey] = useState(apiKey)
  const [ag, setAg] = useState(agency)
  const [showKey, setShowKey] = useState(false)
  const [saved, setSaved] = useState(false)

  function save() {
    setApiKey(key.trim())
    setAgency(ag.trim())
    setSaved(true)
    notify('Settings saved', 'success')
    setTimeout(() => setSaved(false), 2000)
  }

  const inp = { width: '100%', background: 'var(--bg2)', border: '1px solid var(--b1)', borderRadius: 'var(--r2)', padding: '9px 12px', fontSize: 13, color: 'var(--t1)', fontFamily: 'var(--font)', marginBottom: 4 }
  const lbl = { fontSize: 11, fontWeight: 500, color: 'var(--t2)', display: 'block', marginBottom: 6 }
  const hint = { fontSize: 11, color: 'var(--t3)', marginBottom: 20 }

  return (
    <div style={{ flex: 1, overflow: 'auto', padding: '28px 32px', maxWidth: 560 }}>
      <div style={{ fontSize: 20, fontWeight: 600, color: 'var(--t1)', marginBottom: 4 }}>Settings</div>
      <div style={{ fontSize: 12, color: 'var(--t3)', marginBottom: 28 }}>Configure your API key and agency profile</div>

      <div style={{ background: 'var(--bg1)', border: '1px solid var(--b1)', borderRadius: 'var(--r3)', padding: '20px 22px', marginBottom: 16 }}>
        <div style={{ fontSize: 13, fontWeight: 500, color: 'var(--t1)', marginBottom: 16 }}>Gemini API</div>

        <label style={lbl}>API Key</label>
        <div style={{ position: 'relative', marginBottom: 4 }}>
          <input type={showKey ? 'text' : 'password'} value={key} onChange={e => setKey(e.target.value)}
            placeholder="AIza..."
            style={{ ...inp, marginBottom: 0, paddingRight: 70, fontFamily: showKey ? 'var(--mono)' : 'var(--font)' }} />
          <button onClick={() => setShowKey(p => !p)} style={{ position: 'absolute', right: 10, top: '50%', transform: 'translateY(-50%)', background: 'none', border: 'none', color: 'var(--t3)', fontSize: 11, cursor: 'pointer' }}>
            {showKey ? 'Hide' : 'Show'}
          </button>
        </div>
        <div style={hint}>
          Get your key at <a href="https://aistudio.google.com/app/apikey" target="_blank" rel="noreferrer">aistudio.google.com/app/apikey</a>. Stored locally in your browser only.
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: 8, padding: '10px 12px', background: key.startsWith('AIza') ? 'rgba(62,207,142,.07)' : 'var(--bg2)', borderRadius: 'var(--r1)', border: `1px solid ${key.startsWith('AIza') ? 'rgba(62,207,142,.25)' : 'var(--b1)'}` }}>
          <span style={{ width: 6, height: 6, borderRadius: '50%', background: key.startsWith('AIza') ? 'var(--green)' : 'var(--t4)', flexShrink: 0 }}></span>
          <span style={{ fontSize: 11, color: key.startsWith('AIza') ? 'var(--green)' : 'var(--t3)' }}>
            {key.startsWith('AIza') ? 'Valid Gemini key format detected' : 'Enter a valid Gemini API key (starts with AIza)'}
          </span>
        </div>
      </div>

      <div style={{ background: 'var(--bg1)', border: '1px solid var(--b1)', borderRadius: 'var(--r3)', padding: '20px 22px', marginBottom: 20 }}>
        <div style={{ fontSize: 13, fontWeight: 500, color: 'var(--t1)', marginBottom: 16 }}>Agency Profile</div>
        <label style={lbl}>Agency Speciality</label>
        <textarea value={ag} onChange={e => setAg(e.target.value)} rows={3} placeholder="e.g. brand strategy, experiential campaigns, retail activations, digital marketing"
          style={{ ...inp, resize: 'vertical' }} />
        <div style={hint}>This context is injected into every outreach generation prompt to personalise messaging.</div>
      </div>

      <button onClick={save} style={{ padding: '10px 24px', background: saved ? 'var(--green)' : 'var(--accent)', border: 'none', borderRadius: 'var(--r2)', color: '#fff', fontSize: 13, fontWeight: 500, cursor: 'pointer', fontFamily: 'var(--font)', transition: 'background .2s' }}>
        {saved ? '✓ Saved' : 'Save Settings'}
      </button>

      <div style={{ marginTop: 32, padding: '16px 20px', background: 'var(--bg2)', borderRadius: 'var(--r2)', border: '1px solid var(--b1)' }}>
        <div style={{ fontSize: 11, fontWeight: 500, color: 'var(--t2)', marginBottom: 8 }}>How to run the full stack</div>
        <pre style={{ fontFamily: 'var(--mono)', fontSize: 11, color: 'var(--t3)', lineHeight: 1.8, whiteSpace: 'pre-wrap' }}>{`# Backend (Python)
cd backend
pip install -r requirements.txt
cp .env.example .env   # add your key
python app.py

# Frontend (React)
cd frontend
npm install
npm run dev

# Open http://localhost:3000`}</pre>
      </div>
    </div>
  )
}
