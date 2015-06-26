import urllib.request
import ast

def get_problem_name(number):
    url = "http://uhunt.felix-halim.net/api/p/id/{0}".format(number)

    with urllib.request.urlopen(url) as response:
        result = response.read()
        result = ast.literal_eval(result.decode('utf-8'))
        result = result["title"]

    return result
