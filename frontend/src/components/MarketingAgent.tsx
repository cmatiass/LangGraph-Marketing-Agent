import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import { Play, RefreshCw, Copy, Download } from 'lucide-react';

interface LogEntry {
  type: string;
  message: string;
  timestamp: string;
}

interface ResearchFindings {
  topic: string;
  key_points: string[];
  competitor_insights: string[];
  trending_hashtags: string[];
  audience_demographics: {
    age_range: string;
    interests: string[];
    platforms: string[];
  };
  success_criteria: string[];
}

interface TaskResult {
  initial_request: string;
  research_findings: ResearchFindings;
  draft_post: string;
  iteration_count: number;
  critiques: string[];
  human_approved: boolean;
  approval_attempts: number;
  report_path?: string;
}

interface WebSocketMessage {
  type: string;
  status?: string;
  progress?: number;
  current_step?: string;
  message?: string;
  research_findings?: ResearchFindings;
  draft_post?: string;
  iteration?: number;
  iteration_count?: number;
  critiques?: string[];
  critiques_addressed?: string[];
  result?: TaskResult;
  error?: string;
  task_id?: string;
}

interface HumanApprovalData {
  task_id: string;
  draft_post: string;
  research_findings: ResearchFindings;
  iteration_count: number;
  critiques: string[];
}

// API Configuration - automatically detects environment
const API_BASE_URL = process.env.NODE_ENV === 'production' 
  ? window.location.origin 
  : 'http://localhost:8000';

