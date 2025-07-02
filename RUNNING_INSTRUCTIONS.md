# How to Run and Close the Dividend Tracker Program

## Running the Program

1. **Install Python:**
   - Make sure Python is installed on your computer. You can get it from the [Python website](https://www.python.org/downloads/).

2. **Install Required Tools:**
   - Open the terminal (or command prompt).
   - Go to the folder where the program is located.
   - Type this command to install the necessary tools:
     ```
     pip install -r requirements.txt
     ```

3. **Start the Program:**
   - In the terminal, type:
     ```
     uvicorn app.main:app --reload
     ```
   - Open your web browser and go to `http://localhost:8000` to see the program.
   - For front end, type:
     ```
     streamlit run frontend/app.py
     ```
     

## Closing the Program

1. **Stop the Program:**
   - In the terminal, press `Ctrl + C` to stop the program.

2. **Clean Up:**
   - If there are any extra files created by the program, you can delete them to save space.