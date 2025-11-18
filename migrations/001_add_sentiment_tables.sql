-- Migration: Add News and Sentiment Analysis Tables
-- Created: 2025-01-18
-- Description: Adds tables for news articles and sentiment scores

-- News Articles Table
CREATE TABLE IF NOT EXISTS news_articles (
    id SERIAL PRIMARY KEY,
    ticker_id INTEGER REFERENCES tickers(id),
    symbol VARCHAR(10) NOT NULL,
    title TEXT NOT NULL,
    summary TEXT,
    url TEXT,
    source VARCHAR(100),
    author VARCHAR(255),
    published_at TIMESTAMP WITH TIME ZONE,
    category VARCHAR(50),
    tags JSONB,
    image_url TEXT,
    is_breaking BOOLEAN DEFAULT FALSE,
    fetched_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE,

    -- Indexes
    CONSTRAINT news_articles_ticker_id_idx FOREIGN KEY (ticker_id) REFERENCES tickers(id)
);

CREATE INDEX IF NOT EXISTS idx_news_articles_ticker_id ON news_articles(ticker_id);
CREATE INDEX IF NOT EXISTS idx_news_articles_symbol ON news_articles(symbol);
CREATE INDEX IF NOT EXISTS idx_news_articles_published_at ON news_articles(published_at);
CREATE INDEX IF NOT EXISTS idx_news_articles_is_breaking ON news_articles(is_breaking);
CREATE INDEX IF NOT EXISTS idx_news_articles_fetched_at ON news_articles(fetched_at);

-- Sentiment Scores Table
CREATE TABLE IF NOT EXISTS sentiment_scores (
    id SERIAL PRIMARY KEY,
    ticker_id INTEGER REFERENCES tickers(id),
    symbol VARCHAR(10) NOT NULL,
    news_article_id INTEGER REFERENCES news_articles(id),

    -- Sentiment scores (-1 to 1)
    score FLOAT NOT NULL,
    positive FLOAT DEFAULT 0.0,
    negative FLOAT DEFAULT 0.0,
    neutral FLOAT DEFAULT 0.0,

    -- Analysis metadata
    analyzer VARCHAR(50),
    confidence FLOAT,
    sentiment_label VARCHAR(20),

    -- Market impact
    price_change_1h FLOAT,
    price_change_24h FLOAT,
    volume_change FLOAT,

    -- Sentiment shift detection
    is_shift BOOLEAN DEFAULT FALSE,
    shift_magnitude FLOAT,
    previous_sentiment FLOAT,

    -- Timestamps
    analyzed_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE,

    -- Indexes
    CONSTRAINT sentiment_scores_ticker_id_idx FOREIGN KEY (ticker_id) REFERENCES tickers(id),
    CONSTRAINT sentiment_scores_news_article_id_idx FOREIGN KEY (news_article_id) REFERENCES news_articles(id)
);

CREATE INDEX IF NOT EXISTS idx_sentiment_scores_ticker_id ON sentiment_scores(ticker_id);
CREATE INDEX IF NOT EXISTS idx_sentiment_scores_symbol ON sentiment_scores(symbol);
CREATE INDEX IF NOT EXISTS idx_sentiment_scores_news_article_id ON sentiment_scores(news_article_id);
CREATE INDEX IF NOT EXISTS idx_sentiment_scores_sentiment_label ON sentiment_scores(sentiment_label);
CREATE INDEX IF NOT EXISTS idx_sentiment_scores_is_shift ON sentiment_scores(is_shift);
CREATE INDEX IF NOT EXISTS idx_sentiment_scores_analyzed_at ON sentiment_scores(analyzed_at);

-- Add comments for documentation
COMMENT ON TABLE news_articles IS 'News articles for sentiment analysis';
COMMENT ON TABLE sentiment_scores IS 'AI-powered sentiment analysis scores for news and market data';

COMMENT ON COLUMN news_articles.is_breaking IS 'Indicates if this is breaking/urgent news';
COMMENT ON COLUMN sentiment_scores.score IS 'Overall sentiment score from -1 (very negative) to 1 (very positive)';
COMMENT ON COLUMN sentiment_scores.analyzer IS 'Sentiment analyzer used: vader, finbert, or openai';
COMMENT ON COLUMN sentiment_scores.is_shift IS 'Indicates significant sentiment shift detected';
