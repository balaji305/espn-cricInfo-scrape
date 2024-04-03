import Fantasy_Point_Table
import Player_Table
import Match_Table
import Report_Generation
import Bat_vs_Bowl
import os

choice = -1
while(True):
    print("Welcome to Fantasy Cricket League Application Manager")
    print()
    print("-------------------------------------------------------")
    print("MENU")
    print("-------------------------------------------------------")
    print("1. Upload into Match Table")
    print("2. Upload into Fantasy Point Table")
    print("3. Upload into Player Table")
    print("4. Upload into Every Table")
    print("5. Upload and Generate Report")
    print("6. Generate Report only")
    print("7. Bat vs Bowl Report")
    print("8. Exit")
    print("-------------------------------------------------------")
    choice = int(input("Enter your choice: "))
    print("-------------------------------------------------------")
    print()
    if(choice == 1):
        print("Uploading into Match Table...\n")
        Match_Table.Match_Table_Call()
        print("Operation Completed Successfully!!\n")
        print("Please check the Output File to know the results.")
    elif(choice == 2):
        print("Uploading into Fantasy Point Table...\n")
        Fantasy_Point_Table.Fantasy_Point_Table_Call()
        print("Operation Completed Successfully!!\n")
        print("Please check the Output File to know the results.")
    elif(choice == 3):
        print("Uploading into Player Table...\n")
        Player_Table.Player_Table_Call()
        print("Operation Completed Successfully!!\n")
        print("Please check the Output File to know the results.")
    elif(choice == 4):
        print("Uploading into Match Table...\n")
        Match_Table.Match_Table_Call()
        print("Operation Completed Successfully!!\n")
        print("Uploading into Fantasy Point Table...\n")
        Fantasy_Point_Table.Fantasy_Point_Table_Call()
        print("Operation Completed Successfully!!\n")
        print("Uploading into Player Table...\n")
        Player_Table.Player_Table_Call()
        print("Operation Completed Successfully!!\n")
        print("Please check the Output File to know the results.")

    elif(choice == 5):
        print("Uploading into Match Table...\n")
        Match_Table.Match_Table_Call()
        print("Operation Completed Successfully!!\n")
        print("Uploading into Fantasy Point Table...\n")
        Fantasy_Point_Table.Fantasy_Point_Table_Call()
        print("Operation Completed Successfully!!\n")
        print("Uploading into Player Table...\n")
        Player_Table.Player_Table_Call()
        print("Operation Completed Successfully!!\n")
        print("Generating Report...\n")
        Report_Generation.Report_Generation_Call()
        print("Report Generated Successfully!!\n")
        print("Please check the Output File to know the results.")
        
    elif(choice == 6):
        print("Generating Report...\n")
        Report_Generation.Report_Generation_Call()
        print("Report Generated Successfully!!\n")
        print("Please check the Output File to know the results.")
    elif(choice == 7):
        print("Generating Bat vs Bowl Report...\n")
        Bat_vs_Bowl.Bat_vs_Bowl_Call()
        print("Report Generated Successfully!!\n")
        print("Please check the Output File to know the results.")
    elif(choice == 8):
        print("Thank You for using Fantasy Cricket League Application Manager")
        nxt = input("")
        break
    else:
        print("Wrong Choice! Try Again")
        continue
    print("\nPress Enter to continue")
    nxt = input("")
    os.system('cls')
