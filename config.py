import os

ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")
MONGO_URI         = "mongodb://localhost:27017/"
MYSQL_CONFIG      = {"host":"localhost","user":"root","password":"root","database":"capstone_db"}
OUTPUT_DIR        = "output"
LOGS_DIR          = "logs"

PROMPT_SIZES = [8000, 8000, 8000, 12000, 12000, 6000, 6000, 6000]

TECH_MODULES = ["Unix","Shell Scripting","MongoDB","Python","PySpark Core","Advanced SQL","Power BI","Analysis"]