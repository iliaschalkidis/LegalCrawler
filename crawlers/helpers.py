import re


def clean_text(text: str):
    text = re.sub(r'(<\/(li|ul|ol|br|p|h1|h2)>)', r'\g<0>\n', text)
    return re.sub(r'(<\/[^>]+>)', r'\g<0> ', text)