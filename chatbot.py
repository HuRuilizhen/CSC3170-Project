import streamlit as st
import requests
import json
import dashscope
from dashscope import Generation
import re
# Define dashscope API key
dashscope.api_key = "sk-a02071870d814c4a83c74b176638098f"

# Define the get_response function for dashscope
def get_dashscope_response(messages): 
    response = Generation.call(
        "qwen-turbo", 
        messages=messages,
        result_format="message",
    )
    return response

# Define the get_gpt_response function for GPT 3.5
def get_gpt_response(messages):
    url = "https://oa.api2d.net/v1/chat/completions"
    payload = json.dumps(
        {
            "model": "gpt-3.5-turbo",
            "messages": messages,
            "safe_mode": False,
        }
    )
    headers = {
        "Authorization": "Bearer fk216155-ybzDrTKBFD4QDsLvTt07er4yNISFMdm3",
        "User-Agent": "Apifox/1.0.0 (https://apifox.com)",
        "Content-Type": "application/json",
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    response_json = response.json()
    return response_json["choices"][0]["message"]["content"]

# Define messages with just the system prompt message.

def main(user_input, llm_choice):
    prompt = (
        "You are an ai database query assistant for a website. The user enters their queries, and you only output sql and nothing else. The table you want to interact with has the following structure"
    "CREATE TABLE `course_list`  ("
    "`year` int NULL DEFAULT NULL,"
    "`term` varchar(255) CHARACTER NULL DEFAULT NULL,"
    "`year_term` varchar(255)  NULL DEFAULT NULL,"
    "`subject` varchar(255)  NOT NULL,"
    "`number` int NOT NULL,"
    "`name` varchar(255)  NULL DEFAULT NULL,"
    "`description` text  NULL,"
    "`credit_hours` varchar(255)   NULL DEFAULT NULL,"
    "`section_info` text  NULL,"
    "`degree_attributes` varchar(255)   NULL DEFAULT NULL,"
    "`schedule_information` text   NULL,"
    "`CRN` int NULL DEFAULT NULL,"
    "`section` varchar(255)  NOT NULL,"
    "`status_code` varchar(255)  NULL DEFAULT NULL,"
    "`part_of_term` varchar(255)  NULL DEFAULT NULL,"
    "`section_title` varchar(255)  NULL DEFAULT NULL,"
    "`section_credit_hours` varchar(255)  NULL DEFAULT NULL,"
    "`section_status` varchar(255)  NULL DEFAULT NULL,"
    "`enrollment_status` varchar(255)  NULL DEFAULT NULL,"
    "`type` varchar(255)   NULL DEFAULT NULL,"
    "`type_code` varchar(255)  NOT NULL,"
    "`start_time` varchar(255)  NULL DEFAULT NULL,"
    "`end_time` varchar(255)  NULL DEFAULT NULL,"
    "`days_of_week` varchar(255)  NULL DEFAULT NULL,"
    "`room` varchar(255)  NULL DEFAULT NULL,"
    "`building` varchar(255)  NULL DEFAULT NULL,"
    "`instructors` text NULL,"
    "PRIMARY KEY (`subject`, `number`, `section`, `type_code`) USING BTREE,"
    "INDEX `number`(`number` ASC) USING BTREE"
    "ENGINE = InnoDB ROW_FORMAT = Dynamic;"
) # include your prompt here

    messages = [{"role": "system", "content": prompt}]

    # Append the user message to the message list
    messages.append({"role": "user", "content": user_input})
    
    # Conditional call based on LLM selection
    if llm_choice == 'Dashscope LLM':
        # Call the get_response function to get a response from dashscope
        response = get_dashscope_response(messages)
        assistant_output = response["output"]["choices"][0]["message"]["content"]
    else:
        # Call the get_response function to get a response from GPT 3.5
        assistant_output = get_gpt_response(messages)

    def extract_sql_queries(markdown_text):
        # Pattern to capture SQL queries enclosed in triple backticks
        pattern = r"```sql\n(.*?)\n```"
            
        # Find all occurrences of the pattern
        raw_queries = re.findall(pattern, markdown_text, re.DOTALL)
        return raw_queries
        
    assistant_output = extract_sql_queries(assistant_output)
    # Display the AI generated SQL to the user
    st.text_area("AI Generated SQL", assistant_output, height=100)
    # Clear the input for next interaction
    messages = [{"role": "system", "content": prompt}]
    print (assistant_output)
    return assistant_output

# Define messages with just the system prompt message.

prompt = (
        "You are an ai database query assistant for a website. The user enters their queries, and you only output sql and nothing else. The table you want to interact with has the following structure"
   "CREATE TABLE `course_list`  ("
  "`year` int NULL DEFAULT NULL,"
  "`term` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,"
"  `year_term` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,"
"  `subject` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,"
"  `number` int NOT NULL,"
"  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,"
"  `description` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,"
"  `credit_hours` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,"
"  `section_info` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,"
"  `degree_attributes` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,"
"  `schedule_information` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,"
"  PRIMARY KEY (`year_term`, `subject`, `number`) USING BTREE,"
"  INDEX `number`(`number` ASC) USING BTREE,"
"  INDEX `year_term`(`year_term` ASC) USING BTREE,"
"  INDEX `subject`(`subject` ASC) USING BTREE"
") ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;"

"CREATE TABLE `course_section`  ("
"  `year_term` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,"
"  `subject` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,"
"  `number` int NOT NULL,"
"  `CRN` int NULL DEFAULT NULL,"
"  `section` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,"
"  `status_code` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,"
"  `part_of_term` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,"
"  `section_title` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,"
"  `section_credit_hours` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,"
"  `section_status` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,"
"  `enrollment_status` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,"
"  `type` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,"
"  `type_code` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,"
"  `start_time` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,"
"  `end_time` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,"
"  `days_of_week` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,"
"  `room` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,"
"  `building` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,"
"  `instructors` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,"
"  PRIMARY KEY (`year_term`, `subject`, `number`, `section`, `type_code`) USING BTREE,"
"  INDEX `subject_f`(`subject` ASC) USING BTREE,"
"  INDEX `number_f`(`number` ASC) USING BTREE,"
"  CONSTRAINT `number_f` FOREIGN KEY (`number`) REFERENCES `course_list` (`number`) ON DELETE RESTRICT ON UPDATE RESTRICT,"
"  CONSTRAINT `subject_f` FOREIGN KEY (`subject`) REFERENCES `course_list` (`subject`) ON DELETE RESTRICT ON UPDATE RESTRICT,"
"  CONSTRAINT `year_term_f` FOREIGN KEY (`year_term`) REFERENCES `course_list` (`year_term`) ON DELETE RESTRICT ON UPDATE RESTRICT"
") ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;"
)

messages = [{"role": "system", "content": prompt}]