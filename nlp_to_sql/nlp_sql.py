import os
import gradio as gr
import duckdb
import pandas as pd
from openai import OpenAI
from vault_local import open_api_key
from tabulate import tabulate

openai = OpenAI(api_key=open_api_key)
MODEL = 'gpt-4o-mini'

conn = duckdb.connect()


def process_query(csv_file, question):
    try:
        df = pd.read_csv(csv_file)
        table_name = "uploaded_data"
        conn.register(table_name, df)
        actual_columns = list(df.columns)
        # Preprocessing Step: Fix Spelling Mistakes in Question
        correction_prompt = f"""
        Fix any spelling mistakes in the following question to make it clear:
        **Original Question:**  
        {question}
        **Corrected Question:**
        """
        correction_response = openai.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": correction_prompt}]
        )
        corrected_question = correction_response.choices[0].message.content.strip()
        # Convert Corrected Question to SQL
        sql_prompt = f"""
        Convert the following question into a **valid SQL query** for the DuckDB table `{table_name}`.
        ### Rules:
        - **Return only the SQL query** without any extra text, explanations, or formatting.
        - Generate only a SELECT query.
        - If the question contains **misspelled column names**, correct them using this list: {', '.join(actual_columns)}
        - Do NOT use INSERT, UPDATE, DELETE, DROP, or ALTER.
        - Correct any spelling errors in column names.
        - If a column mentioned in the question doesn't exist, suggest the correct column.
        - Assume `{table_name}` has relevant columns.
        - output sql query should look like this SELECT * FROM uploaded_data;

        ### Question:
        {corrected_question}

        ### SQL Query:
        """
        response = openai.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": sql_prompt}]
        )
        sql_query = response.choices[0].message.content.strip()
        result_df = conn.execute(sql_query).df()
        if result_df.empty:
            return "No results found for the given query."

        # Convert result to Markdown/JSON format
        readable_output = tabulate(result_df, headers="keys", tablefmt="grid")

        # Step 4: Convert SQL result to a human-readable response
        summary_prompt = f"""
        Given the following SQL query result, summarize the key insights in a human-readable format.

        ### Question:
        {corrected_question}

        ### SQL Query:
        ```sql
        {sql_query}
        ```

        ### Query Result:
        ```
        {readable_output}
        ```

        ### Human-Readable Summary:
        """
        summary_response = openai.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": summary_prompt}]
        )
        human_summary = summary_response.choices[0].message.content.strip()

        return f"**Query Summary:**\n{human_summary}\n\n**Query Result:**\n```\n{readable_output}\n```"

    except Exception as e:
        return f"❌ Error: {str(e)}"


gr.Interface(
    fn=process_query,
    inputs=["file", "text"],
    outputs="text"  # Change from "dataframe" to "text"
).launch()
