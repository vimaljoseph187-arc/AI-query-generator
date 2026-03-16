def get_sql_prompt(user_query):
    return f"""
You are an expert MySQL query generator.
Convert the natural language request into a valid SQL query.

Request: {user_query}

Return only the SQL query. No explanation.
"""