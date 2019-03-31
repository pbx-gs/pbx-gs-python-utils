import  unittest

from pbx_gs_python_utils.lambdas.gsbot.gsbot_slack import run
from    pbx_gs_python_utils.utils.Dev        import *
from    pbx_gs_python_utils.utils.aws.Lambdas import Lambdas


class test_lambda_gs_bot(unittest.TestCase):

    def setUp(self):
        self.step_lambda   = Lambdas('pbx_gs_python_utils.lambdas.gsbot.gsbot_slack', memory = 3008)

    def test_lambda_update(self):
        self.step_lambda.update_with_src()

    def test_invoke_directly(self):
        payload = {'params': [], 'data': {}}
        text,attachments = run(payload,{})
        assert text == '*Here are the `Slack_Commands` commands available:*'


    def _send_command_message(self,command):
        payload = {'params' : [command] , 'data': {}}
        return self.step_lambda.update_with_lib().invoke(payload)          # see answer in slack, or add a return to line 17 (in lambda_gs_bot)

    def test_hello(self):
        response = self._send_command_message('test')
        assert response == [ ':red_circle: command not found `test`\n'
                              '\n'
                              '*Here are the `Slack_Commands` commands available:*',
                              [ { 'actions': [],
                                  'callback_id': '',
                                  'color': 'good',
                                  'fallback': None,
                                  'text': ' • stats\n • user_info\n • username_to_id\n'}]]

