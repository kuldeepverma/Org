# Org

**The project uses python version 3.8.2**  
*Make sure to install the version mentioned above for things to work flawylessly.*  

After cloning the repository CD into the folder eg. *cd Org*  

**Create a virtual environment**  
`python -m venv env`  
*this create a virtual environment, a new folder **env** will be created inside the **Org** folder.*  

**Activate the virtual environment**  
`.\env\Scripts\activate`  

*the prompt will look like* **(env)D:\Org** *which indicates that the virtual environment is now active.*

**execute the following to install project dependencies**  
`pip install -r requirements.txt`  
*this should install all the dependencies required to successfully run the project*

**serve the project**  
`python manage.py runserver`  
*this should start the server and the web application will be available at http://127.0.0.1:8000/*


**If new dependences have been added to the project, export them to the requirements.txt using**  
`pip freeze > requirements.txt`
