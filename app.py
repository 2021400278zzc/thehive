from api import create_app, db

app = create_app()

@app.route('/')
def index():
    return "TheHive API 服务正常运行"

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0') 