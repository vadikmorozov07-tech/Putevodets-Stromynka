from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from navigate import generate_route

app = Flask(__name__)

CORS(app, resources={
    r"/api/*": {
        "origins": "*",
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

@app.route('/api/generate-route', methods=['POST', 'OPTIONS'])
def generate_route_endpoint():
    
    if request.method == 'OPTIONS':
        return '', 204
    
    try:
        data = request.get_json()
        room_from = data.get('roomFrom', '').strip()
        room_to = data.get('roomTo', '').strip()
        
        if not room_from or not room_to:
            return jsonify({
                'success': False,
                'error': 'Укажите оба кабинета'
            }), 400
        
        if room_from == room_to:
            return jsonify({
                'success': False,
                'error': 'Кабинеты совпадают'
            }), 400
        
        result = generate_route(room_from, room_to)
        
        if not result['success']:
            return jsonify({
                'success': False,
                'error': 'Ошибка в построении маршрута, проверьте введённые кабинеты'
            }), 400
        
        return jsonify(result), 200
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Ошибка сервера: {str(e)}'
        }), 500

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/health')
def health():
    return jsonify({'status': 'ok'}), 200

@app.errorhandler(404)
def not_found(e):
    return jsonify({'error': 'Страница не найдена'}), 404

@app.errorhandler(500)
def server_error(e):
    return jsonify({'error': 'Ошибка сервера'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8001, debug=False)
