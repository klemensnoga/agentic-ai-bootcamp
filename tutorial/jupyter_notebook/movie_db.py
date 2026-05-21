import sqlite3
import json                                                                                                                                                                             
from typing import List
from pathlib import Path                                                                                                                                                                
import mcp.types as types

DB_PATH = "data/movie.sqlite"

class MovieDB:
  def __init__(self, db_path):
      self.db_path = str(Path().resolve().joinpath(db_path))

  def _search_movies(
      self,
      title: str | None,
      min_rating: float | None,
      max_rating: float | None,
      limit: int = 20,
  ) -> List[types.TextContent]:
      """Search movies in the IMDB table by title and/or rating range.

      Args:
          title: Partial or full movie title to search for.
          min_rating: Minimum IMDB rating.
          max_rating: Maximum IMDB rating.
          limit: Max number of results to return.
      """

      conn = sqlite3.connect(self.db_path)
      cursor = conn.cursor()

      query = """
          SELECT Movie_id, Title, Rating, TotalVotes, Budget, Runtime
          FROM IMDB
      """
      params = []
      conditions = []

      if title is not None:
          conditions.append("Title LIKE ?")
          params.append(f"%{title}%")

      if min_rating is not None:
          conditions.append("Rating >= ?")
          params.append(min_rating)

      if max_rating is not None:
          conditions.append("Rating <= ?")
          params.append(max_rating)

      if conditions:
          query += " WHERE " + " AND ".join(conditions)

      query += " ORDER BY Rating DESC LIMIT ?"
      params.append(limit)

      try:
          cursor.execute(query, params)
          results = cursor.fetchall()

          output = []
          for row in results:
              output.append(
                  {
                      "movie_id": row[0],
                      "title": row[1],
                      "rating": row[2],
                      "total_votes": row[3],
                      "budget": row[4],
                      "runtime": row[5],
                  }
              )

      except sqlite3.Error as e:
          conn.close()
          raise e

      finally:
          conn.close()

      return [types.TextContent(
          type="text",
          text=json.dumps(output)
      )]
