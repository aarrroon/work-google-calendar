# YOUR PROJECT TITLE
    #### Video Demo:  https://youtu.be/qYX3E2Qb6x4
    #### Description: This project involves using a simplfied Google Calendar API (gcsa) to extract my shifts from IKEA.
                      From this, the project can obtain which shifts are in the payslip, how much tax is withheld, gross
                      income, add shifts and obtain dates of future or previous payslips. 

### Features:

###### 1. Obtaining Shifts From Given Payslip
    By inputting the date of a payslip or using the current payslip, each shift in the payslip is obtained from Google 
    Calendar and is displayed in a user friendly format like '2022-07-24 - 6:00 to 14:00 on a Sunday'. This can be used 
    to see future shifts if the current payslip is used, or to see previous shifts.


###### 2. Calculating Tax and Gross Income of a Given Payslip
    By inputting the date of a payslip, the gross income can be calculated which is the the total income minus the 
    tax withheld. The method to calculate the tax withheld is by using the formula on the ATO for an Australian resident 
    This is also includes the tax-free threshold. As a result of this, the amount paid each fortnight can be checked 
    with this project to ensure the correct amount is paid.

###### 3. Calculating Types of Hours in a Payslip
    For IKEA, different hours have different loading, which includes evening, Saturday, Sunday, Public holiday loading. 
    This project will calculate the various different hours worked in the payslip.

###### 4. Obtain the Dates of Future and Past Payslips
    A list of dates of payslips will be displayed in order to use the other features with different payslips. The output
    will be in the iso-format which is 'YYYY-MM-DD'.

###### 5. Add Shifts to the Calendar
    Rather than going on the Google Calendar, this provides a fast method to input as many shifts as required and add it 
    to the Google Calendar. 

### Design Choices

###### 1. Class Methods VS Global Functions
    Originally, the global function print_shift was to be implemented as a instance method of the Payslip class. However,
    when writing the function add_calendar_shifts, I wanted to confirm and print out what the user has inputted, and this
    could be done by using the print_shift instance method. However, in order for a function to use the instance method, 
    the method needs to be a class method. However, if this was the case, then the function would not be able to use the 
    attributes of the Payslip class, and therefore it was better to just be a function rather than a method of the Payslip 
    class.

###### 2. Using the Official Google Calendar API vs Google Calendar Simplified API
    I was planning to use the official API as this would give me more experience and accelerate my learning. However, 
    the simplified version was adequate as I only needed to extract the events from the calendar and add events and the 
    simple version would have suffice.

###### 3. Output of 'calculate_tax' Function
    Another design choice was what to output in the calculate_tax function. The decision was between just displaying
    the tax withheld, or just the gross pay. In the end, both was outputted as this was determined to provide more 
    information, and it was outputted as a tuple. 





