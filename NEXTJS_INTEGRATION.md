"""
Next.js Frontend Example - Deepfake Detection

This file shows how to integrate the detection API with your Next.js frontend.
Copy and adapt these functions to your Next.js components.
"""

// pages/api/detect.js - Next.js API route
export default async function handler(req, res) {
    if (req.method !== 'POST') {
        return res.status(405).json({ error: 'Method not allowed' });
    }

    const { file, type } = req.body;

    try {
        const formData = new FormData();
        formData.append('file', file);

        const endpoint = type === 'video' 
            ? 'http://localhost:5000/api/detect-video'
            : 'http://localhost:5000/api/detect-image';

        const response = await fetch(endpoint, {
            method: 'POST',
            body: formData,
        });

        const data = await response.json();
        return res.status(response.status).json(data);
    } catch (error) {
        return res.status(500).json({ error: error.message });
    }
}


// components/DetectionForm.jsx - React component example
'use client';

import { useState } from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

export default function DetectionForm() {
    const [file, setFile] = useState(null);
    const [loading, setLoading] = useState(false);
    const [result, setResult] = useState(null);
    const [error, setError] = useState(null);

    const handleFileChange = (e) => {
        setFile(e.target.files[0]);
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!file) return;

        setLoading(true);
        setError(null);

        const formData = new FormData();
        formData.append('file', file);

        const type = file.type.includes('video') ? 'video' : 'image';
        const endpoint = type === 'video' 
            ? 'http://localhost:5000/api/detect-video'
            : 'http://localhost:5000/api/detect-image';

        try {
            const response = await fetch(endpoint, {
                method: 'POST',
                body: formData,
            });

            const data = await response.json();

            if (response.ok) {
                setResult(data);
            } else {
                setError(data.error || 'Detection failed');
            }
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    const chartData = result ? [
        {
            name: 'Probability',
            Real: (result.real_probability * 100).toFixed(2),
            Fake: (result.fake_probability * 100).toFixed(2),
        }
    ] : [];

    return (
        <div className="detection-form">
            <form onSubmit={handleSubmit}>
                <input 
                    type="file" 
                    onChange={handleFileChange}
                    accept="image/*,video/*"
                    disabled={loading}
                />
                <button type="submit" disabled={loading || !file}>
                    {loading ? 'Analyzing...' : 'Detect'}
                </button>
            </form>

            {error && <div className="error">{error}</div>}

            {result && (
                <div className="results">
                    <h3>Detection Results</h3>
                    <div className="info">
                        <p>Status: {result.status}</p>
                        <p>Real Probability: {(result.real_probability * 100).toFixed(2)}%</p>
                        <p>Fake Probability: {(result.fake_probability * 100).toFixed(2)}%</p>
                        <p>Classification: {result.is_fake ? 'FAKE' : 'REAL'}</p>
                        <p>Confidence: {(result.confidence * 100).toFixed(2)}%</p>
                    </div>

                    <ResponsiveContainer width="100%" height={300}>
                        <BarChart data={chartData}>
                            <CartesianGrid strokeDasharray="3 3" />
                            <XAxis dataKey="name" />
                            <YAxis />
                            <Tooltip />
                            <Legend />
                            <Bar dataKey="Real" fill="#8884d8" />
                            <Bar dataKey="Fake" fill="#ff7300" />
                        </BarChart>
                    </ResponsiveContainer>
                </div>
            )}
        </div>
    );
}


// styles/detection.css
.detection-form {
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-radius: 10px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
}

.detection-form form {
    display: flex;
    gap: 10px;
    margin-bottom: 20px;
}

.detection-form input[type="file"] {
    flex: 1;
    padding: 10px;
    border: 2px solid white;
    border-radius: 5px;
    background: white;
    cursor: pointer;
}

.detection-form button {
    padding: 10px 30px;
    background: white;
    color: #667eea;
    border: none;
    border-radius: 5px;
    font-weight: bold;
    cursor: pointer;
    transition: all 0.3s;
}

.detection-form button:hover:not(:disabled) {
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
}

.detection-form button:disabled {
    opacity: 0.6;
    cursor: not-allowed;
}

.error {
    color: #ff6b6b;
    background: #ffe0e0;
    padding: 15px;
    border-radius: 5px;
    margin-bottom: 20px;
}

.results {
    background: white;
    padding: 20px;
    border-radius: 5px;
    margin-top: 20px;
}

.results h3 {
    color: #333;
    margin-bottom: 15px;
}

.info {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 15px;
    margin-bottom: 20px;
}

.info p {
    background: #f5f5f5;
    padding: 10px;
    border-radius: 5px;
    margin: 0;
}
