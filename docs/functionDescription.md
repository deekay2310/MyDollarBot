AddUserHistory(chat_id, user_record)
- Function to update expenditure details in the json file as and when user adds them

deleteHistory(chat_id)
- Function to delete previous expenditure history of the user

getUserHistory(chat_id):
- Function to fetch user history and display it in the bot window

show_history(message)
- Function to display expendtiture history
- Error message displayed when no history present

command_display(message)
- Function to display total expenditure in a day or month, depending on the user input

display_total(message)
- Function to retrieve spending data per category from user history and return total expense

calculate_spendings(queryResult)
- Function to calculate the total expense per category from the queryResult

edit1(m)
- Function to take input from user about date and the category of the transaction they want to update
- Once user gives the correct details, function edit2 is triggered

edit2(m)
- Based on user's input from edit1, this function checks the field the user wants to update (Date, Category or Cost)
- The choice selected by the user is passed to edit3

edit3(m)
- Based on the information received from edit2, one of the following function is triggered: edit_cat, edit_date or edit_cost

edit_cat(m)
- This function is triggered if user inputs Category in edit2 function
- It will ask user for new category and update the record accordingly

edit_date(m)
- This function is triggered if user inputs Date in edit2 function
- It will ask user for new date and update the record accordingly

edit_cost(m)
- This function is triggered if user inputs Cost in edit2 function
- It will ask user for new cost and update the record accordingly
