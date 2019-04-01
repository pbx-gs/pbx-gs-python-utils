import unittest
from unittest import TestCase

from pbx_gs_python_utils.gsuite.commands.Slides_Commands import Slides_Commands
from pbx_gs_python_utils.utils.Dev                       import Dev
from pbx_gs_python_utils.utils.aws.Lambdas               import Lambdas


class test_Slides_Commands(TestCase):

    #def test_update_lambda(self):
    #    Lambdas('pbx_gs_python_utils.gs.lambda_slides').update_with_src()

    def test_gs_functions(self):
        result = Slides_Commands.gs_functions('T7F3AUXGV', 'DDKUZTK6X', [])
        assert result[0] == (':point_right: Here is the current list of GS Functions (use `slides create '
                             '{{jira id}}` to create the slides:) ')

    @unittest.skip('takes long time and needs auth')
    def test_create(self):
        params = ['GSSP-241']
        result = Slides_Commands.create('T7F3AUXGV', 'DDKUZTK6X', params)
        Dev.pprint(result)
