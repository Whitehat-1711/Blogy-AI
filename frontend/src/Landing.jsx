import React from 'react';

// --- HAND-DRAWN / CARTOON SVG ASSETS (No External Images) ---

const Tape = ({ rotate = -4, left = "50%", top = "-10px", color = "rgba(235, 235, 235, 0.9)" }) => (
  <div style={{
    position: 'absolute',
    top,
    left,
    transform: `translateX(-50%) rotate(${rotate}deg)`,
    width: '80px',
    height: '25px',
    background: color,
    border: '2px solid #1F2A44',
    boxShadow: '3px 3px 0px rgba(31,42,68,0.2)',
    zIndex: 5
  }} />
);

const PaperClip = () => (
  <svg width="40" height="90" viewBox="0 0 40 90" fill="none" style={{ position: 'absolute', top: '-30px', right: '10px', zIndex: 10, filter: 'drop-shadow(3px 3px 0px rgba(31,42,68,0.8))' }}>
    <path d="M25 20V65C25 75 19 80 13 80C7 80 2 75 2 65V15C2 7 7 2 13 2C19 2 24 7 24 15V50" stroke="#E2E8F0" strokeWidth="8" strokeLinecap="round" />
    <path d="M25 20V65C25 75 19 80 13 80C7 80 2 75 2 65V15C2 7 7 2 13 2C19 2 24 7 24 15V50" stroke="#1F2A44" strokeWidth="3" strokeLinecap="round" />
    <path d="M2 65V35" stroke="#1F2A44" strokeWidth="3" strokeLinecap="round" />
  </svg>
);

const PencilDoodle = () => (
  <svg width="150" height="150" viewBox="0 0 100 100" fill="none" style={{ filter: 'drop-shadow(6px 6px 0px #1F2A44)' }}>
    {/* Eraser */}
    <path d="M20 80 L35 95 L25 105 L10 90 Z" fill="#F4A4A4" stroke="#1F2A44" strokeWidth="3" strokeLinejoin="round" />
    {/* Metal Band */}
    <path d="M35 95 L40 90 L25 75 L20 80 Z" fill="#9AA5B4" stroke="#1F2A44" strokeWidth="3" strokeLinejoin="round" />
    {/* Body */}
    <path d="M40 90 L85 45 L70 30 L25 75 Z" fill="#FFC857" stroke="#1F2A44" strokeWidth="3" strokeLinejoin="round" />
    <path d="M30 80 L75 35" stroke="#1F2A44" strokeWidth="3" />
    {/* Wood tip */}
    <path d="M85 45 L95 20 L70 30 Z" fill="#F5EBDD" stroke="#1F2A44" strokeWidth="3" strokeLinejoin="round" />
    {/* Lead */}
    <path d="M90 27 L95 20 L87 23 Z" fill="#1F2A44" stroke="#1F2A44" strokeWidth="2" strokeLinejoin="round" />
  </svg>
);

const BookDoodle = () => (
  <svg width="180" height="150" viewBox="0 0 120 100" fill="none" style={{ filter: 'drop-shadow(6px 6px 0px #1F2A44)' }}>
    {/* Back Cover */}
    <path d="M10 20 L55 10 L105 20 L105 80 L55 70 L10 80 Z" fill="#1F2A44" />
    {/* Pages Right */}
    <path d="M55 15 L100 25 L100 75 L55 65 Z" fill="#fff" stroke="#1F2A44" strokeWidth="3" strokeLinejoin="round" />
    {/* Pages Left */}
    <path d="M55 15 L10 25 L10 75 L55 65 Z" fill="#fff" stroke="#1F2A44" strokeWidth="3" strokeLinejoin="round" />
    {/* Page Lines */}
    <path d="M65 30 L90 35 M65 40 L90 45 M65 50 L90 55 M20 35 L45 30 M20 45 L45 40 M20 55 L45 50" stroke="#A0AEC0" strokeWidth="2" strokeLinecap="round" />
    {/* Bookmark */}
    <path d="M75 15 L85 17 L85 40 L80 35 L75 40 Z" fill="#E0C3FC" stroke="#1F2A44" strokeWidth="2" strokeLinejoin="round" />
    {/* Center crease */}
    <path d="M55 15 L55 65" stroke="#1F2A44" strokeWidth="4" strokeLinecap="round" />
  </svg>
);

