# KSB Log Generator

**KSB Log Generator** makes creating KSB logs easy. Simply select a week then provide a rough, natural-language account of your activities, and KSB Log Generator creates and saves a word doc ready to upload to Aptem.
- Saves doc with appropriate filename, including hours spent that week, date, and name.
- Uses OpenAI API to match KSBs and convert rough language to polished upload-ready account.
- Process multiple docs at once!

## Demo




https://github.com/johnathan217/ksb_log_generator/assets/113518999/f9030c0d-86e9-4aba-9148-0ac46e0879af

**Documents created in demo:**    

[ActivityLog_Johnathan_Phillips_6.0_17-06-2024.docx](https://github.com/user-attachments/files/16069604/ActivityLog_Johnathan_Phillips_6.0_17-06-2024.docx)    

[ActivityLog_Johnathan_Phillips_7.0_24-06-2024.docx](https://github.com/user-attachments/files/16069625/ActivityLog_Johnathan_Phillips_7.0_24-06-2024.docx)


## Prerequisites
Before you begin, ensure you have:
* Installed python - this project was made with 3.11.16
* Installed git

## Installation
#### 1. Clone the repository:
```sh
git clone https://github.com/johnathan217/ksb_log_generator.git
```
  
#### 2. Navigate to the project directory:
```sh
cd ksb_log_generator
```
  
#### 3. Set up a virtual environment (recommended):
```sh
python -m venv venv
```

#### 4. Activate the virtual environment (recommended):
  
On Windows:
```sh
venv\Scripts\activate
```
On macOS and Linux:
```sh
source venv/bin/activate
```

#### 5. Install the required packages:
```sh
pip install -r requirements.txt
```

## Configuration
Create a .env file in the project directory.    
Add the following content to the .env file:    
```sh
OPENAI_API_KEY=your_openai_api_key    
NAME=your_name
```
Replace your_openai_api_key with your actual [OpenAI API key](https://help.openai.com/en/articles/4936850-where-do-i-find-my-openai-api-key) and your_name with your name (used for creating the log filenames)

## Running the application
#### 1. Navigate to the project directory:
```sh
cd project
```
#### 2. Run app.py:
```sh
python app.py
```
This should start the flask app, showing a message like the image below. Look for 'Running on' to see the url you need to use the app.
![image](https://github.com/johnathan217/ksb_log_generator/assets/113518999/2bdf3097-9eaa-4458-b118-dfa4d329d66c)

On start, the app will create logs and outputs directories in the project root.

