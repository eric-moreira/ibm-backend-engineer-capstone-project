from backend import app

if __name__ == '__main__':  # Script executed directly?
    print("pictures microservice.")
    app.run(host="127.0.0.1", port=8080, debug=True,use_reloader=True)