const TornNote = ({ color = "#E0C3FC", rotate = 0, style, children }) => (
  <div style={{ position: 'absolute', transform: `rotate(${rotate}deg)`, ...style }}>
    {/* Tape */}
    <Tape rotate={12} top="-8px" left="60%" color="rgba(244, 164, 164, 0.9)" />
    <svg width="180" height="150" viewBox="0 0 180 150" fill="none" style={{ filter: 'drop-shadow(6px 6px 0px #1F2A44)' }}>
      {/* Hand-drawn torn edge path */}
      <path d="M10 10 L170 10 L170 140 L160 135 L145 145 L130 138 L115 148 L100 136 L85 145 L70 135 L55 145 L40 135 L25 142 L10 135 Z" fill={color} stroke="#1F2A44" strokeWidth="4" strokeLinejoin="round" />
    </svg>
    <div style={{ position: 'absolute', top: 0, left: 0, width: '100%', height: '100%', padding: '25px', display: 'flex', alignItems: 'center', justifyContent: 'center', textAlign: 'center', fontFamily: "'Caveat', cursive", fontSize: '1.6rem', color: '#1F2A44', zIndex: 1, fontWeight: '700' }}>
      {children}
    </div>
  </div>
);

const GridNote = ({ rotate = 0, style, children }) => (
  <div style={{
    position: 'absolute',
    transform: `rotate(${rotate}deg)`,
    width: '160px',
    height: '160px',
    background: '#fff',
    backgroundImage: 'linear-gradient(#CBD5E0 1.5px, transparent 1.5px), linear-gradient(90deg, #CBD5E0 1.5px, transparent 1.5px)',
    backgroundSize: '20px 20px',
    border: '4px solid #1F2A44',
    boxShadow: '6px 6px 0px #1F2A44',
    ...style
  }}>
    <Tape rotate={-5} top="-12px" color="rgba(255, 200, 87, 0.9)" />
    <div style={{ padding: '20px', fontFamily: "'Caveat', cursive", fontSize: '1.5rem', color: '#1F2A44', fontWeight: 'bold' }}>
      {children}
    </div>
  </div>
);

const PaperClipNote = ({ rotate = 0, style, children }) => (
  <div style={{
    position: 'absolute',
    transform: `rotate(${rotate}deg)`,
    width: '150px',
    height: '180px',
    background: '#FFF3CD',
    border: '4px solid #1F2A44',
    boxShadow: '6px 6px 0px #1F2A44',
    borderRadius: '10px 10px 40px 10px',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    ...style
  }}>
    <PaperClip />
    <div style={{ padding: '20px', textAlign: 'center', fontFamily: "'Caveat', cursive", fontSize: '1.6rem', color: '#1F2A44', fontWeight: 'bold' }}>
      {children}
    </div>
  </div>
);

const StarDoodle = ({ style }) => (
  <svg width="60" height="60" viewBox="0 0 60 60" fill="none" style={{ ...style, filter: 'drop-shadow(3px 3px 0px #1F2A44)' }}>
    <path d="M30 5 L36 22 L55 22 L40 33 L45 50 L30 40 L15 50 L20 33 L5 22 L24 22 Z" fill="#FFC857" stroke="#1F2A44" strokeWidth="3" strokeLinejoin="round" />
  </svg>
);

