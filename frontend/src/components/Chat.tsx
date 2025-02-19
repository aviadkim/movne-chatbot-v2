import React, { useState } from 'react';
import './Chat.css';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const Chat: React.FC = () => {
    const [messages, setMessages] = useState<Array<{text: string, isBot: boolean}>>([]);
    const [input, setInput] = useState('');

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!input.trim()) return;

        // Add user message
        setMessages(prev => [...prev, { text: input, isBot: false }]);

        try {
            const response = await fetch(`${API_URL}/api/chat`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: input, language: 'he' })
            });
            const data = await response.json();
            
            // Add bot response
            setMessages(prev => [...prev, { text: data.response, isBot: true }]);
        } catch (error) {
            console.error('Error:', error);
        }

        setInput('');
    };

    return (
        <div className="chat-container">
            <div className="chat-header">
                <h1>Movne Chat - צ'אט מבנה</h1>
            </div>
            <div className="chat-messages">
                {messages.map((msg, index) => (
                    <div key={index} className={`message ${msg.isBot ? 'bot' : 'user'}`}>
                        {msg.text}
                    </div>
                ))}
            </div>
            <form onSubmit={handleSubmit} className="chat-input-form">
                <input
                    type="text"
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    placeholder="הקלד/י שאלה כאן..."
                    dir="rtl"
                />
                <button type="submit">שלח</button>
            </form>
        </div>
    );
};

export default Chat;
