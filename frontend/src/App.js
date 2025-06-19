import React, { useState } from 'react';
import axios from 'axios';
import 'bootstrap/dist/css/bootstrap.min.css';

function App() {
  const [question, setQuestion] = useState('');
  const [answer, setAnswer] = useState('');
  const [loading, setLoading] = useState(false);

  const askQuestion = async () => {
    if (!question.trim()) return;

    setLoading(true);
    setAnswer('');

    try {
      const response = await axios.post('http://localhost:8000/ask', {
        question: question
      });
      setAnswer(response.data.answer);
    } catch (error) {
      console.error('API Error:', error);
      setAnswer('Something went wrong while contacting the AI.');
    }

    setLoading(false);
  };

  return (
    <div className="container mt-5">
      <h1 className="mb-4">AI Legal Assistant</h1>
      <div className="mb-3">
        <textarea
          className="form-control"
          rows="4"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder="Type your legal question..."
        ></textarea>
      </div>
      <button className="btn btn-primary mb-3" onClick={askQuestion} disabled={loading}>
        {loading ? 'Thinking...' : 'Ask AI'}
      </button>
      <div className="alert alert-secondary" role="alert">
        <strong>Answer:</strong>
        <p>{answer}</p>
      </div>
    </div>
  );
}

export default App;