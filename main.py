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

    def pascal_case_fields(fields_str):
        parts = [f.strip() for f in fields_str.split(",") if f.strip()]
        cleaned = []
        for part in parts:
            # Skip if function, wildcard, or alias present
            if "(" in part or "*" in part or " as " in part.lower():
                cleaned.append(part)
            else:
                words = part.split()
                pascal_cased = ' '.join(to_pascal_case(w) for w in words)
                cleaned.append(pascal_cased)
        return cleaned

    def pascal_case_fields(fields_str):
        parts = [f.strip() for f in fields_str.split(",")]
        cleaned = []
        for part in parts:
            # Avoid touching functions or wildcards
            if "(" in part or "*" in part or " as " in part.lower():
                cleaned.append(part)
            else:
                words = part.split()
                pascal_cased = ' '.join(to_pascal_case(w) for w in words)
                cleaned.append(pascal_cased)
        return cleaned

    raw_sql = raw_sql.strip()
    raw_sql = lowercase_keywords(raw_sql)

    select_match = re.search(r"select(.*?)from", raw_sql, re.IGNORECASE | re.DOTALL)
    from_match = re.search(r"from\s+([^\s;]+)", raw_sql, re.IGNORECASE)

    select_part = select_match.group(1).strip() if select_match else ""
    formatted_select_fields = pascal_case_fields(select_part)
    formatted_select = "select\n  " + "\n  , ".join(formatted_select_fields)

    # PascalCase the table name in FROM
    from_clause = ""
    if from_match:
        table_name = from_match.group(1).strip()
        from_clause = f"\nfrom {to_pascal_case(table_name)}"

    # Add WHERE and ORDER BY if present
    where_match = re.search(r"where(.*?)(group by|order by|$)", raw_sql, re.IGNORECASE | re.DOTALL)
    order_by_match = re.search(r"order by(.*)", raw_sql, re.IGNORECASE | re.DOTALL)

    where_part = where_match.group(1).strip() if where_match else ""
    order_by_part = order_by_match.group(1).strip() if order_by_match else ""

    formatted = formatted_select
    if from_clause:
        formatted += from_clause
    if where_part:
        formatted += f"\nwhere {where_part}"
    if order_by_part:
        formatted += f"\norder by {order_by_part}"

    return formatted

if format_button and sql_input:
    formatted_sql = format_sql(sql_input)
    st.text_area("Formatted SQL", formatted_sql, height=300)
