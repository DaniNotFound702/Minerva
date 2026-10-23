import sys
import json
import ImportData.ZermeloMain as zportal_api

def main():
    print("What would you like to scrape?")
    print("1. Appointments")
    print("2. Branches of Schools")
    print("3. Departments of Branches")
    print("4. Branches")
    print("5. Choosable in Departments")
    print("6. Group in Departments")
    print("7. Holidays")
    print("8. Location of Branches")
    print("9. Schools in School Years")
    print("10. Timeslot Names")
    print("11. Students in Departments")
    print("12. Subject Selection Subjects")
    print("0. Exit")
    
    choice = input("\nEnter the number of your choice: ")

    try:
        if choice == '1':
            sy_id = input("Enter schoolYear_id (e.g. 602): ")
            sy = input("Enter schoolYear (e.g. 2026): ")
            user_id = input("Enter user_id (press Enter for default 21187): ")
            user_id = int(user_id) if user_id else 21187
            result = zportal_api.appointments(schoolYear_id=sy_id, schoolYear=sy, user_id=user_id)
        
        elif choice == '2':
            result = zportal_api.branchesofschools()
        
        elif choice == '3':
            result = zportal_api.departmentsofbranches()
            
        elif choice == '4':
            result = zportal_api.branches()
            
        elif choice == '5':
            result = zportal_api.choosableindepartments()
            
        elif choice == '6':
            result = zportal_api.groupindepartments()
            
        elif choice == '7':
            result = zportal_api.holidays()
            
        elif choice == '8':
            result = zportal_api.locationofbranches()
            
        elif choice == '9':
            sy = input("Enter schoolYear (e.g. 602): ")
            result = zportal_api.schoolsinschoolyears(sy)            
        elif choice == '10':
            sy = input("Enter schoolYear (press Enter if not needed): ")
            result = zportal_api.timeslotnames(sy)
            
        elif choice == '11':
            sy = input("Enter schoolYear (press Enter if not needed): ")
            result = zportal_api.studentsindepartments(sy)
            
        elif choice == '12':
            sy = input("Enter schoolYear (press Enter if not needed): ")
            result = zportal_api.subjectselectionsubjects(sy)
            
        elif choice == '0':
            print("Exiting...")
            sys.exit()
        else:
            print("Invalid choice. Please try again.")
            return

        print("\n--- RESULT ---")
        print(json.dumps(result, indent=4))
        
    except Exception as e:
        print(f"\nAn error occurred: {e}")

if __name__ == "__main__":
    main()