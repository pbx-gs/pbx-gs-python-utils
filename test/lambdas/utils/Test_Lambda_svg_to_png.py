import base64
import tempfile

import  pydot
import  unittest
from    utils.Dev              import Dev
from utils.Files import Files
from    utils.Show_Img import Show_Img
from    utils.aws.Lambdas      import Lambdas


class Test_Lambda_svg_to_png(unittest.TestCase):
    def setUp(self):
        self.svg_to_png = Lambdas('utils.svg_to_png')

    def test_simple_png_transformation(self):
        params = { "svg": "PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0idXRmLTgiPz4KPCEtLSBHZW5lcmF0b3I6IEFkb2JlIElsbHVzdHJhdG9yIDE0LjAuMCwgU1ZHIEV4cG9ydCBQbHVnLUluIC4gU1ZHIFZlcnNpb246IDYuMDAgQnVpbGQgNDMzNjMpICAtLT4KPCFET0NUWVBFIHN2ZyBQVUJMSUMgIi0vL1czQy8vRFREIFNWRyAxLjEvL0VOIiAiaHR0cDovL3d3dy53My5vcmcvR3JhcGhpY3MvU1ZHLzEuMS9EVEQvc3ZnMTEuZHRkIj4KPHN2ZyB2ZXJzaW9uPSIxLjEiIGlkPSJMYXllcl8xIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHhtbG5zOnhsaW5rPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5L3hsaW5rIiB4PSIwcHgiIHk9IjBweCIKd2lkdGg9IjUwNXB4IiBoZWlnaHQ9IjUwNXB4IiB2aWV3Qm94PSIwIDAgNTA1IDUwNSIgZW5hYmxlLWJhY2tncm91bmQ9Im5ldyAwIDAgNTA1IDUwNSIgeG1sOnNwYWNlPSJwcmVzZXJ2ZSI+CjxyZWN0IHk9IjAuNDk4IiBmaWxsPSIjRkJERTM0IiB3aWR0aD0iNTA0LjY3IiBoZWlnaHQ9IjUwNC40NDIiLz4KPGc+CjxwYXRoIGZpbGw9IiM1MjQ3MzkiIGQ9Ik0yMTcuNTAzLDM4OC42OTF2MTQuNzU3aC0xNi4xNTV2MzkuNzY2YzAsMy43MjksMC42MjEsNi4yMTQsMS44NjQsNy40NTcKYzEuMjQzLDEuMjQyLDMuNzI4LDEuODYzLDcuNDU2LDEuODYzYzEuMjQzLDAsMi40MzItMC4wNTEsMy41NzMtMC4xNTVjMS4xMzgtMC4xMDIsMi4yMjYtMC4yNTcsMy4yNjItMC40NjZWNDY5CmMtMS44NjQsMC4zMTEtMy45MzcsMC41MTctNi4yMTMsMC42MjFjLTIuMjc5LDAuMTAzLTQuNTA1LDAuMTU1LTYuNjgsMC4xNTVjLTMuNDE3LDAtNi42NTUtMC4yMzItOS43MDgtMC42OTgKYy0zLjA1Ni0wLjQ2Ny01Ljc0Ny0xLjM3Mi04LjA3Ny0yLjcxOWMtMi4zMy0xLjM0NS00LjE3LTMuMjYyLTUuNTE1LTUuNzQ3Yy0xLjM0Ny0yLjQ4NS0yLjAxOS01Ljc0OC0yLjAxOS05Ljc4NnYtNDcuMzc4aC0xMy4zNTkKdi0xNC43NTdoMTMuMzU5di0yNC4wNzdoMjIuMDU4djI0LjA3N0gyMTcuNTAzeiIvPgo8cGF0aCBmaWxsPSIjNTI0NzM5IiBkPSJNMjQ4LjU2OSwzNTguMDkxdjQxLjc4NWgwLjQ2NmMyLjc5Ni00LjY2LDYuMzY5LTguMDUxLDEwLjcxOC0xMC4xNzVjNC4zNDktMi4xMjEsOC41OTQtMy4xODUsMTIuNzM3LTMuMTg1CmM1LjkwMywwLDEwLjc0MiwwLjgwNCwxNC41MjQsMi40MDhjMy43NzgsMS42MDYsNi43NTcsMy44MzIsOC45MzIsNi42OGMyLjE3NSwyLjg0OSwzLjcwMSw2LjMxNyw0LjU4MiwxMC40MDcKYzAuODc5LDQuMDkyLDEuMzIsOC42MjEsMS4zMiwxMy41OTJWNDY5aC0yMi4wNTh2LTQ1LjM1N2MwLTYuNjI3LTEuMDM2LTExLjU3My0zLjEwNi0xNC44MzUKYy0yLjA3My0zLjI2Mi01Ljc0Ny00Ljg5NC0xMS4wMjktNC44OTRjLTYuMDA3LDAtMTAuMzU2LDEuNzg3LTEzLjA0OCw1LjM1OWMtMi42OTQsMy41NzMtNC4wMzksOS40NTEtNC4wMzksMTcuNjMxVjQ2OWgtMjIuMDU4ClYzNTguMDkxSDI0OC41Njl6Ii8+CjxwYXRoIGZpbGw9IiM1MjQ3MzkiIGQ9Ik0zMzQuNDY3LDQ0OS43MzhjMy4zMTMsMy4yMTEsOC4wNzcsNC44MTUsMTQuMjkxLDQuODE1YzQuNDUxLDAsOC4yODMtMS4xMTEsMTEuNDk1LTMuMzQKYzMuMjA4LTIuMjI2LDUuMTc3LTQuNTgyLDUuOTAyLTcuMDY3aDE5LjQxN2MtMy4xMDYsOS42MzEtNy44NzEsMTYuNTE5LTE0LjI5MSwyMC42NTljLTYuNDIyLDQuMTQ0LTE0LjE4OCw2LjIxNC0yMy4zLDYuMjE0CmMtNi4zMTgsMC0xMi4wMTUtMS4wMS0xNy4wODctMy4wMjljLTUuMDc1LTIuMDItOS4zNzQtNC44OTMtMTIuODk0LTguNjIxYy0zLjUyMS0zLjcyOC02LjI0LTguMTgtOC4xNTQtMTMuMzU4CmMtMS45MTgtNS4xNzgtMi44NzQtMTAuODc0LTIuODc0LTE3LjA4N2MwLTYuMDA1LDAuOTgyLTExLjU5NywyLjk1MS0xNi43NzZjMS45NjYtNS4xNzcsNC43NjItOS42NTUsOC4zODgtMTMuNDM3CmMzLjYyNC0zLjc3OSw3Ljk0Ny02Ljc1NywxMi45NzEtOC45MzJjNS4wMjEtMi4xNzUsMTAuNTg3LTMuMjYzLDE2LjY5OS0zLjI2M2M2LjgzNCwwLDEyLjc4OCwxLjMyLDE3Ljg2MywzLjk2MgpjNS4wNzIsMi42NDEsOS4yNDIsNi4xODgsMTIuNTA0LDEwLjY0YzMuMjYzLDQuNDU0LDUuNjE3LDkuNTI5LDcuMDY4LDE1LjIyNGMxLjQ0OSw1LjY5NiwxLjk2NiwxMS42NDksMS41NTMsMTcuODYzSDMyOS4wMwpDMzI5LjM0MSw0NDEuMzUxLDMzMS4xNTEsNDQ2LjUzLDMzNC40NjcsNDQ5LjczOHogTTM1OS4zOTgsNDA3LjQ4N2MtMi42NDEtMi44OTgtNi42NTUtNC4zNS0xMi4wMzktNC4zNQpjLTMuNTIxLDAtNi40NDYsMC41OTgtOC43NzYsMS43ODZjLTIuMzMsMS4xOTItNC4xOTMsMi42NjgtNS41OTIsNC40MjhjLTEuMzk4LDEuNzYyLTIuMzg0LDMuNjI2LTIuOTUxLDUuNTkyCmMtMC41NywxLjk2OS0wLjkwOCwzLjcyOC0xLjAxLDUuMjgxaDM1Ljg4MkMzNjMuODc2LDQxNC42MzMsMzYyLjAzOSw0MTAuMzg4LDM1OS4zOTgsNDA3LjQ4N3oiLz4KPHBhdGggZmlsbD0iIzUyNDczOSIgZD0iTTQxMy4yMjEsMzg4LjY5MXYxMS4xODVoMC40NjZjMi43OTYtNC42Niw2LjQyLTguMDUxLDEwLjg3NC0xMC4xNzVjNC40NTEtMi4xMjEsOS4wMDktMy4xODUsMTMuNjY5LTMuMTg1CmM1LjkwMywwLDEwLjc0MiwwLjgwNCwxNC41MjQsMi40MDhjMy43NzgsMS42MDYsNi43NTcsMy44MzIsOC45MzIsNi42OGMyLjE3NSwyLjg0OSwzLjcwMSw2LjMxNyw0LjU4MiwxMC40MDcKYzAuODc5LDQuMDkyLDEuMzIsOC42MjEsMS4zMiwxMy41OTJWNDY5SDQ0NS41M3YtNDUuMzU3YzAtNi42MjctMS4wMzYtMTEuNTczLTMuMTA2LTE0LjgzNWMtMi4wNzMtMy4yNjItNS43NDctNC44OTQtMTEuMDI5LTQuODk0CmMtNi4wMDcsMC0xMC4zNTYsMS43ODctMTMuMDQ4LDUuMzU5Yy0yLjY5NCwzLjU3My00LjAzOSw5LjQ1MS00LjAzOSwxNy42MzFWNDY5SDM5Mi4yNXYtODAuMzA5SDQxMy4yMjF6Ii8+CjwvZz4KPC9zdmc+Cg=="}
        result = self.svg_to_png.upload_and_invoke(params)
        Show_Img.from_svg_string(result['image'])

    def test_simple_pydot(self):
        graph = pydot.Dot(graph_type='digraph')
        graph.add_edge(pydot.Edge("aaa","bbb"))
        #tmp_name = tempfile.mkstemp()
        #graph.write_svg(tmp_name, prog='dot')
        dot = graph.to_string()

        pydot_lambda = Lambdas('dev.pydot_test')
        dot_code = pydot_lambda.invoke({'name': 'test'})
        params       = {"svg" : base64.b64encode(dot_code.encode()).decode() }

        result = self.svg_to_png.upload_and_invoke(params)

        Show_Img.from_svg_string(result['image'])
        #Dev.pprint(dot)

        print(result)

    def test_create_dot_then_svg_then_png(self):
        dot_to_svg = Lambdas('utils.dot_to_svg').invoke
        svg_to_png = Lambdas('utils.svg_to_png').invoke

        dot     = 'digraph { abc -> edfAAAAA \n abc [shape=box] } '
        svg     = dot_to_svg({"dot" : dot})
        result  = svg_to_png({"svg": svg })
        png     = result['image']

        Show_Img.from_svg_string(png)