const MarketingAgent: React.FC = () => {
  const [request, setRequest] = useState('');
  const [maxIterations, setMaxIterations] = useState(3);
  const [isRunning, setIsRunning] = useState(false);
  const [taskId, setTaskId] = useState<string | null>(null);
  const [progress, setProgress] = useState(0);
  const [currentStep, setCurrentStep] = useState('');
  const [status, setStatus] = useState<'idle' | 'running' | 'completed' | 'error'>('idle');
  const [logs, setLogs] = useState<LogEntry[]>([]);
  const [result, setResult] = useState<TaskResult | null>(null);
  const [examples, setExamples] = useState<string[]>([]);
  const [websocket, setWebsocket] = useState<WebSocket | null>(null);
  const [connectionStatus, setConnectionStatus] = useState<'disconnected' | 'connecting' | 'connected'>('disconnected');
  const [awaitingApproval, setAwaitingApproval] = useState(false);
  const [approvalData, setApprovalData] = useState<HumanApprovalData | null>(null);
  const [humanFeedback, setHumanFeedback] = useState('');
  
  const logOutputRef = useRef<HTMLDivElement>(null);
  const clientId = useRef(Math.random().toString(36).substr(2, 9));

  useEffect(() => {
    // Load example requests
    loadExamples();
    
    // Initialize WebSocket connection
    connectWebSocket();
    
    return () => {
      if (websocket) {
        websocket.close();
      }
    };
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  useEffect(() => {
    // Auto-scroll logs to bottom
    if (logOutputRef.current) {
      logOutputRef.current.scrollTop = logOutputRef.current.scrollHeight;
    }
  }, [logs]);

  const loadExamples = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/api/marketing/examples`);
      setExamples(response.data.examples);
    } catch (error) {
      console.error('Error loading examples:', error);
      setExamples([
        'Create a marketing post for a new AI-powered productivity app',
        'Generate content promoting a sustainable fashion brand',
        'Write a post for a local coffee shop\'s grand opening'
      ]);
    }
  };

  const connectWebSocket = () => {
    setConnectionStatus('connecting');
    
    // WebSocket connection - automatically detects environment
    const wsProtocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const wsHost = process.env.NODE_ENV === 'production' 
      ? window.location.host 
      : 'localhost:8000';
    const ws = new WebSocket(`${wsProtocol}//${wsHost}/ws/${clientId.current}`);
    
    ws.onopen = () => {
      console.log('WebSocket connected');
      setConnectionStatus('connected');
      addLog('system', 'Connected to LangGraph Marketing Agent');
    };
    
    ws.onmessage = (event) => {
      try {
        const data: WebSocketMessage = JSON.parse(event.data);
        handleWebSocketMessage(data);
      } catch (error) {
        console.error('Error parsing WebSocket message:', error);
        addLog('error', 'Error parsing server message');
      }
    };
    
    ws.onerror = (error) => {
      console.error('WebSocket error:', error);
      setConnectionStatus('disconnected');
      addLog('error', 'Connection error occurred');
    };
    
    ws.onclose = () => {
      console.log('WebSocket disconnected');
      setConnectionStatus('disconnected');
      addLog('system', 'Disconnected from server');
      
      // Attempt to reconnect after 5 seconds if not manually closed
      if (status === 'running') {
        setTimeout(connectWebSocket, 5000);
      }
    };
    
    setWebsocket(ws);
  };

  const handleWebSocketMessage = (data: WebSocketMessage) => {
    switch (data.type) {
      case 'status':
        if (data.status) setStatus(data.status as any);
        if (data.progress !== undefined) setProgress(data.progress);
        if (data.current_step) setCurrentStep(data.current_step);
        if (data.message) addLog('info', data.message);
        break;
        
      case 'log':
        if (data.message) addLog('info', data.message);
        break;
        
      case 'research_complete':
        if (data.message) addLog('success', data.message);
        break;
        
      case 'draft_created':
        if (data.message) addLog('success', data.message);
        break;
        
      case 'critique_complete':
        if (data.critiques && data.critiques.length > 0) {
          addLog('info', data.message || `Found ${data.critiques.length} critiques`);
          data.critiques.forEach((critique, index) => {
            addLog('info', `  ${index + 1}. ${critique}`);
          });
        } else {
          addLog('success', data.message || 'No critiques found - draft is ready!');
        }
        break;
        
      case 'draft_refined':
        if (data.message) addLog('success', data.message);
        break;
        
      case 'awaiting_human_approval':
        setAwaitingApproval(true);
        setApprovalData({
          task_id: data.task_id || taskId || '',
          draft_post: data.draft_post || '',
          research_findings: data.research_findings || {} as ResearchFindings,
          iteration_count: data.iteration_count || 0,
          critiques: data.critiques || []
        });
        addLog('info', '👤 Ready for human review - please approve, reject, or provide feedback');
        break;
        
      case 'generation_complete':
        setStatus('completed');
        setProgress(100);
        setCurrentStep('Completed');
        setIsRunning(false);
        if (data.result) {
          setResult(data.result);
          addLog('success', '🎉 Marketing post generation completed successfully!');
        }
        break;
        
      case 'generation_error':
        setStatus('error');
        setIsRunning(false);
        addLog('error', `❌ Error: ${data.error || 'Unknown error occurred'}`);
        break;
        
      case 'error':
        addLog('error', data.message || 'An error occurred');
        break;
        
      default:
        console.log('Unknown WebSocket message type:', data.type);
    }
  };

  const addLog = (type: string, message: string) => {
    const entry: LogEntry = {
      type,
      message,
      timestamp: new Date().toLocaleTimeString()
    };
    setLogs(prev => [...prev, entry]);
  };

  const startGeneration = async () => {
    if (!request.trim()) {
      alert('Please enter a marketing request');
      return;
    }
    
    if (connectionStatus !== 'connected') {
      alert('Not connected to server. Please wait for connection to establish.');
      return;
    }

    try {
      setIsRunning(true);
      setStatus('running');
      setProgress(0);
      setCurrentStep('Starting');
      setResult(null);
      setLogs([]);
      
      // Create task
      const response = await axios.post(`${API_BASE_URL}/api/marketing/generate`, {
        request,
        max_iterations: maxIterations
      });
      
      const newTaskId = response.data.task_id;
      setTaskId(newTaskId);
      
      addLog('system', `Task created with ID: ${newTaskId}`);
      
      // Start generation via WebSocket
      if (websocket && websocket.readyState === WebSocket.OPEN) {
        websocket.send(JSON.stringify({
          type: 'start_generation',
          task_id: newTaskId
        }));
      } else {
        throw new Error('WebSocket connection not available');
      }
      
    } catch (error: any) {
      console.error('Error starting generation:', error);
      setIsRunning(false);
      setStatus('error');
      addLog('error', `Failed to start generation: ${error.message}`);
    }
  };

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text).then(() => {
      addLog('success', 'Content copied to clipboard');
    }).catch(() => {
      addLog('error', 'Failed to copy to clipboard');
    });
  };

  const resetForm = () => {
    setRequest('');
    setMaxIterations(3);
    setStatus('idle');
    setProgress(0);
    setCurrentStep('');
    setResult(null);
    setLogs([]);
    setTaskId(null);
    setIsRunning(false);
    setAwaitingApproval(false);
    setApprovalData(null);
    setHumanFeedback('');
  };

  const handleHumanApproval = (action: 'approve' | 'reject' | 'feedback') => {
    if (!websocket || !approvalData) return;

    const feedbackData = {
      type: 'human_feedback',
      task_id: approvalData.task_id,
      feedback: {
        action,
        feedback: action === 'feedback' ? humanFeedback : ''
      }
    };

    websocket.send(JSON.stringify(feedbackData));
    
    if (action === 'approve') {
      addLog('success', '✅ Post approved by human reviewer');
      setAwaitingApproval(false);
      setApprovalData(null);
    } else if (action === 'reject') {
      addLog('info', '❌ Post rejected - continuing refinement process');
      setAwaitingApproval(false);
      setApprovalData(null);
      setStatus('running');
    } else if (action === 'feedback') {
      if (!humanFeedback.trim()) {
        alert('Please provide feedback before submitting');
        return;
      }
      addLog('info', `💬 Human feedback provided: ${humanFeedback}`);
      setAwaitingApproval(false);
      setApprovalData(null);
      setHumanFeedback('');
      setStatus('running');
    }
  };

  const getStatusClassName = () => {
    switch (status) {
      case 'running': return 'status-display running';
      case 'completed': return 'status-display completed';
      case 'error': return 'status-display error';
      default: return 'status-display';
    }
  };

  const getStatusIcon = () => {
    switch (status) {
      case 'running': return <RefreshCw className="spinner" size={20} />;
      case 'completed': return '✅';
      case 'error': return '❌';
      default: return '⚪';
    }
  };

  return (
    <div className="marketing-agent">
      {/* Header */}
      <div className="agent-header">
        <h1>🤖 LangGraph Marketing Agent</h1>
        <p>AI-Powered Marketing Content Generator with Self-Correction</p>
      </div>

      {/* Main Content */}
      <div className="agent-content">
        {/* Input Section */}
        <div className="input-section">
          <h2>📝 Configure Your Request</h2>
          
          <div className="form-group">
            <label htmlFor="request">Marketing Request</label>
            <textarea
              id="request"
              className="form-control"
              placeholder="Describe the marketing content you need..."
              value={request}
              onChange={(e) => setRequest(e.target.value)}
              disabled={isRunning}
            />
          </div>

          <div className="form-group">
            <label>Quick Examples</label>
            <div className="examples-grid">
              {examples.map((example, index) => (
                <button
                  key={index}
                  className={`example-btn ${request === example ? 'selected' : ''}`}
                  onClick={() => setRequest(example)}
                  disabled={isRunning}
                >
                  {example}
                </button>
              ))}
            </div>
          </div>

          <div className="form-group">
            <label htmlFor="maxIterations">Max Refinement Iterations</label>
            <select
              id="maxIterations"
              className="form-control"
              value={maxIterations}
              onChange={(e) => setMaxIterations(Number(e.target.value))}
              disabled={isRunning}
            >
              <option value={1}>1 iteration</option>
              <option value={2}>2 iterations</option>
              <option value={3}>3 iterations (recommended)</option>
              <option value={4}>4 iterations</option>
              <option value={5}>5 iterations</option>
            </select>
          </div>

          <div className="form-group">
            <button
              className="btn btn-primary"
              onClick={startGeneration}
              disabled={isRunning || connectionStatus !== 'connected'}
              style={{ width: '100%', marginBottom: '10px' }}
            >
              <Play size={16} />
              {isRunning ? 'Generating...' : 'Generate Marketing Post'}
            </button>
            
            <button
              className="btn btn-secondary"
              onClick={resetForm}
              disabled={isRunning}
              style={{ width: '100%' }}
            >
              <RefreshCw size={16} />
              Reset
            </button>
          </div>

          <div className="form-group">
            <small style={{ color: connectionStatus === 'connected' ? '#28a745' : '#dc3545' }}>
              Connection: {connectionStatus}
            </small>
          </div>
        </div>

        {/* Output Section */}
        <div className="output-section">
          <h2>📊 Live Process Monitor</h2>

          {/* Status Display */}
          <div className={getStatusClassName()}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '10px' }}>
              {getStatusIcon()}
              <strong>{currentStep || 'Ready to start'}</strong>
            </div>
            
            {isRunning && (
              <div className="progress">
                <div 
                  className="progress-bar" 
                  style={{ width: `${progress}%` }}
                ></div>
              </div>
            )}
            
            <div style={{ fontSize: '14px', opacity: 0.8 }}>
              Progress: {progress}%
              {taskId && (
                <span style={{ marginLeft: '10px' }}>
                  Task ID: {taskId.substring(0, 8)}...
                </span>
              )}
            </div>
          </div>

          {/* Live Logs */}
          <div className="log-output" ref={logOutputRef}>
            {logs.length === 0 ? (
              <div style={{ color: '#888', textAlign: 'center', padding: '20px' }}>
                Process logs will appear here in real-time...
              </div>
            ) : (
              logs.map((log, index) => (
                <div key={index} className="log-entry">
                  <span className="log-timestamp">{log.timestamp}</span>
                  <span className={`log-message ${log.type}`}>
                    {log.message}
                  </span>
                </div>
              ))
            )}
          </div>

          {/* Human Approval Interface */}
          {awaitingApproval && approvalData && (
            <div className="result-display" style={{ marginTop: '20px', borderLeft: '4px solid #ffc107' }}>
              <h3>👤 Human Review Required</h3>
              <p style={{ marginBottom: '15px', color: '#666' }}>
                Please review the marketing post below and decide whether to approve it, reject it, or provide specific feedback for improvement.
              </p>
              
              <div className="result-content" style={{ marginBottom: '20px' }}>
                <strong>Draft Post (Iteration {approvalData.iteration_count}):</strong>
                <div style={{ marginTop: '10px', padding: '15px', background: '#f8f9fa', borderRadius: '8px', border: '1px solid #e5e5e5' }}>
                  {approvalData.draft_post}
                </div>
              </div>

              {approvalData.critiques.length > 0 && (
                <div style={{ marginBottom: '20px' }}>
                  <strong>Outstanding Issues:</strong>
                  <ul style={{ marginTop: '10px', paddingLeft: '20px' }}>
                    {approvalData.critiques.map((critique, index) => (
                      <li key={index} style={{ margin: '5px 0', color: '#666' }}>{critique}</li>
                    ))}
                  </ul>
                </div>
              )}

              <div style={{ marginBottom: '15px' }}>
                <label htmlFor="human-feedback" style={{ display: 'block', marginBottom: '5px', fontWeight: '600' }}>
                  Provide specific feedback (optional):
                </label>
                <textarea
                  id="human-feedback"
                  className="form-control"
                  placeholder="Enter specific improvements you'd like to see..."
                  value={humanFeedback}
                  onChange={(e) => setHumanFeedback(e.target.value)}
                  style={{ minHeight: '80px' }}
                />
              </div>

              <div style={{ display: 'flex', gap: '10px', flexWrap: 'wrap' }}>
                <button
                  className="btn btn-primary"
                  onClick={() => handleHumanApproval('approve')}
                >
                  ✅ Approve & Complete
                </button>
                <button
                  className="btn btn-secondary"
                  onClick={() => handleHumanApproval('reject')}
                >
                  ❌ Reject & Retry
                </button>
                <button
                  className="btn btn-secondary"
                  onClick={() => handleHumanApproval('feedback')}
                  disabled={!humanFeedback.trim()}
                >
                  💬 Submit Feedback & Refine
                </button>
              </div>
            </div>
          )}

          {/* Results */}
          {result && (
            <div className="result-display">
              <h3>🎯 Final Marketing Post</h3>
              <div className="result-content">
                {result.draft_post}
              </div>
              
              <div style={{ marginTop: '15px', display: 'flex', gap: '10px' }}>
                <button
                  className="btn btn-secondary"
                  onClick={() => copyToClipboard(result.draft_post)}
                >
                  <Copy size={16} />
                  Copy Post
                </button>
                
                {result.report_path && (
                  <button className="btn btn-secondary">
                    <Download size={16} />
                    Download Report
                  </button>
                )}
              </div>

              {/* Research Findings */}
              {result.research_findings && (
                <div className="research-findings">
                  <h4>🔬 Research Findings</h4>
                  
                  <div>
                    <strong>Key Points:</strong>
                    <ul>
                      {result.research_findings.key_points.map((point, index) => (
                        <li key={index}>{point}</li>
                      ))}
                    </ul>
                  </div>

                  <div>
                    <strong>Target Audience:</strong> {result.research_findings.audience_demographics.age_range} interested in {result.research_findings.audience_demographics.interests.join(', ')}
                  </div>

                  <div>
                    <strong>Platforms:</strong> {result.research_findings.audience_demographics.platforms.join(', ')}
                  </div>

                  <div>
                    <strong>Hashtags:</strong> {result.research_findings.trending_hashtags.join(', ')}
                  </div>
                </div>
              )}

              {/* Process Summary */}
              <div style={{ marginTop: '15px', padding: '15px', background: '#f8f9fa', borderRadius: '8px' }}>
                <strong>Process Summary:</strong>
                <ul style={{ margin: '10px 0', paddingLeft: '20px' }}>
                  <li>Refinement iterations: {result.iteration_count}</li>
                  <li>Outstanding critiques: {result.critiques.length}</li>
                  <li>Human approval: {result.human_approved ? 'Yes' : 'Pending'}</li>
                </ul>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default MarketingAgent;
