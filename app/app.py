from flask import Flask, render_template, jsonify, request
import model
app = Flask(__name__)

@app.route('/')
@app.route('/index')
def chat():
    return render_template('chat.html')

@app.route('/predict', methods=['POST','GET'])
def predict_emotion():
    if request.method == 'POST':
        msg = request.form['user_msg']
        print('[app.py] predict(POST), msg=',msg)
    else: 
        msg = request.args.get('user_msg')
        print('[app.py] predict(GET), msg=',msg)
    # predict_result = mymodel.predict('엘사는 예전보다 더 강한 여자가 되어 있었다.')
    predict_result = mymodel.predict(msg)
    print("[app.py] 예측값: ",float(predict_result[0]),", 판단: ",predict_result[1])
    data={'result':float(predict_result[0]), 'answer':predict_result[1]}
    return jsonify(data)

mymodel = model.MyModel('./../model/model_file.h5')
# app.run(debug = True)