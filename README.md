# WorksSale-SaasBasedSalesManagementSoftware
Works Sale tackles inefficiencies in sales management by offering an easy-to-use CRM and sales acceleration tool. It streamlines forecasting, monitors sales across branches, and helps businesses achieve their targets, saving time and boosting sales effectiveness.

# Before Running the Project:
For the project to run a bash terminal is needed. In PowerShell or cmd the command(source .env) is not working so please follow the below steps to successfully run the project.
Download - https://git-scm.com/download/win
In cmd - pip install six
Change the Vs code default terminal to bash
once the bash terminal is open run - cd main_part
source .env (This command will connect Django to mail via SMTP)(This command is a must before running the server every time)
python manage.py runserver
# Content:
Once the user creates an account a confirmation mail will be sent to him.
The user will be able to log in only if he has activated the account by clicking the link sent to his mail.
For the activation links to send to users I have created a dummy mail id.
The dummy mail id login details are provided in the (main_part>.env) file.
