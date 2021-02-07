#Setup Project 

##Requirements
 - python 3.8
 - check requirements.txt

##Setup
1. Create new virtual environment with python 3.8
2. Activate environment
3. Install requirements (pip install -r requirements.txt)
4. Run migrate command (python manage.py migrate)
5. Add your google geocoding API key in settings.py (GOOGLE_PLACE_API_KEY = "API-KEY")   
5. Run server (python manage.py runserver)
6. Visit http://localhost:8000

##File structure

----------
xls file must contain only one column `ADDRESS`

|ADDRESS|

|BTM layout Bangalore|
