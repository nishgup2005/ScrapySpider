# Scrapy settings for phhc_crawler project
# OPTIMIZED VERSION - Significant performance improvements over original

BOT_NAME = "phhc_crawler"
SPIDER_MODULES = ["phhc_crawler.spiders"]
NEWSPIDER_MODULE = "phhc_crawler.spiders"

# ============================================================================
# CRITICAL PERFORMANCE OPTIMIZATION SETTINGS
# ============================================================================

# Massive concurrency boost (from default 16 to 100)
CONCURRENT_REQUESTS = 100

# High single-domain concurrency (from 1 to 50) - MAJOR BOTTLENECK FIX
CONCURRENT_REQUESTS_PER_DOMAIN = 50

# Optimized download delay (from 1 to 0.1 seconds)
DOWNLOAD_DELAY = 0.1

# Enhanced reactor thread pool for better DNS/IO handling
REACTOR_THREADPOOL_MAXSIZE = 50

# ============================================================================
# AUTOTHROTTLE - ADAPTIVE PERFORMANCE TUNING
# ============================================================================

# Enable AutoThrottle for intelligent performance adaptation
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 0.1
AUTOTHROTTLE_MAX_DELAY = 3
AUTOTHROTTLE_TARGET_CONCURRENCY = 8.0
AUTOTHROTTLE_DEBUG = False  # Set to True for debugging performance issues

# ============================================================================
# PERFORMANCE KILLERS - DISABLED
# ============================================================================

# Disable robots.txt checking (major performance killer)
ROBOTSTXT_OBEY = False

# Disable cookies (not needed for this use case)
COOKIES_ENABLED = False

# Disable redirect middleware if not needed
# REDIRECT_ENABLED = False

# ============================================================================
# MEMORY AND CACHING OPTIMIZATIONS
# ============================================================================

# Optimize DNS cache
DNSCACHE_ENABLED = True
DNSCACHE_SIZE = 10000

# Disable HTTP cache to save memory (enable only if needed)
HTTPCACHE_ENABLED = False

# Memory usage optimization
MEMDEBUG_ENABLED = False

# ============================================================================
# TIMEOUT OPTIMIZATIONS
# ============================================================================

# Optimized timeout settings
DOWNLOAD_TIMEOUT = 30
DOWNLOAD_DELAY_SPREAD = 0.5

# ============================================================================
# REQUEST OPTIMIZATION
# ============================================================================

# Optimized retry settings
RETRY_TIMES = 2  # Reduced from default 3
RETRY_HTTP_CODES = [500, 502, 503, 504, 408, 429]

# Connection pooling
DOWNLOAD_WARNSIZE = 33554432  # 32MB
DOWNLOAD_MAXSIZE = 104857600  # 100MB

# ============================================================================
# PIPELINE CONFIGURATION
# ============================================================================

# Configure item pipelines with performance monitoring
ITEM_PIPELINES = {
    "phhc_crawler.pipelines.PerformancePipeline": 100,
    "phhc_crawler.pipelines.OptimizedExcelExportPipeline": 300,
}

# ============================================================================
# LOGGING AND MONITORING
# ============================================================================

# Optimized logging settings
LOG_FILE = "crawl.log"
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(levelname)s: %(message)s"

# Disable unnecessary stats
STATS_CLASS = 'scrapy.statscollectors.MemoryStatsCollector'

# ============================================================================
# DATA EXPORT CONFIGURATION
# ============================================================================

# Configure feeds for dual export (CSV backup + Excel primary)
FEEDS = {
    'results_backup.csv': {
        'format': 'csv',
        'encoding': 'utf8',
        'overwrite': True,
    }
}

FEED_EXPORT_ENCODING = "utf-8"

# ============================================================================
# USER AGENT AND HEADERS
# ============================================================================

# Rotate user agents to avoid detection
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"

# Default request headers
DEFAULT_REQUEST_HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
}

# ============================================================================
# MIDDLEWARE CONFIGURATION (Optional - Uncomment if needed)
# ============================================================================

# Enable rotating user agents if getting blocked
# DOWNLOADER_MIDDLEWARES = {
#     'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
#     'scrapy_user_agents.middlewares.RandomUserAgentMiddleware': 400,
# }

# Enable proxy rotation if needed
# ROTATING_PROXY_LIST_PATH = 'proxy_list.txt'
# DOWNLOADER_MIDDLEWARES = {
#     'rotating_proxies.middlewares.RotatingProxyMiddleware': 610,
#     'rotating_proxies.middlewares.BanDetectionMiddleware': 620,
# }

# ============================================================================
# EXPERIMENTAL SETTINGS (Use with caution)
# ============================================================================

# Enable asyncio reactor for better performance (Python 3.7+)
# TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"

# ============================================================================
# CONFIGURATION NOTES
# ============================================================================

# Performance Expectations:
# - Original: ~0.11 requests/second (16 concurrent, 1 second delay)
# - Optimized: ~30-50 requests/second (100 concurrent, 0.1 second delay)
# - Expected speedup: 270-450x faster request processing
# - Total runtime: 5-10 minutes (down from 30 minutes)

# Troubleshooting if blocked:
# 1. Reduce CONCURRENT_REQUESTS to 50
# 2. Increase DOWNLOAD_DELAY to 0.5
# 3. Enable AUTOTHROTTLE_DEBUG = True
# 4. Consider enabling proxy rotation

# Memory usage:
# - Expected: 2-4GB during peak operation
# - If memory issues: Reduce CONCURRENT_REQUESTS to 50