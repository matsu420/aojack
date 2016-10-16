import requests
import websocket
import json
import re


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

    testcase_pat = re.compile('http://analytic.u-aizu.ac.jp:8080/aoj/testcase.jsp\?id=[a-zA-Z0-9_]+&case=')
    def __init__(self, userID, password):
        self.userID = userID
        self.password = password

    def get_file(self, runID, case, in_file = False, out_file = False):
        url = "http://judge.u-aizu.ac.jp/onlinejudge/review.jsp?rid="
        url += runID

        res = requests.get(url)

        url = AOJ.testcase_pat.search(res.text).group()

        url += case
        url += "&type="

        if not url is None:
            try:
                if in_file:
                    with open(runID + '_in.txt', 'w') as f:
                        res = requests.get(url + 'in')
                        f.write(res.text.encode('utf-8'))
            except IOError:
                print "Failed to write input"
            except requests.exceptions.ConnectionError:
                print "Failed to download input"
            except:
                raise

            try:
                if out_file:
                    with open(runID + '_out.txt', 'w') as f:
                        res = requests.get(url + 'out')
                        f.write(res.text.encode('utf-8'))
            except IOError:
                print "Failed to write output"
            except requests.exceptions.ConnectionError:
                print "Failed to download output"
            except:
                raise

        else:
            print "Failed to access runID status"


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
                    print 'RunID:' + str(submit_result['runID'])
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

