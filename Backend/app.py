from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import cv2
import numpy as np
from PIL import Image
import io
import base64
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)
TINEYE_API_KEY = os.environ.get('TINEYE_API_KEY', '')
TINEYE_API_URL = 'https://api.tineye.com/rest/search/'

search_count = {'month': datetime.now().month, 'count': 0, 'limit': 5000}


def decode_base64_image(base64_string):
    try:
        if ',' in base64_string:
            base64_string = base64_string.split(',')[1]

        img_data = base64.b64decode(base64_string)

        pil_img = Image.open(io.BytesIO(img_data))

        opencv_img = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)

        return opencv_img, pil_img
    except Exception as e:
        raise Exception(f"Failed to decode image: {str(e)}")


def perform_ela_analysis(img_pil):
    try:
        buffer1 = io.BytesIO()
        img_pil.save(buffer1, 'JPEG', quality=95)
        buffer1.seek(0)
        original = cv2.imdecode(np.frombuffer(buffer1.read(), np.uint8), cv2.IMREAD_COLOR)

        buffer2 = io.BytesIO()
        img_pil.save(buffer2, 'JPEG', quality=90)
        buffer2.seek(0)
        compressed = cv2.imdecode(np.frombuffer(buffer2.read(), np.uint8), cv2.IMREAD_COLOR)

        if original.shape != compressed.shape:
            compressed = cv2.resize(compressed, (original.shape[1], original.shape[0]))

        diff = cv2.absdiff(original, compressed)
        score = np.mean(diff)

        return min(score * 2.5, 100)
    except:
        return 0


def analyze_noise_pattern(img):
    try:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        noise = cv2.Laplacian(gray, cv2.CV_64F).var()

        if noise < 50:
            return 70
        elif noise > 500:
            return 65
        else:
            return 25
    except:
        return 0


def analyze_color_distribution(img):
    try:
        hist_b = cv2.calcHist([img], [0], None, [256], [0, 256])
        hist_g = cv2.calcHist([img], [1], None, [256], [0, 256])
        hist_r = cv2.calcHist([img], [2], None, [256], [0, 256])

        std_b = np.std(hist_b)
        std_g = np.std(hist_g)
        std_r = np.std(hist_r)

        avg_std = (std_b + std_g + std_r) / 3

        if avg_std < 100:
            return 60
        else:
            return 20
    except:
        return 0


def analyze_edge_consistency(img):
    try:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 100, 200)
        edge_density = np.sum(edges > 0) / edges.size

        if edge_density < 0.05 or edge_density > 0.3:
            return 50
        else:
            return 15
    except:
        return 0


def detect_ai_photoshop(opencv_img, pil_img):
    results = {
        'is_ai_generated': False,
        'is_photoshopped': False,
        'confidence': 0,
        'verdict': 'Unknown',
        'tests': []
    }

    try:
        ela_score = perform_ela_analysis(pil_img)
        noise_score = analyze_noise_pattern(opencv_img)
        color_score = analyze_color_distribution(opencv_img)
        edge_score = analyze_edge_consistency(opencv_img)

        results['tests'] = [
            {'name': 'ELA (Photoshop Detection)', 'score': round(ela_score, 1)},
            {'name': 'Noise Pattern (AI Detection)', 'score': round(noise_score, 1)},
            {'name': 'Color Distribution', 'score': round(color_score, 1)},
            {'name': 'Edge Consistency', 'score': round(edge_score, 1)}
        ]

        avg_score = (ela_score + noise_score + color_score + edge_score) / 4
        results['confidence'] = round(avg_score, 1)

        if avg_score > 70:
            results['verdict'] = 'High Risk'
            results['is_ai_generated'] = noise_score > 60 or edge_score > 45
            results['is_photoshopped'] = ela_score > 60
        elif avg_score > 35:
            results['verdict'] = 'Medium Risk'
            results['is_ai_generated'] = noise_score > 40
            results['is_photoshopped'] = ela_score > 30
        else:
            results['verdict'] = 'Low Risk (Likely Authentic)'

        return results

    except Exception as e:
        results['error'] = str(e)
        return results


