from typing import Annotated
from typing_extensions import TypedDict                                                                                                                                                 
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages

from nat.builder.framework_enum import LLMFrameworkEnum
from nat.builder.sync_builder import SyncBuilder

chat_llm = SyncBuilder.current().get_llm("nim_llm", wrapper_type=LLMFrameworkEnum.LANGCHAIN)
movie_agent = SyncBuilder.current().get_function("movie_agent")


class ConversationState(TypedDict):
  messages: Annotated[list, add_messages]


def classify_node(state: ConversationState):
  response = chat_llm.invoke([
      {"role": "system", "content": (
          "You are an intent classifier for a movie database assistant. "
          "The database contains IMDB movie data: titles, ratings, votes, budgets, and runtimes. "
          "Classify the user's question as either 'in_domain' or 'out_of_domain'. "
          "Reply with ONLY one word.\n\n"
          "in_domain: questions about movies, ratings, top movies, searching movies by title, "
          "comparing movie ratings, budgets, runtimes.\n\n"
          "out_of_domain: anything unrelated to movies."
      )},
      *state["messages"]
  ])
  raw = response.content.strip().lower()
  return {"messages": [{"role": "assistant", "content": raw}]}


def route_intent(state: ConversationState):
  last = state["messages"][-1].content.strip().lower()
  if last == "in_domain":
      return "movie_agent"
  return "reject"


async def movie_agent_node(state: ConversationState):
  user_query = state["messages"][0].content
  result = await movie_agent.ainvoke(user_query)
  return {"messages": [{"role": "assistant", "content": str(result)}]}


def reject_node(state: ConversationState):
  return {"messages": [{"role": "assistant", "content": "Sorry, I can only help with movie-related questions."}]}


graph = StateGraph(ConversationState)
graph.add_node("classify", classify_node)
graph.add_node("movie_agent", movie_agent_node)
graph.add_node("reject", reject_node)

graph.add_edge(START, "classify")
graph.add_conditional_edges("classify", route_intent, {"movie_agent": "movie_agent", "reject": "reject"})
graph.add_edge("movie_agent", END)
graph.add_edge("reject", END)

intent_graph = graph.compile()
