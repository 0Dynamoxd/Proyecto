from app import create_app

app = create_app()

if __name__ == '__main__':
    #app.run(debug=True)
    # Configuración para usar SSL (HTTPS)
    
    # Configuración para usar SSL (HTTPS) con las rutas correctas en Windows
    app.run(debug=True, host='0.0.0.0', port=5000,
            ssl_context=('C:\\Users\\fisgo\\Downloads\\127.0.0.1.pem', 
                         'C:\\Users\\fisgo\\Downloads\\127.0.0.1-key.pem'))