def search_tineye(image_base64):
    global search_count

    current_month = datetime.now().month
    if search_count['month'] != current_month:
        search_count = {'month': current_month, 'count': 0, 'limit': 5000}

    if search_count['count'] >= search_count['limit']:
        return {
            'error': 'Monthly search limit reached',
            'quota': {
                'used': search_count['count'],
                'limit': search_count['limit'],
                'remaining': 0
            }
        }

    search_count['count'] += 1

    if not TINEYE_API_KEY:
        return {
            'total_matches': 42,
            'first_appearance': {
                'date': '2021-03-15',
                'url': 'https://example.com/original-source',
                'domain': 'example.com'
            },
            'top_matches': [
                {
                    'url': 'https://example.com/original-source',
                    'domain': 'example.com',
                    'crawl_date': '2021-03-15',
                    'size': '1920x1080'
                },
                {
                    'url': 'https://news-site.com/article-123',
                    'domain': 'news-site.com',
                    'crawl_date': '2021-04-20',
                    'size': '1920x1080'
                },
                {
                    'url': 'https://social-media.com/post/456',
                    'domain': 'social-media.com',
                    'crawl_date': '2021-05-10',
                    'size': '1080x1080'
                }
            ],
            'quota': {
                'used': search_count['count'],
                'limit': search_count['limit'],
                'remaining': search_count['limit'] - search_count['count']
            },
            'note': 'Using mock data. Set TINEYE_API_KEY environment variable for real results.'
        }

    try:
        import requests

        if ',' in image_base64:
            image_base64 = image_base64.split(',')[1]

        response = requests.post(
            TINEYE_API_URL,
            data={
                'image_upload': image_base64,
                'api_key': TINEYE_API_KEY
            },
            timeout=30
        )

        if response.status_code == 200:
            data = response.json()
            matches = data.get('results', {}).get('matches', [])

            first_appearance = None
            if matches:
                oldest = min(matches, key=lambda x: x['crawl_date'])
                first_appearance = {
                    'date': oldest['crawl_date'],
                    'url': oldest['backlink'],
                    'domain': oldest['domain']
                }

            return {
                'total_matches': len(matches),
                'first_appearance': first_appearance,
                'top_matches': matches[:5],
                'quota': {
                    'used': search_count['count'],
                    'limit': search_count['limit'],
                    'remaining': search_count['limit'] - search_count['count']
                }
            }
        else:
            return {'error': f'TinEye API error: {response.status_code}'}

    except Exception as e:
        return {'error': str(e)}


@app.route('/', methods=['GET'])
def home():
    return jsonify({
        'service': 'Image Detective API',
        'status': 'online',
        'version': '1.0.0',
        'endpoints': {
            'health': '/health',
            'quota': '/quota',
            'analyze': '/analyze (POST)'
        }
    })


@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        'status': 'ok',
        'service': 'Image Detective API',
        'timestamp': datetime.now().isoformat()
    })


@app.route('/quota', methods=['GET'])
def get_quota():
    return jsonify({
        'used': search_count['count'],
        'limit': search_count['limit'],
        'remaining': search_count['limit'] - search_count['count'],
        'month': search_count['month']
    })


@app.route('/analyze', methods=['POST', 'OPTIONS'])
def analyze():

    if request.method == 'OPTIONS':
        return '', 204

    try:
        data = request.get_json()

        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400

        if 'image' not in data:
            return jsonify({'error': 'No image provided in request'}), 400

        image_base64 = data['image']

        opencv_img, pil_img = decode_base64_image(image_base64)

        ai_results = detect_ai_photoshop(opencv_img, pil_img)

        tineye_results = search_tineye(image_base64)

        response = {
            'success': True,
            'ai_detection': ai_results,
            'tineye': tineye_results
        }

        return jsonify(response)

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


if __name__ == '__main__':
    print("\n" + "=" * 60)
    print(" IMAGE DETECTIVE API SERVER")
    print("=" * 60)
    print(f" Server running on: http://localhost:5000")
    print(f" Health check: http://localhost:5000/health")
    print(f" Get quota: http://localhost:5000/quota")
    print(f" Analyze endpoint: http://localhost:5000/analyze (POST)")
    print("=" * 60)
    print("\nTest the server:")
    print("   1. Open browser: http://localhost:5000/health")
    print("   2. You should see: {'status': 'ok', ...}")
    print("\n Note: TinEye mock data is being used.")
    print("   Set TINEYE_API_KEY environment variable for real results.\n")

    app.run(debug=True, port=5000, host='0.0.0.0')
