import enum
from crewai_tools import (
    BrowserbaseLoadTool,
    CodeDocsSearchTool,
    CodeInterpreterTool,
    ComposioTool,
    CSVSearchTool,
    DallETool,
    DirectorySearchTool,
    DirectoryReadTool,
    DOCXSearchTool,
    EXASearchTool,
    FileReadTool,
    FileWriterTool,
    FirecrawlCrawlWebsiteTool,
    FirecrawlScrapeWebsiteTool,
    FirecrawlSearchTool,
    GithubSearchTool,
    SerperDevTool,
    JSONSearchTool,
    MDXSearchTool,
    MySQLSearchTool,
    NL2SQLTool,
    PDFSearchTool,
    PGSearchTool,
    ScrapeWebsiteTool,
    SeleniumScrapingTool,
    SpiderTool,
    TXTSearchTool,
    VisionTool,
    WebsiteSearchTool,
    XMLSearchTool,
    YoutubeChannelSearchTool,
    YoutubeVideoSearchTool,
)


class ToolType(str, enum.Enum):
    """Type of tool."""

    BROWSERBASE = "browserbase"
    CODEDOCS_SEARCH_TOOL = "codedocs_search_tool"
    CODE_INTERPRETER = "code_interpreter"
    COMPOSIO_TOOL = "composio_tool"
    CSV_SEARCH_TOOL = "csv_search_tool"
    DALLE_TOOL = "dalle_tool"
    DIRECTORY_SEARCH_TOOL = "directory_search_tool"
    DIRECTORY_READ_TOOL = "directory_read_tool"
    DOCX_SEARCH_TOOL = "docx_search_tool"
    EXA_SEARCH_TOOL = "exa_search_tool"
    FILE_READ_TOOL = "file_read_tool"
    FILE_WRITER_TOOL = "file_writer_tool"
    FIRECRAWL_CRAWL_WEBSITE_TOOL = "firecrawl_crawl_website_tool"
    FIRECRAWL_SCRAPE_WEBSITE_TOOL = "firecrawl_scrape_website_tool"
    FIRECRAWL_SEARCH_TOOL = "firecrawl_search_tool"
    GITHUB_SEARCH_TOOL = "github_search_tool"
    SERPER_DEV_TOOL = "serper_dev_tool"
    JSON_SEARCH_TOOL = "json_search_tool"
    MDX_SEARCH_TOOL = "mdx_search_tool"
    MYSQL_SEARCH_TOOL = "mysql_search_tool"
    NL2SQL_TOOL = "nl2sql_tool"
    PDF_SEARCH_TOOL = "pdf_search_tool"
    PG_SEARCH_TOOL = "pg_search_tool"
    SCRAPE_WEBSITE_TOOL = "scrape_website_tool"
    SELENIUM_SCRAPING_TOOL = "selenium_scraping_tool"
    SPIDER_TOOL = "spider_tool"
    TXT_SEARCH_TOOL = "txt_search_tool"
    VISION_TOOL = "vision_tool"
    WEBSITE_SEARCH_TOOL = "website_search_tool"
    XML_SEARCH_TOOL = "xml_search_tool"
    YOUTUBE_CHANNEL_SEARCH_TOOL = "youtube_channel_search_tool"
    YOUTUBE_VIDEO_SEARCH_TOOL = "youtube_video_search_tool"


