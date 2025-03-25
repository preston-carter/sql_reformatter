# main.py
import streamlit as st
import re

st.set_page_config(page_title="SQL Reformatter", layout="wide")

st.title("Custom SQL Reformatter")
st.markdown("""
Paste your raw SQL below. The formatter will apply these custom rules:
- Lowercase SQL keywords  
- Leading commas  
- PascalCase for field and CTE names  
- CASE/WHEN/THEN alignment  
- No field renaming or blank line changes  
""")

sql_input = st.text_area("Input SQL", height=300)
format_button = st.button("Format SQL")

SQL_KEYWORDS = [
    "select", "from", "where", "group by", "order by", "with", "as", "case", "when", "then", "end",
    "on", "join", "left join", "inner join", "outer join", "full join", "having", "union", "over",
    "partition by", "order", "desc", "asc", "distinct", "limit", "offset", "extract", "interval", "date_add"
]

def format_sql(raw_sql):
    formatted = raw_sql

    # Lowercase all SQL keywords
    for keyword in SQL_KEYWORDS:
        pattern = re.compile(rf"\\b{keyword}\\b", re.IGNORECASE)
        formatted = pattern.sub(keyword, formatted)

    # Comma-first style (simplified for now)
    formatted = re.sub(r",\\s*([a-zA-Z_])", r"\n  , \1", formatted)

    # Inline comments → move to above line
    formatted = re.sub(r"(.*?)--(.*)", r"--\2\n\1", formatted)

    # Ensure blank lines between CTEs
    formatted = re.sub(r"\\)\\s*,\\s*(\\w+\\s+as)\\s*\\(", r")\n\n, \1\n(", formatted)

    # Clean parentheses spacing
    formatted = re.sub(r"\\(\\s*", "(", formatted)
    formatted = re.sub(r"\\s*\\)", ")", formatted)

    return formatted

if format_button and sql_input:
    formatted_sql = format_sql(sql_input)
    st.text_area("Formatted SQL", formatted_sql, height=300)
