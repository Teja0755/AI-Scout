from langgraph.graph import StateGraph, END  
from typing import TypedDict, List

# ----- STATE -----
class ScoutState(TypedDict):
    # this is the shared dict that flows through every node
    # each agent reads from it and adds to it
    stories: List[str]      # raw story titles from HN
    summary: str            # LLM summary from news agent
    trends: str             # trend analysis (next agent)

# ----- NODES (agents) -----
from hn_agent import fetch_top_hn_stories, summarize_stories

def news_node(state: ScoutState) -> ScoutState:
    # receives state, does its job, returns updated state
    stories = fetch_top_hn_stories()
    titles = [s.get("title", "No title") for s in stories]
    summary = summarize_stories(stories)
    
    return {
        **state,            # keep everything already in state
        "stories": titles,  # add stories
        "summary": summary  # add summary
    }

from trend_agent import analyze_trends

def trend_node(state: ScoutState) -> ScoutState:
    trends = analyze_trends(state["summary"])
    return {
        **state,
        "trends": trends
    }

# ----- BUILD THE GRAPH -----
def build_graph():
    graph = StateGraph(ScoutState)       # create graph with our state shape
    
    graph.add_node("news", news_node)    # register news_node as "news"
    graph.add_node("trends", trend_node) # register trend_node as "trends"
    
    graph.set_entry_point("news")        # start here
    graph.add_edge("news", "trends")     # news → trends
    graph.add_edge("trends", END)        # trends → done
    
    return graph.compile()               # compile into a runnable graph

# ----- RUN IT -----
if __name__ == "__main__":
    graph = build_graph()
    
    result = graph.invoke({              # invoke = run the graph
        "stories": [],                   # initial empty state
        "summary": "",
        "trends": ""
    })
    
    print("=== STORIES ===")
    for s in result["stories"]:
        print(f"  - {s}")
    
    print("\n=== SUMMARY ===")
    print(result["summary"])
    
    print("\n=== TRENDS ===")
    print(result["trends"])