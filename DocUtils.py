from typing import List, Optional
from docx import Document
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from io import StringIO
import pandas as pd


class DocUtils:
    @staticmethod
    def doc_to_string(input_path: str) -> str:
        doc: Document = Document(input_path)
        full_text: List[str] = []
        for table in doc.tables:
            table_data: List[List[str]] = []
            for row in table.rows:
                row_data: List[str] = []
                for cell in row.cells:
                    cell_text: str = '\n'.join([para.text for para in cell.paragraphs])
                    row_data.append(cell_text)
                table_data.append(row_data)
            df: pd.DataFrame = pd.DataFrame(table_data)
            full_text.append('TABLE_START')
            full_text.append(df.to_csv(index=False, sep='\t'))
            full_text.append('TABLE_END')

        text: str = "\n".join(full_text)
        return text

    @staticmethod
    def string_to_doc(text: str, file_path: str) -> None:
        doc: Document = Document()
        lines: List[str] = text.split('\n')

        table_data: List[str] = []
        inside_table: bool = False

        for line in lines:
            if line == 'TABLE_START':
                inside_table = True
                table_data = []
            elif line == 'TABLE_END':
                inside_table = False
                if table_data:
                    df: pd.DataFrame = pd.read_csv(StringIO('\n'.join(table_data)), sep='\t')
                    df = df.fillna(' ')
                    table = doc.add_table(rows=df.shape[0], cols=df.shape[1])
                    for i, row in df.iterrows():
                        for j, cell in enumerate(row):
                            table.cell(i, j).text = str(cell)

                    for row in table.rows:
                        for cell in row.cells:
                            tc = cell._element
                            tcPr = tc.get_or_add_tcPr()
                            tcBorders = OxmlElement('w:tcBorders')
                            for border_name in ["top", "left", "bottom", "right"]:
                                border = OxmlElement(f'w:{border_name}')
                                border.set(qn('w:val'), 'single')
                                border.set(qn('w:sz'), '4')
                                border.set(qn('w:space'), '0')
                                border.set(qn('w:color'), '000000')
                                tcBorders.append(border)
                            tcPr.append(tcBorders)
                table_data = []
            elif inside_table:
                table_data.append(line)
            else:
                doc.add_paragraph(line)

        doc.save(file_path)

    @staticmethod
    def extract_table_content(text: str) -> Optional[str]:
        start_marker: str = "TABLE_START"
        end_marker: str = "TABLE_END"

        start_index: int = text.find(start_marker)
        end_index: int = text.find(end_marker)

        if start_index == -1 or end_index == -1:
            return None

        end_index += len(end_marker)

        table_content: str = text[start_index:end_index].strip()

        return table_content

    @staticmethod
    def calculate_total_hours(table_string: str) -> float:
        lines: List[str] = table_string.split('\n')
        table_data: List[str] = []
        inside_table: bool = False

        for line in lines:
            if line == 'TABLE_START':
                inside_table = True
                table_data = []
            elif line == 'TABLE_END':
                inside_table = False
                if table_data:
                    df: pd.DataFrame = pd.read_csv(StringIO('\n'.join(table_data)), sep='\t')
                    df = df.fillna(' ')
                    if 'Hours' in df.columns:
                        hours_total: float = df['Hours'].astype(float).sum()
                        return hours_total
                    else:
                        print("The 'Hours' column was not found in the DataFrame.")
            elif inside_table:
                table_data.append(line)

        return 0.0