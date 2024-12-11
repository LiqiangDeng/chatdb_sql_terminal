# ChatDB: A SQL like chat database software based on console interaction

This project mainly focuses on developing a kind of interactive ChatGPT-like application that can help user to interact with the database. They can learn how to query data in database system, and perform some simple operations through dialogue with the program. The program currently only supports console terminal interaction and only supports MySQL database.

---

## About

This project is mainly used for the Data Science course at USC.

### Key Features
- Create table structures, upload data
- Explore databases and show table
- Obtain sample queries
- Execute the queries directly
- Ask questions in natural language

### Key File Introduction

- data: Some dataset in csv file.
- report: Course report and document.
- main.py: Program entrance, main process.
- mysql_conn.py: Configuration and tool methods for connecting databases.
- example.py: Generate example SQL queries.
- nlp.py: Process user's natural language input, return SQL .queries and explanations.
- upload.py: Create table structure and upload data.
- import_old.py (Abandoned): The table structure and data upload of the old version dataset. This file is only for archiving and saving purposes. 

---

## Getting Started

### Prerequisites

- Python >= 3.10
- You can check the required libraries in the requirements.txt file

```bash
git clone git@github.com:LiqiangDeng/chatdb_sql_terminal.git

pip install -r requirements.txt
```
---

### Usage

You can first modify the database connection configuration information from the 'mysql_conn.py' file, and then obtain the table structure in the 'upload.py' file. You can choose to manually create the table structure or run it separately to complete the initial table structure creation and test data upload.

(Optional) Recommend manually creating table structures based on database configuration
```base
python upload.py
```

Enter the main program
```bash
python main.py
```

After entering the main program, you can interact according to the prompts. You can enter the name 'help' to view the help guide.

## Contact
Name: Liqiang Deng

Email: liqiangd@usc.edu/liqiangdengemail@gmail.com
