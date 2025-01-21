#
# Humanoid: A simple, natural language interface for orchestrating autonomous agents.
# File: tooling.py
# Author: Aditya Patange (AdiPat)
# License: MIT License
# ⚡️ "Every instruction, flowing as energy, a fragment of space-time." — AdiPat
#

import os
import logging
import traceback
import enum
from crewai.tools import BaseTool
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

logger = logging.getLogger(__name__)


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


def get_tools_list() -> list[str]:
    """
    Retrieves a list of all tools in the system.
    """
    tools_list = ToolType.__members__.keys()
    return tools_list


def get_available_tools() -> dict:
    """
    Retrieves the list of available tools and initializes them.
    - Gets a list of all available tools.
    - Initializes each tool.
    - Returns a dictionary of all available tools.
    """
    all_tools = get_tools_list()
    tools = {}
    for tool in all_tools:
        try:
            tool = get_tool(tool_id=tool, args={})
            if tool:
                tools[tool] = tool
        except Exception as e:
            logger.error(f"Error while initializing tool {tool}: {str(e)}")
            logger.error(traceback.format_exc())
    return tools


def get_tool(tool_id: ToolType, args: dict) -> BaseTool:
    """
    Initializes a tool based on the specified tool ID.
    If the tool requires any arguments, they can be passed in the args dictionary.
    In the case of a missing argument, the tool will be initialized with default values.
    It is the callers responsibility to pass the correct arguments to the tool.
    If the tool requires an API key, it will be fetched from the environment variables.
    If the environment variable is missing, the tool will not be initialized and an error will be logged.
    """
    ## TODO: Create a tool config which can be passed to the LLM easily and has the necessary args for the tool to run
    if tool_id == ToolType.BROWSERBASE:
        browserbase_api_key = os.getenv("BROWSERBASE_API_KEY")
        browserbase_project_id = os.getenv("BROWSERBASE_PROJECT_ID")
        if not browserbase_api_key or not browserbase_project_id:
            logger.error(
                "Browserbase tool cannot be initialized: Missing API key or project ID."
            )
            return None
        return BrowserbaseLoadTool(
            api_key=browserbase_api_key, project_id=browserbase_project_id
        )
    elif tool_id == ToolType.CODEDOCS_SEARCH_TOOL:
        docs_url = args.get("docs_url")
        if not docs_url:
            return CodeDocsSearchTool()
        else:
            return CodeDocsSearchTool(docs_url=docs_url)
    elif tool_id == ToolType.CODE_INTERPRETER:
        # TODO: Figure out a way to inject tool-specific args into the crew config
        return (
            CodeInterpreterTool()
        )  # Set allow_code_execution=True on Agent initialization
    elif tool_id == ToolType.COMPOSIO_TOOL:
        composio_api_key = os.getenv("COMPOSIO_API_KEY")
        if not composio_api_key:
            logger.error("Composio tool cannot be initialized: Missing API key.")
            return None
        from_action = args.get("from_action")
        from_app = args.get("from_app")
        if not from_action and not from_app:
            logger.error(
                "Composio tool cannot be initialized: Missing from_action or from_app."
            )
            return None
        if from_action:
            action = args.get("action")
            if action:
                return ComposioTool.from_action(action=action)
        if from_app:
            app = args.get("app")
            if not app:
                logger.error("Composio tool cannot be initialized: Missing app.")
                return None
            tags = args.get("tags")
            use_case = args.get("use_case")
            if not tags and not use_case:
                logger.error(
                    "Composio tool cannot be initialized: Missing tags or use_case."
                )
                return None
            if tags:
                return ComposioTool.from_app(app, tags=tags)
            if use_case:
                return ComposioTool.from_app(app, use_case=use_case)
        return None
    elif tool_id == ToolType.CSV_SEARCH_TOOL:
        csv = args.get("csv")
        if csv:
            return CSVSearchTool(csv=csv)
        return CSVSearchTool()
    elif tool_id == ToolType.DALLE_TOOL:
        model = args.get("model")
        size = args.get("size")
        quality = args.get("quality")
        n = args.get("n")
        args = {}
        if model:
            args["model"] = model
        if size:
            args["size"] = size
        if quality:
            args["quality"] = quality
        if n:
            args["n"] = n
        return DallETool(**args)
    elif tool_id == ToolType.DIRECTORY_SEARCH_TOOL:
        directory = args.get("directory")
        if directory:
            return DirectorySearchTool(directory=directory)
        return DirectorySearchTool()
    elif tool_id == ToolType.DIRECTORY_READ_TOOL:
        directory = args.get("directory")
        if directory:
            return DirectoryReadTool(directory=directory)
        return DirectoryReadTool()
    elif tool_id == ToolType.DOCX_SEARCH_TOOL:
        docx = args.get("docx")
        if docx:
            return DOCXSearchTool(docx=docx)
        return DOCXSearchTool()
    elif tool_id == ToolType.EXA_SEARCH_TOOL:
        exa_api_key = os.getenv("EXA_API_KEY")
        if not exa_api_key:
            logger.error("EXA tool cannot be initialized: Missing API key.")
            return None
        return EXASearchTool()
    elif tool_id == ToolType.FILE_READ_TOOL:
        file_path = args.get("file_path")
        if file_path:
            return FileReadTool(file_path=file_path)
        return FileReadTool()
    elif tool_id == ToolType.FILE_WRITER_TOOL:
        return FileWriterTool()
    elif tool_id == ToolType.FIRECRAWL_CRAWL_WEBSITE_TOOL:
        firecrawl_api_key = os.getenv("FIRECRAWL_API_KEY")
        url = args.get("url")
        if not firecrawl_api_key:
            logger.error(
                "Firecrawl Crawl Website tool cannot be initialized: Missing API key."
            )
            return None
        if url:
            return FirecrawlCrawlWebsiteTool(api_key=firecrawl_api_key, url=url)
        return FirecrawlCrawlWebsiteTool(
            api_key=firecrawl_api_key, url="https://www.google.com"
        )
    elif tool_id == ToolType.FIRECRAWL_SCRAPE_WEBSITE_TOOL:
        firecrawl_api_key = os.getenv("FIRECRAWL_API_KEY")
        url = args.get("url")
        if not firecrawl_api_key:
            logger.error(
                "Firecrawl Scrape Website tool cannot be initialized: Missing API key."
            )
            return None
        if url:
            return FirecrawlScrapeWebsiteTool(api_key=firecrawl_api_key, url=url)
        return FirecrawlScrapeWebsiteTool(
            api_key=firecrawl_api_key, url="https://www.google.com"
        )
    elif tool_id == ToolType.FIRECRAWL_SEARCH_TOOL:
        firecrawl_api_key = os.getenv("FIRECRAWL_API_KEY")
        if not firecrawl_api_key:
            logger.error(
                "Firecrawl Search tool cannot be initialized: Missing API key."
            )
            return None
        query = args.get("query")
        if query:
            return FirecrawlSearchTool(api_key=firecrawl_api_key, query=query)
        return FirecrawlSearchTool(api_key=firecrawl_api_key)
    elif tool_id == ToolType.GITHUB_SEARCH_TOOL:
        gh_token = os.getenv("GITHUB_TOKEN")
        if not gh_token:
            gh_token = args.get("gh_token")
        if not gh_token:
            logger.error(
                "Github Search tool cannot be initialized: Missing GitHub token."
            )
            return None
        github_repo = args.get("github_repo")
        content_types = args.get("content_types") or ["code"]  # type: list[str]
        return GithubSearchTool(
            gh_token=gh_token, github_repo=github_repo, content_types=content_types
        )
    elif tool_id == ToolType.SERPER_DEV_TOOL:
        serper_api_key = os.getenv("SERPER_API_KEY")
        if not serper_api_key:
            logger.error("Serper Dev tool cannot be initialized: Missing API key.")
            return None
        tool_args = {}
        fields = ["search_url", "country", "location", "locale", "n_results"]
        tool_args = {}
        for field in fields:
            arg_val = args.get(field)
            if arg_val:
                tool_args[field] = arg_val
        return SerperDevTool(**tool_args)
    elif tool_id == ToolType.JSON_SEARCH_TOOL:
        json_path = args.get("json_path")
        if json_path:
            return JSONSearchTool(json_path=json_path)
        return JSONSearchTool()
    elif tool_id == ToolType.MDX_SEARCH_TOOL:
        mdx = args.get("mdx")
        if mdx:
            return MDXSearchTool(mdx=mdx)
        return MDXSearchTool()
    elif tool_id == ToolType.MYSQL_SEARCH_TOOL:
        db_uri = args.get("db_uri")
        table_name = args.get("table_name")
        if not db_uri or not table_name:
            logger.error(
                "MySQL Search tool cannot be initialized: Missing DB URI or table name."
            )
            return None
        return MySQLSearchTool(db_uri=db_uri, table_name=table_name)
    elif tool_id == ToolType.NL2SQL_TOOL:
        db_uri = args.get("db_uri")
        if not db_uri:
            logger.error("NL2SQL tool cannot be initialized: Missing DB URI.")
            return None
        return NL2SQLTool(db_uri=db_uri)
    elif tool_id == ToolType.PDF_SEARCH_TOOL:
        pdf = args.get("pdf")
        if pdf:
            return PDFSearchTool(pdf=pdf)
        return PDFSearchTool()
    elif tool_id == ToolType.PG_SEARCH_TOOL:
        db_uri = args.get("db_uri")
        table_name = args.get("table_name")
        if not db_uri or not table_name:
            logger.error(
                "PG Search tool cannot be initialized: Missing DB URI or table name."
            )
            return None
        return PGSearchTool(db_uri=db_uri, table_name=table_name)
    elif tool_id == ToolType.SCRAPE_WEBSITE_TOOL:
        website_url = args.get("website_url")
        if website_url:
            return ScrapeWebsiteTool(website_url=website_url)
        return ScrapeWebsiteTool()
    elif tool_id == ToolType.SELENIUM_SCRAPING_TOOL:
        fields = ["website_url", "css_element", "cookie", "wait_time"]
        tool_args = {}
        for field in fields:
            arg_val = args.get(field)
            if arg_val:
                tool_args[field] = arg_val
        return SeleniumScrapingTool(**tool_args)
    elif tool_id == ToolType.SPIDER_TOOL:
        spider_api_key = os.getenv("SPIDER_API_KEY")
        if not spider_api_key:
            logger.error("Spider tool cannot be initialized: Missing API key.")
            return None
        fields = [
            "params",
            "request",
            "limit",
            "depth",
            "cache",
            "budget",
            "locale",
            "cookies",
            "stealth",
            "headers",
            "metadata",
            "viewport",
            "encoding",
            "subdomains",
            "user_agent",
            "store_data",
            "gpt_config",
            "fingerprint",
            "storageless",
            "readability",
            "return_format",
            "proxy_enabled",
            "query_selector",
            "full_resources",
            "request_timeout",
            "run_in_background",
        ]
        tool_args = {}
        for field in fields:
            arg_val = args.get(field)
            if arg_val:
                if field in ["limit", "depth", "request_timeout"]:
                    tool_args[field] = int(arg_val)
                elif field in [
                    "cache",
                    "stealth",
                    "metadata",
                    "subdomains",
                    "store_data",
                    "fingerprint",
                    "storageless",
                    "readability",
                    "proxy_enabled",
                    "full_resources",
                    "run_in_background",
                ]:
                    tool_args[field] = bool(arg_val)
                else:
                    tool_args[field] = arg_val
        return SpiderTool(api_key=spider_api_key, **tool_args)
    elif tool_id == ToolType.TXT_SEARCH_TOOL:
        txt = args.get("txt")
        if txt:
            return TXTSearchTool(txt=txt)
        return TXTSearchTool()
    elif tool_id == ToolType.VISION_TOOL:
        image_path_url = args.get("image_path_url")
        if image_path_url:
            return VisionTool(image_path_url=image_path_url)
        return VisionTool()
    elif tool_id == ToolType.WEBSITE_SEARCH_TOOL:
        website = args.get("website")
        if website:
            return WebsiteSearchTool(website=website)
        return WebsiteSearchTool()
    elif tool_id == ToolType.XML_SEARCH_TOOL:
        xml = args.get("xml")
        if xml:
            return XMLSearchTool(xml=xml)
        return XMLSearchTool()
    elif tool_id == ToolType.YOUTUBE_CHANNEL_SEARCH_TOOL:
        youtube_channel_handle = args.get("youtube_channel_handle")
        if youtube_channel_handle:
            return YoutubeChannelSearchTool(
                youtube_channel_handle=youtube_channel_handle
            )
        return YoutubeChannelSearchTool()
    elif tool_id == ToolType.YOUTUBE_VIDEO_SEARCH_TOOL:
        youtube_video_url = args.get("youtube_video_url")
        if youtube_video_url:
            return YoutubeVideoSearchTool(youtube_video_url=youtube_video_url)
        return YoutubeVideoSearchTool()
    ## Nothing matched
    logger.error(f"Tool ID {tool_id} not found.")
    logger.error(f"Supported Tool IDs: {ToolType.__members__}")
    return None
