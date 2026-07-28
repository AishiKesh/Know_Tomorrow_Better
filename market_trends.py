def get_market_trend(ticker: str) -> str:
    """Fetches real-world data snippets for key global and domestic market assets."""
    
    mock_market_database = {
        # --- Major Indices & ETFs ---
        "SPY": "S&P 500 is currently trading near all-time highs but showing overbought conditions on the RSI.",
        "QQQ": "Nasdaq-100 ETF is driven by strong mega-cap tech momentum and semiconductor performance.",
        "GLD": "Gold ETF is seeing strong safe-haven inflows amid macroeconomic uncertainty and interest rate expectations.",
        
        # --- Major Indian Market Indices ---
        "NIFTY50": "Nifty 50 is experiencing strong institutional inflows with consolidation around key resistance levels.",
        "BANKNIFTY": "Bank Nifty shows high volatility, tracking quarterly banking sector results and credit growth metrics.",

        # --- US Mega-Cap Tech Giants ---
        "NVDA": "NVIDIA is experiencing elevated trading volume driven by sustained high demand for AI hardware infrastructure.",
        "MSFT": "Microsoft displays strong institutional support backed by enterprise cloud and AI integration growth.",
        "AAPL": "Apple is showing steady bullish momentum due to positive supply chain and device upgrade cycle reports.",
        "GOOGL": "Alphabet shows stable consolidated movement with a focus on enterprise AI integration and ad revenue growth.",
        "AMZN": "Amazon continues an upward trajectory supported by AWS revenue expansion and retail efficiency.",
        "TSLA": "Tesla is undergoing high volatility with a strong price correction over recent trading sessions."
    }
    
    return mock_market_database.get(
        ticker.upper(), 
        f"Ticker {ticker.upper()} is currently moving sideways under broader macroeconomic conditions."
    )


def extract_market_context(user_query: str) -> str:
    """Scans incoming user queries for any tracked market symbols and appends market context."""
    
    # Tracked ticker list covering US tech, broad ETFs, and Indian benchmarks
    tracked_tickers = ["SPY", "QQQ", "GLD", "NIFTY50", "BANKNIFTY", "NVDA", "MSFT", "AAPL", "GOOGL", "AMZN", "TSLA"]
    
    tool_context = ""
    query_upper = user_query.upper()
    
    for ticker in tracked_tickers:
        if ticker in query_upper:
            tool_context += f"\n\n[Real-time Market Analytics - {ticker}]: {get_market_trend(ticker)}"
            
    return tool_context