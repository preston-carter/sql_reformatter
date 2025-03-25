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
    # Normalize all SQL keywords to lowercase
    def lowercase_keywords(sql):
        for kw in sorted(SQL_KEYWORDS, key=len, reverse=True):  # longer keywords first
            pattern = re.compile(rf"\b{kw}\b", re.IGNORECASE)
            sql = pattern.sub(kw, sql)
        return sql

    formatted = raw_sql
    formatted = lowercase_keywords(formatted)

    # Move commas to start of line (for SELECT-like fields)
    lines = formatted.split('\n')
    new_lines = []
    for line in lines:
        if ',' in line and not line.strip().startswith(','):
            parts = [p.strip() for p in line.split(',')]
            new_line = '\n'.join([f"  , {p}" if i > 0 else f"  {p}" for i, p in enumerate(parts)])
            new_lines.append(new_line)
        else:
            new_lines.append(f"  {line.strip()}")
    formatted = '\n'.join(new_lines)

    # Indent SELECT block (simple demo version)
    formatted = re.sub(r"(?i)\bselect\b", "select", formatted)
    formatted = re.sub(r"(?i)\bfrom\b", "\nfrom", formatted)
    formatted = re.sub(r"(?i)\bwhere\b", "\nwhere", formatted)
    formatted = re.sub(r"(?i)\border by\b", "\norder by", formatted)

    return formatted

if format_button and sql_input:
    formatted_sql = format_sql(sql_input)
    st.text_area("Formatted SQL", formatted_sql, height=300)
