import React from 'react';
import './LandingPage.css';
import {
    Science,
    Assessment,
    Psychology,
    TrendingUp,
    Security,
    Speed,
    Biotech
} from '@mui/icons-material';

const LandingPage = ({ onStart }) => {
    return (
        <div className="landing-page">
            {/* Navigation */}
            <nav className="nav-bar glass-effect">
                <div className="container nav-content">
                    <div className="logo">
                        <Biotech sx={{ fontSize: 32, color: '#2563EB' }} />
                        <span>MedCore AI</span>
                    </div>
                    <button className="btn btn-primary" onClick={onStart}>
                        Launch Platform
                    </button>
                </div>
            </nav>

            {/* Hero Section */}
            <header className="hero-section container">
                <div className="animate-fade-in">
                    <div className="inline-block px-4 py-1.5 mb-6 rounded-full bg-blue-50 text-blue-700 text-sm font-medium border border-blue-100">
                        ✨ Next Generation Pharmaceutical Research
                    </div>
                    <h1 className="hero-title">
                        Accelerate Drug Discovery<br />
                        with Agentic AI
                    </h1>
                    <p className="hero-subtitle">
                        Orchestrate 7 specialized AI agents to analyze clinical trials, patents,
                        and market data in real-time. Reduce research time from weeks to minutes.
                    </p>
                    <button className="btn btn-primary" onClick={onStart}>
                        Start Research Now
                    </button>

                    <div className="stats-container">
                        <div className="stat-item">
                            <span className="stat-value">96%</span>
                            <span className="stat-label">Time Reduction</span>
                        </div>

                        <div className="stat-item">
                            <span className="stat-value">7</span>
                            <span className="stat-label">Specialized Agents</span>
                        </div>
                    </div>
                </div>
            </header>

            {/* Bento Grid Features */}
            <section className="container">
                <div className="bento-grid">
                    {/* Feature 1 - Large */}
                    <div className="bento-item bento-large animate-fade-in delay-1">
                        <div>
                            <div className="card-icon">
                                <Psychology />
                            </div>
                            <h3 className="card-title">Multi-Agent Orchestration</h3>
                            <p className="card-desc">
                                A master agent intelligently decomposes complex research queries into
                                specialized tasks, coordinating a fleet of expert agents for
                                comprehensive analysis.
                            </p>
                        </div>
                    </div>

                    {/* Feature 2 */}
                    <div className="bento-item animate-fade-in delay-2">
                        <div>
                            <div className="card-icon">
                                <Science />
                            </div>
                            <h3 className="card-title">Clinical Intelligence</h3>
                            <p className="card-desc">
                                Real-time analysis of clinical trials data, phase distribution,
                                and recruitment status.
                            </p>
                        </div>
                    </div>

                    {/* Feature 3 */}
                    <div className="bento-item animate-fade-in delay-3">
                        <div>
                            <div className="card-icon">
                                <Security />
                            </div>
                            <h3 className="card-title">Patent Landscape</h3>
                            <p className="card-desc">
                                Instant IP analysis covering active patents, expiry dates,
                                and freedom-to-operate checks.
                            </p>
                        </div>
                    </div>

                    {/* Feature 4 */}
                    <div className="bento-item animate-fade-in delay-4">
                        <div>
                            <div className="card-icon">
                                <TrendingUp />
                            </div>
                            <h3 className="card-title">Market Analysis</h3>
                            <p className="card-desc">
                                Deep dive into market size, CAGR, and competitive landscape
                                for any therapeutic area.
                            </p>
                        </div>
                    </div>

                    {/* Feature 5 */}
                    <div className="bento-item animate-fade-in delay-4">
                        <div>
                            <div className="card-icon">
                                <Assessment />
                            </div>
                            <h3 className="card-title">Automated Reporting</h3>
                            <p className="card-desc">
                                Generate professional PDF reports with executive summaries
                                and citations instantly.
                            </p>
                        </div>
                    </div>

                    {/* Feature 6 - Large */}
                    <div className="bento-item bento-large animate-fade-in delay-3">
                        <div>
                            <div className="card-icon">
                                <Speed />
                            </div>
                            <h3 className="card-title">Real-Time Synthesis</h3>
                            <p className="card-desc">
                                Our LLM engine synthesizes data from PubMed, ClinicalTrials.gov,
                                and USPTO into a cohesive narrative, identifying hidden connections
                                and opportunities.
                            </p>
                        </div>
                    </div>
                </div>
            </section>

            {/* Footer */}
            <footer className="footer">
                <div className="container text-center text-secondary">
                    <p>© 2024 MedCore AI Platform. All rights reserved.</p>
                </div>
            </footer>
        </div>
    );
};

export default LandingPage;
