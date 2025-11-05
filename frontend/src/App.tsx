import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import './App.css';

function App() {
  const [message, setMessage] = useState('');

  const testBackend = async () => {
    try {
      const response = await fetch('http://localhost:8001/test');
      const data = await response.json();
      setMessage(`Backend connected! ${data.test} - Python ${data.python_version}`);
    } catch (error) {
      setMessage('Backend connection failed. Make sure Flask is running on port 8001.');
    }
  };

  return (
    <Router>
      <div className="App">
        <nav className="navbar">
          <div className="container navbar-content">
            <Link to="/" className="logo">🎨 ArtBuddy</Link>
            <div className="nav-links">
              <Link to="/" className="nav-link">Home</Link>
              <Link to="/gallery" className="nav-link">Gallery</Link>
              <Link to="/generate" className="nav-link">Generate</Link>
            </div>
          </div>
        </nav>

        <Routes>
          <Route path="/" element={<Home testBackend={testBackend} message={message} />} />
          <Route path="/gallery" element={<Gallery />} />
          <Route path="/generate" element={<Generate />} />
        </Routes>
      </div>
    </Router>
  );
}

function Home({ testBackend, message }: { testBackend: () => void; message: string }) {
  return (
    <div className="container">
      <div className="hero">
        <h1>AI Art Generator</h1>
        <p>Create amazing artwork with the power of AI</p>
        <div>
          <button onClick={testBackend} className="btn btn-primary">
            Test Backend Connection
          </button>
        </div>
        {message && (
          <div className={`mt-4 ${message.includes('failed') ? 'error' : 'success'}`}>
            {message}
          </div>
        )}
      </div>
    </div>
  );
}

function Gallery() {
  const [images, setImages] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);

  const loadGallery = async () => {
    setLoading(true);
    try {
      const response = await fetch('http://localhost:8001/gallery');
      const data = await response.json();
      setImages(data.images || []);
    } catch (error) {
      console.error('Failed to load gallery');
    } finally {
      setLoading(false);
    }
  };

  // Auto-load gallery on component mount
  React.useEffect(() => {
    loadGallery();
  }, []);

  const downloadImage = (filename: string) => {
    const link = document.createElement('a');
    link.href = `http://localhost:8001/download/${filename}`;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
    <div className="container">
      <div className="hero">
        <h1>Gallery</h1>
        <p>Discover amazing AI-generated artwork</p>
        <button onClick={loadGallery} className="btn btn-primary">
          Load Gallery
        </button>
      </div>
      
      {loading && <div className="text-center"><span className="loading"></span></div>}
      
      <div className="grid grid-3">
        {images.map((img, index) => (
          <div key={index} className="card">
            <img 
              src={img.full_url}
              alt={img.prompt || `Generated artwork ${index + 1}`}
              style={{ 
                width: '100%', 
                height: '200px',
                objectFit: 'cover',
                borderRadius: '8px'
              }}
              onLoad={() => console.log('Image loaded:', img.filename)}
              onError={(e) => {
                console.error('Failed to load image:', img.full_url);
                e.currentTarget.src = 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjAwIiBoZWlnaHQ9IjIwMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cmVjdCB3aWR0aD0iMTAwJSIgaGVpZ2h0PSIxMDAlIiBmaWxsPSIjZGRkIi8+PHRleHQgeD0iNTAlIiB5PSI1MCUiIGZvbnQtZmFtaWx5PSJBcmlhbCIgZm9udC1zaXplPSIxNCIgZmlsbD0iIzk5OSIgdGV4dC1hbmNob3I9Im1pZGRsZSIgZHk9Ii4zZW0iPkltYWdlIEVycm9yPC90ZXh0Pjwvc3ZnPg==';
              }}
            />
            <div style={{ padding: '8px', fontSize: '12px', color: 'rgba(255,255,255,0.8)' }}>
              {img.prompt && img.prompt.length > 30 ? img.prompt.substring(0, 30) + '...' : img.prompt}
            </div>
            <div style={{ marginTop: '8px', textAlign: 'center' }}>
              <button 
                onClick={() => downloadImage(img.filename)}
                className="btn btn-primary"
                style={{ fontSize: '12px', padding: '4px 8px' }}
              >
                Download
              </button>
            </div>
          </div>
        ))}
      </div>
      
      {images.length === 0 && !loading && (
        <div style={{ textAlign: 'center', marginTop: '40px', color: 'rgba(255,255,255,0.6)' }}>
          No images found. Generate some artwork first!
        </div>
      )}
    </div>
  );
}

function Generate() {
  const [prompt, setPrompt] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState('');

  const handleGenerate = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setResult(null);
    setError('');

    try {
      const response = await fetch('http://localhost:8001/generate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          prompt: prompt,
          width: 512,
          height: 512
        })
      });

      const data = await response.json();
      
      if (data.success) {
        setResult(data);
      } else {
        setError(data.error || 'Generation failed');
      }
    } catch (error) {
      setError('Failed to connect to backend. Make sure Flask is running on port 8001.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <div className="hero">
        <h1>Generate Art</h1>
        <p>Describe your vision and let AI create it</p>
      </div>

      <div className="grid grid-2">
        <div className="card">
          <form onSubmit={handleGenerate}>
            <div className="form-group">
              <label>Describe your artwork:</label>
              <input
                type="text"
                className="input"
                value={prompt}
                onChange={(e) => setPrompt(e.target.value)}
                placeholder="A beautiful sunset over mountains..."
                required
              />
            </div>
            <button 
              type="submit" 
              className="btn btn-primary" 
              disabled={loading}
              style={{ width: '100%' }}
            >
              {loading ? <span className="loading"></span> : 'Generate Artwork'}
            </button>
          </form>

          {error && (
            <div className="error mt-4">
              {error}
            </div>
          )}
        </div>

        <div className="card">
          {result ? (
            <div>
              <h3>Generated Artwork</h3>
              <img 
                src={result.full_url || `http://localhost:8001${result.image_url}`}
                alt={result.prompt}
                style={{ 
                  width: '100%', 
                  borderRadius: '8px',
                  marginTop: '16px'
                }}
                onError={(e) => {
                  console.error('Image failed to load:', result.full_url || result.image_url);
                  e.currentTarget.style.display = 'none';
                }}
              />
              <p className="mt-4" style={{ color: 'rgba(255,255,255,0.8)' }}>
                Prompt: {result.prompt}
              </p>
              <div className="success mt-4">
                {result.message}
              </div>
              <button 
                onClick={() => {
                  const link = document.createElement('a');
                  link.href = result.full_url || `http://localhost:8001${result.image_url}`;
                  link.download = (result.image_url || 'artwork.png').split('/').pop();
                  document.body.appendChild(link);
                  link.click();
                  document.body.removeChild(link);
                }}
                className="btn btn-primary"
                style={{ marginTop: '8px', width: '100%' }}
              >
                Download Image
              </button>
            </div>
          ) : (
            <div style={{ 
              height: '300px',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              color: 'rgba(255,255,255,0.5)',
              border: '2px dashed rgba(255,255,255,0.3)',
              borderRadius: '8px'
            }}>
              Your generated artwork will appear here
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;