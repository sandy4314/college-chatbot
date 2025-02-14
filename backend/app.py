from flask import Flask, request, jsonify
from flask_cors import CORS  
from transformers import pipeline
from sentence_transformers import SentenceTransformer, util  
import re  

app = Flask(__name__)
CORS(app)  

# Load AI models
qa_pipeline = pipeline("question-answering", model="deepset/roberta-base-squad2")
embedding_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# Sample college information (long text)
context = """

Swayam NPTEL IIT Madras recognized the college with 'AAA' Grade for the third time (National Level-Sixth Rank in the Country and First Rank in the State). In the Times Engineering Institutes Ranking Survey 2023 conducted by Times of India,

Srilatha is the HOD of CSE. Kolla Srinivas is the Principal.
The college is ranked 36th in Top 125 Private Engineering Institutes.
Nagesh is the HOD of IOT.
CSE is the top branch in college.

"""

# Split context into sentences for better matching
sentences = [sent.strip() for sent in context.split(".") if sent.strip()]
sentence_embeddings = embedding_model.encode(sentences, convert_to_tensor=True)

# Function to extract roles dynamically
def extract_roles(text):
    role_pattern = r"([\w\s]+)\s+(is|was)\s+the\s+([\w\s]+)"
    matches = re.findall(role_pattern, text, re.IGNORECASE)
    return {match[2].strip().lower(): match[0].strip() for match in matches}

role_dict = extract_roles(context)

@app.route("/chat", methods=["POST"])
def chat():
    try:
        user_query = request.json.get("message", "").strip()

        if not user_query:
            return jsonify({"reply": "No message provided"}), 400

        # Step 1: Check if the query is asking about a known role
        for role, person in role_dict.items():
            if role.lower() in user_query.lower():
                return jsonify({"reply": f"{person} is the {role.capitalize()}."})

        # Step 2: Compute similarity with each sentence in the context
        query_embedding = embedding_model.encode(user_query, convert_to_tensor=True)
        similarity_scores = util.pytorch_cos_sim(query_embedding, sentence_embeddings)[0]
        
        # Find the most relevant sentence
        best_match_index = similarity_scores.argmax().item()
        best_match_score = similarity_scores[best_match_index].item()

        # If match is found, use QA model or return closest sentence
        if best_match_score >= 0.3:  
            best_sentence = sentences[best_match_index]

            # If the query is too short, return the sentence directly
            if len(user_query.split()) < 3:
                return jsonify({"reply": best_sentence})

            # Otherwise, use the QA model to extract the answer
            response = qa_pipeline(question=user_query, context=best_sentence)
            if response and "answer" in response and response["answer"].strip():
                return jsonify({"reply": response["answer"]})

        return jsonify({"reply": "Ask me about the college! or check your question once"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(port=5000, debug=True)
