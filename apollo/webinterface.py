from urllib2 import Request, urlopen, URLError

import ast

class WebInterface:
    def get_problem_name(self, number):
        url = "http://uhunt.felix-halim.net/api/p/id/{0}".format(number)
        request = Request(url)

        response = urlopen(request)
        result = response.read()
        result = ast.literal_eval(result)
        result = result["title"]
        print(result)
