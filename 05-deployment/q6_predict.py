import pickle

from flask import Flask, request, jsonify

def load(filename:str):
    with open(filename, 'rb') as f_in:
        return pickle.load(f_in)
    
dv = load('dv.bin')
model = load('model1.bin')

app = Flask('Bank credit scoring')

@app.route('/predict', methods=['POST'])
def predict():
    client = request.get_json()
    
    X = dv.transform([client])
    y_pred = model.predict_proba(X)[0, 1]
    score = y_pred >= 0.5
    
    result = {
        'probability': float(y_pred),
        'get_credit': bool(score)
    }
    
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=9696)