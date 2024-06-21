from DocUtils import DocUtils
from test_string import test_string


class Tests:
    @staticmethod
    def test_string_to_doc():
        DocUtils.string_to_doc(test_string, "output_test", True)


Tests.test_string_to_doc()
