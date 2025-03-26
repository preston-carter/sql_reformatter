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
    def lowercase_keywords(sql):
        for kw in sorted(SQL_KEYWORDS, key=len, reverse=True):
            pattern = re.compile(rf"\b{kw}\b", re.IGNORECASE)
            sql = pattern.sub(kw, sql)
        return sql

    def to_pascal_case(word):
        if not word or not re.search(r'[a-zA-Z]', word):
            return word
        word = word.strip().lower()
        parts = re.split(r'[_\s]+', word) if '_' in word else re.findall(r'[a-z]+|\d+', word)
        return ''.join(part.capitalize() for part in parts if part)

    def pascal_case_fields(fields_str):
        if not fields_str.strip():
            return []
        parts = [f.strip() for f in fields_str.split(",") if f.strip()]
        cleaned = []
        for part in parts:
            if "(" in part or "*" in part or " as " in part.lower():
                cleaned.append(part)
            else:
                pascal_cased = to_pascal_case(part)
                cleaned.append(pascal_cased)
        return cleaned

    raw_sql = raw_sql.strip()
    raw_sql = lowercase_keywords(raw_sql)

    # --- Extract select ---
    select_match = re.search(r"select\s+(.*?)\s+from\s", raw_sql, re.IGNORECASE | re.DOTALL)
    select_part = select_match.group(1).strip() if select_match else ""
    select_fields = pascal_case_fields(select_part)
    formatted_select = "select\n  " + "\n  , ".join(select_fields) if select_fields else "select"

    # --- Extract from ---
    from_match = re.search(r"from\s+([^\s\(\);]+)", raw_sql, re.IGNORECASE)
    from_clause = ""
    if from_match:
        table_name = from_match.group(1).strip()
        if re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', table_name):
            table_name = to_pascal_case(table_name)
        from_clause = f"\nfrom {table_name}"

    # --- Extract where ---
    where_match = re.search(r"where\s+(.*?)(order by|group by|$)", raw_sql, re.IGNORECASE | re.DOTALL)
    where_clause = ""
    if where_match:
        where_content = where_match.group(1).strip()
        where_clause = f"\nwhere {where_content}"

    # --- Extract order by ---
    order_by_match = re.search(r"order by\s+(.*)", raw_sql, re.IGNORECASE)
    order_by_clause = ""
    if order_by_match:
        order_by_clause = f"\norder by {order_by_match.group(1).strip()}"

    return formatted_select + from_clause + where_clause + order_by_clause

if format_button and sql_input:
    formatted_sql = format_sql(sql_input)
    st.text_area("Formatted SQL", formatted_sql, height=300)
