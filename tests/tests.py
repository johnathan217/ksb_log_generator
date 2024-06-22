import json

import pandas as pd

from DocUtils import DocUtils
from test_string import test_string


class Tests:
    df = DocUtils.word_table_to_df("tests/testdoc.docx")

    @staticmethod
    def test_string_to_doc():
        DocUtils.string_to_doc(test_string, "tests/output_test_string_to_doc.docx", True)

    @staticmethod
    def test_word_table_to_df():
        print(Tests.df)

    @staticmethod
    def test_df_to_doc():
        doc = DocUtils.df_to_doc(Tests.df)
        doc.save("tests/output_test_df_to_doc.docx")

    @staticmethod
    def test_get_total_hours():
        print(DocUtils.get_total_hours(Tests.df))

    class DfInterp:
        @staticmethod
        def test_json_df():
            print(f"\nJSON:")
            print(json.dumps(json.loads((Tests.df.to_json())), indent=4))

        @staticmethod
        def test_string_df():
            print(f"\nString:")
            print(Tests.df.to_string())

        @staticmethod
        def test_csv_df():
            print(f"\nCSV:")
            print(Tests.df.to_csv())


pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

# Tests.DfInterp.test_json_df()
# Tests.DfInterp.test_string_df()
# Tests.DfInterp.test_csv_df()
# Tests.test_word_table_to_df()
#Tests.test_df_to_doc()
Tests.test_get_total_hours()