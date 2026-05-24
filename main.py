from fastapi import FastAPI      # FastAPI class — this IS your web application
from news_agent import fetch_top_hn_stories, summarize_stories  
from agent_graph import build_graph

# import the two functions we just built — reusing them as-is

app = FastAPI()                  # create your FastAPI app instance

@app.get("/news")                # decorator — tells FastAPI: when someone hits GET /news, run this function
def get_news():
    stories = fetch_top_hn_stories()        # fetch from HN
    summary = summarize_stories(stories)    # summarize with LLM
    
    return {                      # FastAPI auto-converts this dict to JSON response
        "stories": [s.get("title") for s in stories],  # list of titles
        "summary": summary                              # LLM summary
    }

@app.get("/briefing")                    # new endpoint
def get_briefing():
    graph = build_graph()                # build the graph
    result = graph.invoke({              # run it with empty initial state
        "stories": [],
        "summary": "",
        "trends": ""
    })
    return result                        # return the full final state as JSON