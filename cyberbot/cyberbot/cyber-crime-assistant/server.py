from flask import Flask, request, jsonify
from flask_cors import CORS
from main import create_rag_chain

app = Flask(__name__)
# Allow requests from your React app's origin
CORS(app, resources={r"/ask": {"origins": "http://localhost:5173"}}) 

# Create the RAG chain when the server starts
print("Initializing RAG chain...")
rag_chain = create_rag_chain()
print("RAG chain ready.")

@app.route('/ask', methods=['POST'])
def ask_question():
    """
    API endpoint to receive a question and return the AI's answer.
    """
    data = request.get_json()
    query = data.get('query')

    if not query:
        return jsonify({'error': 'No query provided'}), 400

    try:
        print(f"Received query: {query}")
        # Invoke the RAG chain with the user's query
        response = rag_chain.invoke(query)
        print(f"Generated response: {response}")
        return jsonify({'response': response})

    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({'error': 'Failed to process the request'}), 500

if __name__ == '__main__':
    # Runs the Flask server
    app.run(host='0.0.0.0', port=5000, debug=True)