TOOL_CONFIG = {
    ToolType.BROWSERBASE: {
        "class": BrowserbaseLoadTool,
        "env_vars": ["BROWSERBASE_API_KEY", "BROWSERBASE_PROJECT_ID"],
        "args": {},
    },
    ToolType.CODEDOCS_SEARCH_TOOL: {
        "class": CodeDocsSearchTool,
        "env_vars": [],
        "args": {"docs_url": str},
    },
    ToolType.CODE_INTERPRETER: {
        "class": CodeInterpreterTool,
        "env_vars": [],
        "args": {},
    },
    ToolType.COMPOSIO_TOOL: {
        "class": ComposioTool,
        "env_vars": ["COMPOSIO_API_KEY"],
        "args": {
            "from_action": str,
            "from_app": str,
            "action": str,
            "app": str,
            "tags": list,
            "use_case": str,
        },
    },
    ToolType.CSV_SEARCH_TOOL: {
        "class": CSVSearchTool,
        "env_vars": [],
        "args": {"csv": str},
    },
    ToolType.DALLE_TOOL: {
        "class": DallETool,
        "env_vars": [],
        "args": {"model": str, "size": str, "quality": str, "n": int},
    },
    ToolType.DIRECTORY_SEARCH_TOOL: {
        "class": DirectorySearchTool,
        "env_vars": [],
        "args": {"directory": str},
    },
    ToolType.DIRECTORY_READ_TOOL: {
        "class": DirectoryReadTool,
        "env_vars": [],
        "args": {"directory": str},
    },
    ToolType.DOCX_SEARCH_TOOL: {
        "class": DOCXSearchTool,
        "env_vars": [],
        "args": {"docx": str},
    },
    ToolType.EXA_SEARCH_TOOL: {
        "class": EXASearchTool,
        "env_vars": ["EXA_API_KEY"],
        "args": {},
    },
    ToolType.FILE_READ_TOOL: {
        "class": FileReadTool,
        "env_vars": [],
        "args": {"file_path": str},
    },
    ToolType.FILE_WRITER_TOOL: {"class": FileWriterTool, "env_vars": [], "args": {}},
    ToolType.FIRECRAWL_CRAWL_WEBSITE_TOOL: {
        "class": FirecrawlCrawlWebsiteTool,
        "env_vars": ["FIRECRAWL_API_KEY"],
        "args": {"url": str},
    },
    ToolType.FIRECRAWL_SCRAPE_WEBSITE_TOOL: {
        "class": FirecrawlScrapeWebsiteTool,
        "env_vars": ["FIRECRAWL_API_KEY"],
        "args": {"url": str},
    },
    ToolType.FIRECRAWL_SEARCH_TOOL: {
        "class": FirecrawlSearchTool,
        "env_vars": ["FIRECRAWL_API_KEY"],
        "args": {"query": str},
    },
    ToolType.GITHUB_SEARCH_TOOL: {
        "class": GithubSearchTool,
        "env_vars": ["GITHUB_TOKEN"],
        "args": {"gh_token": str, "github_repo": str, "content_types": list},
    },
    ToolType.SERPER_DEV_TOOL: {
        "class": SerperDevTool,
        "env_vars": ["SERPER_API_KEY"],
        "args": {
            "search_url": str,
            "country": str,
            "location": str,
            "locale": str,
            "n_results": int,
        },
    },
    ToolType.JSON_SEARCH_TOOL: {
        "class": JSONSearchTool,
        "env_vars": [],
        "args": {"json_path": str},
    },
    ToolType.MDX_SEARCH_TOOL: {
        "class": MDXSearchTool,
        "env_vars": [],
        "args": {"mdx": str},
    },
    ToolType.MYSQL_SEARCH_TOOL: {
        "class": MySQLSearchTool,
        "env_vars": [],
        "args": {"db_uri": str, "table_name": str},
    },
    ToolType.NL2SQL_TOOL: {
        "class": NL2SQLTool,
        "env_vars": [],
        "args": {"db_uri": str},
    },
    ToolType.PDF_SEARCH_TOOL: {
        "class": PDFSearchTool,
        "env_vars": [],
        "args": {"pdf": str},
    },
    ToolType.PG_SEARCH_TOOL: {
        "class": PGSearchTool,
        "env_vars": [],
        "args": {"db_uri": str, "table_name": str},
    },
    ToolType.SCRAPE_WEBSITE_TOOL: {
        "class": ScrapeWebsiteTool,
        "env_vars": [],
        "args": {"website_url": str},
    },
    ToolType.SELENIUM_SCRAPING_TOOL: {
        "class": SeleniumScrapingTool,
        "env_vars": [],
        "args": {
            "website_url": str,
            "css_element": str,
            "cookie": str,
            "wait_time": int,
        },
    },
    ToolType.SPIDER_TOOL: {
        "class": SpiderTool,
        "env_vars": ["SPIDER_API_KEY"],
        "args": {
            "params": dict,
            "request": dict,
            "limit": int,
            "depth": int,
            "cache": bool,
            "budget": int,
            "locale": str,
            "cookies": dict,
            "stealth": bool,
            "headers": dict,
            "metadata": bool,
            "viewport": str,
            "encoding": str,
            "subdomains": bool,
            "user_agent": str,
            "store_data": bool,
            "gpt_config": dict,
            "fingerprint": bool,
            "storageless": bool,
            "readability": bool,
            "return_format": str,
            "proxy_enabled": bool,
            "query_selector": str,
            "full_resources": bool,
            "request_timeout": int,
            "run_in_background": bool,
        },
    },
    ToolType.TXT_SEARCH_TOOL: {
        "class": TXTSearchTool,
        "env_vars": [],
        "args": {"txt": str},
    },
    ToolType.VISION_TOOL: {
        "class": VisionTool,
        "env_vars": [],
        "args": {"image_path_url": str},
    },
    ToolType.WEBSITE_SEARCH_TOOL: {
        "class": WebsiteSearchTool,
        "env_vars": [],
        "args": {"website": str},
    },
    ToolType.XML_SEARCH_TOOL: {
        "class": XMLSearchTool,
        "env_vars": [],
        "args": {"xml": str},
    },
    ToolType.YOUTUBE_CHANNEL_SEARCH_TOOL: {
        "class": YoutubeChannelSearchTool,
        "env_vars": [],
        "args": {"youtube_channel_handle": str},
    },
    ToolType.YOUTUBE_VIDEO_SEARCH_TOOL: {
        "class": YoutubeVideoSearchTool,
        "env_vars": [],
        "args": {"youtube_video_url": str},
    },
}
