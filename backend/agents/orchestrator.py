from backend.agents.qa_agent import qa_agent
from backend.agents.research_agent import research_agent
from backend.agents.test_agent import test_agent

def route_query(query: str):

    q = query.lower()

    if any(keyword in q for keyword in 
           ["test case", "test cases", "testing", "scenario", "qa"]):
        return {
            "response": test_agent(query),
            "agent": "test",
            "sources": []
        }

    elif any(keyword in q for keyword in 
        ["research", "report", "analysis", "explain in detail", "study"]):
        return {
            "response": research_agent(query),
            "agent": "research",
            "sources": []
        }

    else:
        result = qa_agent(query)

        return {
            "response": result["response"],
            "agent": "qa",
            "sources": result["sources"]
        }
    
if __name__ == "__main__": 
    query = "What is technology?"
    result = route_query(query)
    print(result)
