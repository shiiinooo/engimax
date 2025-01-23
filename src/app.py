import streamlit as st
from search_engine import SearchEngine
from workflow import graph, State
from langchain_core.messages import HumanMessage

def main():
    st.title("Product Search Engine")
    st.write("Search for products with AI-powered recommendations.")

    # Initialize session state if needed
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Query Input
    query = st.text_input("Enter your search query:")
    
    if query:
        # Configure graph execution
        config = {"configurable": {"thread_id": "1"}}
        
        # Create initial state with user query
        initial_state = {
            "messages": [HumanMessage(content=query)],
            "search_results": []
        }
        
        # Create containers for results
        search_results_container = st.empty()        
        # Execute graph
        final_results = None
        
        # Process results
        for event in graph.stream(initial_state, config, stream_mode="values"):
            if "search_results" in event:
                final_results = event["search_results"]
                results_text = "### Search Results:\n"
                for result in final_results:
                    if result.get('is_external', False):
                        results_text += f"""
<div style='padding: 10px; margin: 10px 0; border-radius: 5px; background-color: #1E1E1E;'>

**Title:** {result['name']}  
**Source:** [{result['source']}]({result['source']})  
**Description:** {result['description']}

</div>
"""
                    else:
                        results_text += f"""
<div style='padding: 10px; margin: 10px 0; border-radius: 5px; background-color: #1E1E1E;'>

**Name:** {result['name']}  
**Price:** ${result['price']}  
**Description:** {result['description']}

</div>
"""
                search_results_container.markdown(results_text, unsafe_allow_html=True)
                
            
    
if __name__ == "__main__":
    main()