const ArrowDoodle = ({ style }) => (
  <svg width="70" height="90" viewBox="0 0 70 90" fill="none" style={{ ...style, filter: 'drop-shadow(3px 3px 0px rgba(31,42,68,0.5))' }}>
    <path d="M10 10 C 20 40, 50 60, 30 80 M30 80 L15 70 M30 80 L45 75" stroke="#F4A4A4" strokeWidth="6" strokeLinecap="round" strokeLinejoin="round" />
  </svg>
);


export default function LandingPage({ onNavigate }) {
  React.useEffect(() => {
    if (!document.getElementById("landing-animations")) {
      const style = document.createElement("style");
      style.id = "landing-animations";
      style.innerHTML = `
        @keyframes float-1 { 0%, 100% { transform: translateY(0px) rotate(0deg); } 50% { transform: translateY(-15px) rotate(3deg); } }
        @keyframes float-2 { 0%, 100% { transform: translateY(0px) rotate(0deg); } 50% { transform: translateY(-10px) rotate(-4deg); } }
        @keyframes float-3 { 0%, 100% { transform: translateY(0px) rotate(0deg); } 50% { transform: translateY(-20px) rotate(-2deg); } }
        @keyframes wiggle { 0%, 100% { transform: rotate(-5deg); } 50% { transform: rotate(5deg); } }
        
        .neo-button {
          background: #FFC857;
          border: 4px solid #1F2A44;
          box-shadow: 6px 6px 0px #1F2A44;
          color: #1F2A44;
          font-weight: 800;
          font-size: 1.25rem;
          padding: 16px 36px;
          border-radius: 12px;
          cursor: pointer;
          transition: transform 0.1s, box-shadow 0.1s;
        }
        .neo-button:active {
          transform: translate(6px, 6px);
          box-shadow: 0px 0px 0px #1F2A44;
        }
        
        .animate-f1 { animation: float-1 5s ease-in-out infinite; }
        .animate-f2 { animation: float-2 7s ease-in-out infinite; }
        .animate-f3 { animation: float-3 6s ease-in-out infinite; }
        .animate-wg { animation: wiggle 4s ease-in-out infinite; }
      `;
      document.head.appendChild(style);
    }
  }, []);

  return (
    <div style={{
      width: '100vw',
      height: '100vh',
      display: 'flex',
      flexDirection: 'column',
      background: '#F5EBDD',
      overflow: 'hidden',
      position: 'relative',
      fontFamily: "'Nunito', sans-serif"
    }}>
      {/* Full Page Graph Paper Texture */}
      <div style={{
        position: 'absolute',
        inset: 0,
        backgroundImage: 'linear-gradient(rgba(31,42,68,0.06) 2px, transparent 2px), linear-gradient(90deg, rgba(31,42,68,0.06) 2px, transparent 2px)',
        backgroundSize: '40px 40px',
        zIndex: 0
      }} />

      {/* --- SCATTERED ELEMENTS ACTUALLY SCATTERED USING FIXED POSITIONS --- */}

      {/* Top Left */}
      <div className="animate-f1" style={{ position: 'absolute', top: '10%', left: '10%', zIndex: 1 }}>
        <GridNote rotate={-6}>
          New Ideas 💡
        </GridNote>
      </div>

      {/* Top Right */}
      <div className="animate-f2" style={{ position: 'absolute', top: '15%', right: '12%', zIndex: 2 }}>
        <TornNote rotate={8} color="#C8E6CB">
          Rank #1
        </TornNote>
      </div>

      {/* Bottom Left */}
      <div className="animate-f3" style={{ position: 'absolute', bottom: '15%', left: '15%', zIndex: 2 }}>
        <PaperClipNote rotate={-10}>
          SEO<br />Keywords
        </PaperClipNote>
      </div>

      {/* Middle Left: Hand Drawn Pencil */}
      <div className="animate-f2" style={{ position: 'absolute', top: '45%', left: '6%', zIndex: 3, transform: 'rotate(15deg)' }}>
        <PencilDoodle />
      </div>

      {/* Bottom Right: Hand Drawn Book */}
      <div className="animate-f1" style={{ position: 'absolute', bottom: '8%', right: '5%', zIndex: 3, transform: 'rotate(-10deg) scale(1.35)' }}>
        <BookDoodle />
      </div>

      {/* Doodles */}
      <StarDoodle style={{ position: 'absolute', top: '25%', left: '35%', zIndex: 1 }} className="animate-wg" />
      <StarDoodle style={{ position: 'absolute', bottom: '30%', right: '8%', zIndex: 1 }} className="animate-wg" />
      <ArrowDoodle style={{ position: 'absolute', top: '18%', right: '35%', zIndex: 4, transform: 'rotate(20deg)' }} className="animate-wg" />

      {/* --- NAVBAR --- */}
      <div style={{
        position: 'absolute', top: 0, left: 0, width: '100%',
        display: 'flex', justifyContent: 'space-between', alignItems: 'center',
        padding: '24px 48px', zIndex: 20
      }}>
        <div style={{
          background: '#1F2A44', color: '#FFC857', padding: '10px 16px', borderRadius: '10px',
          fontFamily: "'Caveat', cursive", fontSize: '2rem', fontWeight: 'bold',
          transform: 'rotate(-2deg)', boxShadow: '4px 4px 0px rgba(31,42,68,0.2)'
        }}>
          The Scrapbook
        </div>
        <div style={{ display: 'flex', gap: '16px' }}>
          <button onClick={() => onNavigate('login')} className="neo-button" style={{
            background: '#fff', fontSize: '1.1rem', padding: '12px 28px'
          }}>
            Login
          </button>
          <button onClick={() => onNavigate('login')} className="neo-button" style={{
            background: '#E0C3FC', fontSize: '1.1rem', padding: '12px 28px'
          }}>
            Sign Up
          </button>
        </div>
      </div>

      {/* --- DEAD CENTER HERO SECTION --- */}
      <div style={{
        position: 'absolute',
        top: '50%',
        left: '50%',
        transform: 'translate(-50%, -50%)',
        zIndex: 10,
        width: '100%',
        maxWidth: '750px',
        textAlign: 'center'
      }}>
        <div style={{
          background: '#fff',
          border: '5px solid #1F2A44',
          boxShadow: '12px 12px 0px #1F2A44',
          borderRadius: '20px',
          padding: '50px 40px',
          position: 'relative',
          animation: 'popIn 0.8s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards'
        }}>
          {/* Top Tape overlaying hero */}
          <Tape top="-15px" left="50%" rotate={-2} color="rgba(181, 216, 247, 0.9)" />

          {/* Curated Chaos Tag */}
          <div style={{
            position: 'absolute', top: '-18px', right: '-25px',
            background: '#F4A4A4', color: '#1F2A44', padding: '10px 24px',
            border: '3px solid #1F2A44', borderRadius: '50px',
            fontWeight: '900', fontSize: '18px', boxShadow: '6px 6px 0px #1F2A44',
            transform: 'rotate(12deg)', zIndex: 11
          }}>
            Curated Chaos!
          </div>

          <h1 style={{
            fontSize: '5rem', fontWeight: '900', lineHeight: '1.2',
            color: '#1F2A44', marginBottom: '20px'
          }}>
            Welcome to <br />
            <span style={{ color: '#92681A', textDecoration: 'underline decoration-wavy', textUnderlineOffset: '10px' }}>
              Scrapbook
            </span>
          </h1>
          <p style={{
            fontSize: '1.5rem', color: '#4A5568', margin: '0 auto 40px auto',
            lineHeight: '1.6', maxWidth: '550px'
          }}>
            Your all-in-one SEO engine and journal. Animated, powerful, and built to rank your ideas.
          </p>

          <button onClick={() => onNavigate('journal')} className="neo-button">
            Start Your First Entry 🚀
          </button>
        </div>
      </div>
    </div>
  );
}