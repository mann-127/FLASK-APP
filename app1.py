from flask import Flask, jsonify, request
from supabase import create_client, Client
import os
from dotenv import load_dotenv
 
load_dotenv()
 
# --- Supabase Configuration ---
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

app = Flask(__name__)

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
 
# --- Core Services ---
 
@app.route("/")
def hello():
    """A simple welcome message."""
    return "Hello! This API interacts with a real Supabase 'todos' table."
 
# --- Todo Management Endpoints ---
 
@app.route("/api/todos", methods=["POST"])
def create_todo():
    """
    Creates a new todo in the Supabase 'todos' table.
    Expects JSON body with 'task' (string) and optional 'priority'.
    """
    data = request.get_json()
    if not data or 'task' not in data:
        return jsonify({"error": "Missing 'task' in JSON body"}), 400
 
    try:
        new_task = str(data['task']).strip()
        if not new_task:
            return jsonify({"error": "Task cannot be empty"}), 400
 
        # Prepare the record for Supabase
        new_record = {
            "task": new_task,
            "is_complete": False,
            "priority": data.get("priority", "Medium")
        }
        
        # Insert into Supabase
        response = supabase.table("todos").insert(new_record).execute()
        
        if hasattr(response, 'data') and response.data:
            return jsonify({
                "message": "Todo created successfully",
                "data": response.data[0]
            }), 201
        else:
            return jsonify({"error": "Failed to create todo"}), 500
 
    except Exception as e:
        return jsonify({"error": f"Server error: {str(e)}"}), 500
 
 
@app.route("/api/todos", methods=["GET"])
def get_todos():
    """
    Fetches all todos from the Supabase 'todos' table.
    """
    try:
        response = supabase.table("todos").select("*").execute()
        
        return jsonify({
            "data": response.data,
            "count": len(response.data),
            "status": "success"
        })
 
    except Exception as e:
        return jsonify({"error": f"Failed to fetch todos: {str(e)}"}), 500
 
 
@app.route("/api/todos/<int:todo_id>", methods=["GET"])
def get_todo(todo_id):
    """
    Fetches a specific todo by ID from Supabase.
    """
    try:
        response = supabase.table("todos").select("*").eq("id", todo_id).execute()
        
        if not response.data:
            return jsonify({"error": "Todo not found"}), 404
            
        return jsonify({
            "data": response.data[0],
            "status": "success"
        })
 
    except Exception as e:
        return jsonify({"error": f"Failed to fetch todo: {str(e)}"}), 500
 
 
@app.route("/api/todos/<int:todo_id>", methods=["PUT"])
def update_todo(todo_id):
    """
    Updates a specific todo in Supabase.
    Expects JSON body with fields to update.
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided for update"}), 400
 
    try:
        # Remove id from update data if present
        update_data = {k: v for k, v in data.items() if k != 'id'}
        
        if not update_data:
            return jsonify({"error": "No valid fields to update"}), 400
 
        response = supabase.table("todos").update(update_data).eq("id", todo_id).execute()
        
        if not response.data:
            return jsonify({"error": "Todo not found"}), 404
            
        return jsonify({
            "message": "Todo updated successfully",
            "data": response.data[0]
        })
 
    except Exception as e:
        return jsonify({"error": f"Failed to update todo: {str(e)}"}), 500

@app.route("/api/todos/<int:todo_id>", methods=["DELETE"])
def delete_todo(todo_id):
    """
    Deletes a specific todo from Supabase.
    """
    try:
        # First check if todo exists
        check_response = supabase.table("todos").select("id").eq("id", todo_id).execute()
        
        if not check_response.data:
            return jsonify({"error": "Todo not found"}), 404
 
        # Delete the todo
        delete_response = supabase.table("todos").delete().eq("id", todo_id).execute()
        
        return jsonify({
            "message": "Todo deleted successfully",
            "deleted_id": todo_id
        }), 200
 
    except Exception as e:
        return jsonify({"error": f"Failed to delete todo: {str(e)}"}), 500
 
# --- Utility Services ---
 
@app.route("/api/health", methods=["GET"])
def health_check():
    """Health check endpoint to verify API and database connectivity."""
    try:
        # Test database connection
        test_response = supabase.table("todos").select("id").limit(1).execute()
        
        return jsonify({
            "status": "healthy",
            "service": "supabase-todo-api",
            "database": "connected"
        }), 200
        
    except Exception as e:
        return jsonify({
            "status": "unhealthy",
            "service": "supabase-todo-api",
            "database": "disconnected",
            "error": str(e)
        }), 503
 
 
if __name__ == "__main__":
    # Note: debug=True should be disabled in production
    app.run(debug=False, use_reloader=False)
