from app import app
import os

if __name__ == "__main__":
    # For local development
    # app.run(host="0.0.0.0", port=5000, debug=True)

    # For deployment on Render
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

