from flask import Flask, request, jsonify
from flask_cors import CORS
from sql_agent import answer_from_db
from database import add_user,update_user_record,read_user_record,find_user
import datetime
app = Flask(__name__)
CORS(app)  

def handle_old_user(user_id,user_query):
    try:
        user_previous_data=read_user_record(user_id)
        if user_previous_data !=None:
            print("old user 2 -------")
            old_time=user_previous_data[2]
            old_time=datetime.datetime.strptime(old_time, "%Y-%m-%d %H:%M:%S")
            
            current_time = datetime.datetime.now()
            print("Current Time: ",current_time)
            print("Old Time: ",old_time)
            history=user_previous_data[1]
            response=""
            time_difference = current_time - old_time
            print("Time difference : ",time_difference)
            print("total differece in seconds : ",time_difference.total_seconds())
            if((time_difference.total_seconds())>= 5 * 60):
                print("Old")
                response = answer_from_db(user_query,"Old",str(history))
            else:
                print("current")
                response = answer_from_db(user_query,"current",str(history))
            if len(history) < 5:
                history.append(
                    {
                        "HumanMessage": user_query,
                        "AIMessage": response
                    }
                )
            else:
                history.pop(0)
                history.append(
                    {
                        "HumanMessage": user_query,
                        "AIMessage": response
                    }
                )
            update_user_record(user_id,history)
            return response
    except Exception as e:
        print("Exceptions : ",str(e))
    


def handle_new_user(user_id,user_query):
    response = answer_from_db(user_query,"New",str([]))
    history = [
        {
            "HumanMessage": user_query,
            "AIMessage": response
        }
    ]
    print("IN handle new user : ----- ")
    add_user(user_id,history)
    return response



@app.route('/askdb', methods=['POST'])
def handle_query():
    try:
        data = request.get_json()

        #check if all requirements are present in api call
        if 'user_query' not in data:
            raise ValueError("Missing 'user_query' in the input JSON.")
        if 'user_id' not in data:
            raise ValueError("Missing 'user_id' in the input JSON.")
        
        #extract required data from api call
        user_query = data['user_query']
        # user_id=data['user_id']

        #check user if exsit or not
        # if(find_user(user_id)):
        #     response = handle_old_user(user_id,user_query)
        #     return jsonify({'response': response}), 200
        # else:
        #     print("old user ---- 2: ")
        #     response=handle_new_user(user_id,user_query)
        #     return jsonify({'response': response}), 200
        response=answer_from_db(user_query)
        return jsonify({"response":response}), 200


    except ValueError as e:
        return jsonify({'error': str(e)}), 400

    except Exception as e:
        return jsonify({'error': 'An error occurred while processing your request.'}), 500


if __name__ == '__main__':
    app.run(debug=True)
