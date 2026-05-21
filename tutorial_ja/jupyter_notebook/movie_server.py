import sys
import os
from typing import Any                                                                                                                                                                  
from mcp.server.lowlevel import Server                                                                                                                                                  
from mcp.server.streamable_http_manager import StreamableHTTPSessionManager
from starlette.applications import Starlette                                                                                                                                            
from starlette.routing import Mount
from starlette.types import Receive, Scope, Send
import mcp.types as types
import json
import contextlib
import logging
from collections.abc import AsyncIterator
import uvicorn
from movie_db import MovieDB

logger = logging.getLogger(__name__)

DB_PATH = "data/movie.sqlite"


def main(db_path: str = DB_PATH):
  movie_db = MovieDB(db_path)
  mcp = Server("movie-db")

  @mcp.list_tools()
  async def handle_list_tools() -> list[types.Tool]:
      return [
          types.Tool(
      name="search_movies",                                                                                                                                                               
      description="Search movies by title and/or rating range. Results are sorted by rating descending. To get the top N highest rated movies, just set limit=N without any rating filters. Rating scale is 1.0 to 10.0. In this dataset, ratings range from 7.5 to 8.8.",
      inputSchema={
          "type": "object",
          "properties": {
              "title": {"type": "string", "description": "Partial or full movie title to search for"},
              "min_rating": {"type": "number", "description": "Minimum IMDB rating (1.0 to 10.0)"},
              "max_rating": {"type": "number", "description": "Maximum IMDB rating (1.0 to 10.0)"},
              "limit": {"type": "integer", "description": "Max results to return (default 20)"},
          },
      },
      ),
      ]

  @mcp.call_tool()
  async def handle_call_tool(name: str, args: dict[str, Any] | None):
      args = args or {}

      if name == "search_movies":
          return movie_db._search_movies(
              title=args.get("title"),
              min_rating=args.get("min_rating"),
              max_rating=args.get("max_rating"),
              limit=args.get("limit", 20),
          )
      else:
          return [types.TextContent(
              type="text",
              text=json.dumps({"error": f"Unknown tool: {name}"})
          )]

  session_manager = StreamableHTTPSessionManager(
      app=mcp,
      event_store=None,
      json_response=True,
      stateless=True,
  )

  async def handle_streamable_http(
      scope: Scope, receive: Receive, send: Send
  ) -> None:
      await session_manager.handle_request(scope, receive, send)

  @contextlib.asynccontextmanager
  async def lifespan(app: Starlette) -> AsyncIterator[None]:
      async with session_manager.run():
          logger.info("Movie DB MCP server started!")
          try:
              yield
          finally:
              logger.info("Movie DB MCP server shutting down...")

  starlette_app = Starlette(
      debug=True,
      routes=[
          Mount("/mcp", app=handle_streamable_http),
      ],
      lifespan=lifespan,
  )
  port = int(os.environ.get("MCP_PORT", "8000"))
  uvicorn.run(starlette_app, host="127.0.0.1", port=port)


if __name__ == "__main__":
  db_path = sys.argv[1] if len(sys.argv) > 1 else DB_PATH
  main(db_path)
