import React, { useState } from 'react';

const TextAnalyzer = () => {
    const [text, setText] = useState('');
    const [entities, setEntities] = useState([]);

    const analyzeText = async () => {
        const response = await fetch('http://localhost:8000/api/analyze/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text }),
        });
        const data = await response.json();
        setEntities(data.entities);
    };

    return (
        <div>
            <textarea value={text} onChange={(e) => setText(e.target.value)} />
            <button onClick={analyzeText}>Analyze</button>
            <ul>
                {entities.map((entity, index) => (
                    <li key={index}>{entity[0]} - {entity[1]}</li>
                ))}
            </ul>
        </div>
    );
};

export default TextAnalyzer;