import requests
import websocket
import json


class AOJ:
    extension = {
            'c': 'C',
            'cpp': 'C++14',
            'rb': 'Ruby',
            'java': 'JAVA',
            'py': 'Python',
            }

    status_code_str = [
            "Compile Error",
            "Wrong Answer",
            "Time Limit Exceeded",
            "Memory Limit Exceeded",
            "Accepted",
            "Waiting Judge",
            "Output Limit Exceeded",
            "Runtime Error",
            "Presentation Error",
            "Running",
            "Judge Not Available",
            ]

    def __init__(self, userID, password):
        self.userID = userID
        self.password = password


    def submit(self, problemNO, language, sourceCode, lessonID = "", live = True):

        data = {"problemNO": problemNO,
                "lessonID": lessonID,
                "language": language,
                "sourceCode": sourceCode,
                }

        data['userID'] = self.userID
        data['password'] = self.password

        ws = None

        if live:
            ws = websocket.create_connection('ws://ionazn.org/status')

        res = requests.post('http://judge.u-aizu.ac.jp/onlinejudge/webservice/submit', data = data)

        if "UserID or Password is Wrong." in res.text:
            print "UserID or Password is Wrong"
        elif "Invalid problem" in res.text:
            print "Invalid problem"
        elif live:
            while True:
                submit_result = json.loads(ws.recv())
                if submit_result['userID'] == self.userID and submit_result['status'] != 5 and submit_result['status'] != 9:
                    print submit_result['problemTitle'] + ': ', 
                    print AOJ.status_code_str[submit_result['status']]
                    break


    def submit_file(self, path, problemNO, lessonID = "", live = True):
        sourceCode = ""
        try:
            with open(path, "r") as f:
                sourceCode = f.read()
        except IOError:
            print "No such file or directory: " + path
        except:
            raise
        else:
            ex_index = path.rfind('.') + 1
            language = AOJ.extension[path[ex_index: ]]

            self.submit(problemNO, language, sourceCode, lessonID, live)

