from flask import Flask, request, jsonify
from flask_cors import CORS
from sql_agent import answer_from_db
app = Flask(__name__)
CORS(app)  


#flask api podt request route 
@app.route('/askdb', methods=['POST'])
def handle_query():    
    if request.method=='POST':
        user_query = request.json['query']


        try:
            response=answer_from_db(user_query)
            return jsonify({"response":response}), 200
        except ValueError as e:
                return jsonify({'error': str(e)}), 400

        except Exception as e:
                return jsonify({'error': 'An error occurred while processing your request.'}), 500



if __name__ == '__main__':
    app.run(debug=True)
