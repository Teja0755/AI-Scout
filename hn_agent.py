import httpx                   # HTTP client — like requests, but modern and async-ready
from groq import Groq          # Groq SDK to call our LLM
from dotenv import load_dotenv # reads .env file

load_dotenv()                  # loads GROQ_API_KEY into environment

client = Groq()                # creates our LLM connection

def fetch_top_hn_stories(limit=5):

    top_ids = httpx.get("https://hacker-news.firebaseio.com/v0/topstories.json").json()

    stories = []  # empty list to collect story details

    for story_id in top_ids[:limit]:  
   
        
        story = httpx.get(f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json").json()
        # for each ID, hit a different endpoint that returns the full story object
        # f"..." → f-string, injects story_id into the URL dynamically
        # story is now a dict: {title, url, score, author, ...}
        
        stories.append(story)  # add this story dict to our list

    return stories  # return the full list of 5 story dicts

def summarize_stories(stories):
    titles = "\n".join([f"- {s.get('title', 'No title')}" for s in stories])
  

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{
            "role": "user",
            "content": f"Summarize these HackerNews stories in 3 sentences:\n{titles}"
            # inject the titles string into the prompt
        }]
    )

    return response.choices[0].message.content  # return just the text

if __name__ == "__main__":

    print("Fetching HN stories...")
    stories = fetch_top_hn_stories()  # call our fetch function

    print("Stories fetched:")
    for s in stories:
        print(f"  - {s.get('title')}")  # print each title

    print("\nSummary:")
    print(summarize_stories(stories))  # call summarize, print result

