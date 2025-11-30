from flask import Flask, jsonify, request, abort
 
app = Flask(__name__)
 
# --- Arithmetic Services (GET with Query Parameters) ---
 
@app.route("/")
def hello():
    # How to call: http://127.0.0.1:5000/
    return "Hello, CI/CD! This is a simple REST API."
 
# 1. Add (Query Parameters)
@app.route("/add", methods=["GET"])
def add_numbers():
    """Calculates a + b using query parameters."""
    # How to call: http://127.0.0.1:5000/add?a=7&b=6
    try:
        a = int(request.args.get("a", 0))
        b = int(request.args.get("b", 0))
        return jsonify({"result": a + b})
    except ValueError:
        return jsonify({"error": "Invalid input: 'a' and 'b' must be integers"}), 400
 
# 2. Subtract (Query Parameters)
@app.route("/subtract", methods=["GET"])
def subtract_numbers():
    """Calculates a - b using query parameters."""
    # How to call: http://127.0.0.1:5000/subtract?a=7&b=78
    try:
        a = int(request.args.get("a", 0))
        b = int(request.args.get("b", 0))
        return jsonify({"result": a - b})
    except ValueError:
        return jsonify({"error": "Invalid input: 'a' and 'b' must be integers"}), 400
 
# 3. Multiply (Query Parameters)
@app.route("/multiply", methods=["GET"])
def multiply_numbers():
    """Calculates a * b using query parameters."""
    # How to call: http://127.0.0.1:5000/multiply?a=4&b=11
    try:
        a = int(request.args.get("a", 0))
        b = int(request.args.get("b", 0))
        return jsonify({"result": a * b})
    except ValueError:
        return jsonify({"error": "Invalid input: 'a' and 'b' must be integers"}), 400

# 4. Divide (Query Parameters)
@app.route("/divide", methods=["GET"])
def divide_numbers():
    """Calculates a / b using query parameters, handling division by zero."""
    # How to call: http://127.0.0.1:5000/divide?a=100&b=4
    try:
        a = int(request.args.get("a", 0))
        b = int(request.args.get("b", 0))
 
        if b == 0:
            return jsonify({"error": "Division by zero is not allowed"}), 400
 
        return jsonify({"result": a / b})
    except ValueError:
        return jsonify({"error": "Invalid input: 'a' and 'b' must be integers"}), 400

# 5. Cube (Query Parameters) - NEW
@app.route("/cube", methods=["GET"])
def cube_number():
    """Calculates the cube (x * x * x) of a single number 'x'."""
    # How to call: http://127.0.0.1:5000/cube?x=3
    try:
        x = int(request.args.get("x", 0))
        return jsonify({"result": x ** 3})
    except ValueError:
        return jsonify({"error": "Invalid input: 'x' must be an integer"}), 400

# 8. Calculate Area (POST with JSON) - NEW
@app.route("/area", methods=["POST"])
def calculate_area():
    """Calculates the area of a rectangle based on JSON body data."""
    # How to call (e.g., using curl or Postman):
    # curl -X POST -H "Content-Type: application/json" -d '{"width": 5, "height": 10}' http://127.0.0.1:5000/area
    
    data = request.get_json()
    if not data or 'width' not in data or 'height' not in data:
        return jsonify({"error": "Missing 'width' or 'height' in JSON body"}), 400
 
    try:
        width = int(data['width'])
        height = int(data['height'])
        area = width * height
        return jsonify({"result": area, "units": "square units"})
    except ValueError:
        return jsonify({"error": "Width and height must be integers"}), 400
    except Exception:
        return jsonify({"error": "Invalid JSON format"}), 400

# 10. Health Check (GET) - NEW
@app.route("/health", methods=["GET"])
def health_check():
    """A standard endpoint to check if the API is running correctly."""
    # How to call: http://127.0.0.1:5000/health
    return jsonify({"status": "ok", "service": "calculator-api"}), 200
 
if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
