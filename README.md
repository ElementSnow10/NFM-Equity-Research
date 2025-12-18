NFM-Equity-Research is a research-focused equity analysis platform that uses a New Fundamental Model (NFM) combined with LLM-based reasoning to identify, rank, and continuously monitor the fundamentally strongest companies in the Indian stock market. Sync all.

The system evaluates ~6,000 listed Indian companies using multi-factor fundamental data, selects the Top 50 companies, generates explainable research justifications, and dynamically updates the list as business fundamentals evolve.

This project is designed to emulate and potentially outperform high-performance LLM-driven equity research systems (≈50% XIRR benchmarks) through transparent scoring, continuous monitoring, and automated churn logic.

Objectives:

- Build a scalable fundamentals-driven equity screening engine
- Rank Indian equities using a weighted New Fundamental Model
- Generate human-readable reasoning for stock selection using LLMs
- Monitor deterioration signals and trigger early warnings
- Maintain a dynamic Top 50 list via automated churn decisions

High-Level Architecture:

- Market Universe (~6,000 Stocks)
- Fundamental Data Ingestion
- Feature Engineering (40+ Parameters)
- NFM Weighted Scoring Engine  
- Top 50 Stock Selection   
- LLM-Based Research & Explanation    
- Continuous Monitoring & Alerts       
- Churn (Add / Remove Companies)


NFM-Equity-Research/
│
├── data/                 # Raw & processed financial data
├── features/             # Feature engineering & parameter logic
├── scoring/              # NFM scoring & ranking models
├── monitoring/           # Continuous tracking & alerts
├── churn/                # Add/remove decision logic
├── llm/                  # Prompting & explanation generation
├── reports/              # Company-level research outputs
├── notebooks/            # Research & experimentation
├── config/               # Parameter configs & weights
├── README.md
└── requirements.txt
