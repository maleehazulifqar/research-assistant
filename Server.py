from flask import Flask, request, jsonify, send_from_directory
from embedder import create_vectorstore, save_vectorstore, load_vectorstore
from retriever import create_rag_chain
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)

chain = None
uploaded_files = []

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/upload', methods=['POST'])
def upload():
    global chain, uploaded_files

    print("Files received:", request.files)
    files = request.files.getlist('pdfs')
    print("PDF list:", files)

    # Empty file check
    valid_files = [f for f in files if f and f.filename != '']
    if not valid_files:
        return jsonify({'error': 'No files received'}), 400

    saved_paths = []
    file_names = []

    for file in valid_files:
        temp_path = f"temp_{file.filename}"
        file.save(temp_path)
        saved_paths.append(temp_path)
        file_names.append(file.filename)
        print(f"Saved: {temp_path}")

    try:
        vs = create_vectorstore(saved_paths)
        save_vectorstore(vs)
        chain = create_rag_chain(vs)
        uploaded_files = file_names
    except Exception as e:
        print("Error during processing:", e)
        return jsonify({'error': str(e)}), 500
    finally:
        for path in saved_paths:
            if os.path.exists(path):
                os.remove(path)

    return jsonify({
        'status': 'ready',
        'files': file_names,
        'count': len(file_names)
    })

@app.route('/ask', methods=['POST'])
def ask():
    global chain
    if not chain:
        return jsonify({'answer': 'Please upload and process a PDF first.'})

    data = request.json
    question = data.get('question', '')
    history = data.get('history', [])

    if not question:
        return jsonify({'answer': 'Please ask a question.'})

    history_text = ""
    if history:
        for msg in history[-4:]:
            history_text += f"User: {msg['user']}\nAssistant: {msg['assistant']}\n"

    full_question = f"{history_text}User: {question}" if history_text else question
    answer = chain.invoke(full_question)

    return jsonify({'answer': answer})

@app.route('/files', methods=['GET'])
def get_files():
    return jsonify({'files': uploaded_files})

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='127.0.0.1')