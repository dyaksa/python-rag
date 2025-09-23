from flask import Blueprint, request, jsonify
from app.usecases import ingest_pdf_stream, query_knn

bp = Blueprint('ingest', __name__)

@bp.route("/ask", methods=["POST"])
def ask():
    ask_query = request.json.get("ask")
    if not ask_query:
        return jsonify({"error": "Missing query parameter"}), 400
    try:
        rag_chain = query_knn(ask_query)
        answer = rag_chain.invoke({"question": ask_query})
        return jsonify({"answer": answer}), 200
    except Exception as e:
        return jsonify({"error": "Failed to process query", "detail": str(e)}), 500
    

@bp.route('/upload', methods=['POST'])
def ingest():
    if 'file' not in request.files:
        return jsonify({"error": "Missing form field 'file'"}), 400

    f = request.files.get('file')
    if not f or f.filename == '':
        return jsonify({"error": "No file provided or empty filename"}), 400

    try:
        max_tokens = int(request.form.get('max_tokens', 500))
        overlap_tokens = int(request.form.get('overlap_tokens', 50))
    except ValueError:
        return jsonify({"error": "max_tokens and overlap_tokens must be integers"}), 400
    
    # Basic content-type hint (optional)
    if f.mimetype not in ("application/pdf", "application/octet-stream"):
        # Not rejecting strictly, just warning inside response
        content_type_note = f"Unexpected mimetype {f.mimetype}; proceeding"
    else:
        content_type_note = None

    try:
        resp = ingest_pdf_stream(
            stream=f.stream,
            source=request.form.get('source') or (f.filename or "document.pdf"),
            max_tokens=max_tokens,
            overlap_tokens=overlap_tokens
        )
    except Exception as e:  # Broad catch to return JSON error
        return jsonify({"error": "Failed to ingest document", "detail": str(e)}), 500

    response_payload = {"status": "success", "details": resp}
    if content_type_note:
        response_payload["note"] = content_type_note
    return jsonify(response_payload), 200