
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [jobs, setJobs] = useState([]);
  const [selectedJob, setSelectedJob] = useState('');
  const [email, setEmail] = useState('');
  const [resume, setResume] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  // Fetch jobs on load from FastAPI backend
  useEffect(() => {
    axios.get('http://127.0.0.1:8000/jobs/')
      .then(res => setJobs(res.data))
      .catch(err => console.error("Error fetching jobs:", err));
  }, []);

  const handleApply = async (e) => {
    e.preventDefault();
    if (!selectedJob || !email || !resume) {
      alert("Please fill all fields and select a resume PDF!");
      return;
    }

    const formData = new FormData();
    formData.append("candidate_email", email);
    formData.append("resume", resume);

    setLoading(true);
    try {
      const response = await axios.post(`http://127.0.0.1:8000/apply/${selectedJob}`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      setResult(response.data);
      alert("Resume analyzed successfully!");
    } catch (err) {
      console.error("Error uploading resume:", err);
      alert("Error uploading resume. Check backend terminal for details.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: '40px', fontFamily: 'Arial', maxWidth: '800px', margin: 'auto' }}>
      <h1>🚀 HireFlow AI - Recruitment Dashboard</h1>
      <p>AI-Powered ATS Resume Matcher for Internships & Jobs</p>

      <hr style={{ margin: '20px 0' }} />

      <h2>Apply for a Job</h2>
      <form onSubmit={handleApply} style={{ display: 'flex', flexDirection: 'column', gap: '15px' }}>
        <div>
          <label><strong>Select Job Position: </strong></label>
          <select value={selectedJob} onChange={(e) => setSelectedJob(e.target.value)} style={{ padding: '8px', width: '100%', marginTop: '5px' }}>
            <option value="">-- Choose a Job --</option>
            {jobs.map(job => (
              <option key={job.id} value={job.id}>{job.title} - (Skills: {job.required_skills})</option>
            ))}
          </select>
        </div>

        <div>
          <label><strong>Your Email: </strong></label>
          <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} placeholder="name@example.com" style={{ padding: '8px', width: '100%', marginTop: '5px' }} />
        </div>

        <div>
          <label><strong>Upload Resume (PDF): </strong></label>
          <input type="file" accept=".pdf" onChange={(e) => setResume(e.target.files[0])} style={{ padding: '8px', width: '100%', marginTop: '5px' }} />
        </div>

        <button type="submit" disabled={loading} style={{ padding: '12px', background: '#007bff', color: '#fff', border: 'none', cursor: 'pointer', fontSize: '16px', borderRadius: '4px' }}>
          {loading ? "Analyzing Resume with AI..." : "Submit & Get ATS Score"}
        </button>
      </form>

      {result && (
        <div style={{ marginTop: '30px', padding: '20px', background: '#f8f9fa', borderLeft: '5px solid #28a745', borderRadius: '4px' }}>
          <h3>🎯 ATS Evaluation Result</h3>
          <p><strong>Match Score:</strong> <span style={{ fontSize: '22px', color: '#28a745', fontWeight: 'bold' }}>{result.match_score}%</span></p>
          <p><strong>Matched Skills:</strong> {result.matched_skills || "None"}</p>
          <p><strong>Missing Skills:</strong> {result.missing_skills || "None"}</p>
          <p><strong>Status:</strong> {result.status}</p>
        </div>
      )}
    </div>
  );
}

export default App;