from webapp import app

if __name__ == '__main__':
    app.secret_key='123456'
    app.run(debug=True, host='192.168.0.104')