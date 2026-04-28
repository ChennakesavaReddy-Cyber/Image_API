import requests
import base64

API_URL = 'http://localhost:5000'

print("Testing Image Detective API...")
print("=" * 50)

print("\n1. Testing /health endpoint...")
try:
    response = requests.get(f'{API_URL}/health')
    print(f"   Status Code: {response.status_code}")
    print(f"   Response: {response.json()}")
    if response.status_code == 200:
        print("    PASS")
    else:
        print("    FAIL")
except Exception as e:
    print(f"    ERROR: {e}")

print("\n2. Testing /quota endpoint...")
try:
    response = requests.get(f'{API_URL}/quota')
    print(f"   Status Code: {response.status_code}")
    print(f"   Response: {response.json()}")
    if response.status_code == 200:
        print("    PASS")
    else:
        print("    FAIL")
except Exception as e:
    print(f"    ERROR: {e}")

print("\n3. Testing /analyze endpoint...")
try:
    from PIL import Image
    import io

    img = Image.new('RGB', (100, 100), color='red')
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    img_bytes = buffer.getvalue()
    img_base64 = base64.b64encode(img_bytes).decode('utf-8')
    img_data_url = f"data:image/png;base64,{img_base64}"

    response = requests.post(
        f'{API_URL}/analyze',
        json={'image': img_data_url},
        headers={'Content-Type': 'application/json'}
    )

    print(f"   Status Code: {response.status_code}")

    if response.status_code == 200:
        data = response.json()
        print(f"   Success: {data.get('success')}")
        print(f"   AI Verdict: {data.get('ai_detection', {}).get('verdict')}")
        print(f"   Confidence: {data.get('ai_detection', {}).get('confidence')}%")
        print(f"   TinEye Matches: {data.get('tineye', {}).get('total_matches')}")
        print("    PASS")
    else:
        print(f"   Response: {response.text}")
        print("    FAIL")

except Exception as e:
    print(f"    ERROR: {e}")

print("\n" + "=" * 50)
print("Testing complete!")
print("\nIf all tests passed, your API is working correctly!")
print("If any failed, check the Flask server terminal for errors.")