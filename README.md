# AI-FOR-EDUCATION

## Steps to Run this Project

### 1. Clone this Repository

Run this command in the terminal at the directory where you want to store this project:

```bash
git clone https://github.com/nurturegrit/auto_grading_assignments.git
```

### 2. Install Requirements

Run this in the terminal (Ensure you have Python installed):

```bash
pip install -r requirements.txt
```

#### Setting Up Backend Database

1. Install `sqlite3` on your system.
2. Navigate to the `databases` folder.
3. Run the following commands in the terminal:
   ```bash
   sqlite3 data.db
   .read schema.sql
   .read initial_inserts.sql
   .exit
   ```
4. Return to the root folder of the project.

#### Setting Up Keys Config

1. Create a new folder named `Keys`.
2. Create a JSON file `autograder_config.json` within the `Keys` folder:

   ```json
   {
       "email": "***",  // Email with SMTP connection available for third-party applications
       "password": "****",  // Password for the email connection
       "smtp": "smtp.mail.**.com",  // SMTP of the service provider of your email
       "model_name": "gpt-4o-mini",
       "endpoint": "https://models.inference.ai.azure.com"
   }
   ```

3. Create another JSON file `tester_config.json` in the `Keys` folder:

   ```json
   {
       "endpoint": "https://models.inference.ai.azure.com",
       "model_name": "gpt-4o-mini"
   }
   ```

4. Create a text file `key.txt` in the 'Keys' folder:

   ```
   your_key_for_gpt-40-mini_connection_here
   ```

5. Return to the root folder of the project.

### 3. Launch The Application

Run the following command in the terminal from the root directory (`auto_grading_assignments`):

```bash
python3 app.py
```

Open a browser and go to:

```
http://127.0.0.1:5000
```

- You will see a Teacher's Login and a Student's Login.

#### Teacher's Login

- Login using any credentials (authentication not required).
- Click the `Create New Assignment` button.
- Add assignment details and questions (use the `Add Another Question` button).
- Click the `Make Assignment` button.

A new assignment will be created in the backend, generating:

- A JSON file with assignment details.
- A questions folder with questions in TXT files.
- A test cases folder with Python test case files for testing.

#### Student's Login

- Login using your name.
- The Dashboard will display all assignments available in the database.
- Click on the newly created assignment.

You'll notice that assignment questions have constraints for their solutions, created during test case generation.

- Upload solutions for each question by clicking the `Upload Solution` button.

#### Grading Assignments

- Navigate to the root directory of the project in the terminal.
- Run the following command:

```bash
python3 main.py $Assignment_Name
```

Replace `$Assignment_Name` with any assignment name in the database.

In the backend, we have implemented:

- Test case checking for student solutions.
- Grading and feedback retrieval from the GPT-4o-mini API.
- Feedback email sent to students with emails in the database.
- Grade storage in the `data.db` database.