from utils.project import languages,project
#the create_braille_table function is used to create the braille table for lib louis
#the create_braille_tests function is used to create the braille tests for lib louis
#the get_braille_from_text_in_source function is used to convert the text characters to braille characters in the source language file
from utils.braille import create_braille_table, create_braille_tests, get_braille_from_text_in_source
#The create_filtered_csv function is used to create the filtered csv file
#The regenerate_characters_using_hex function is used to regenerate the characters in the language source file
from utils.csv import create_filtered_csv, regenerate_characters_using_hex
#The add_characters_to_nvda function is used to add the symbols to the nvda symbols file
#The generate_locale_file function is used to generate the locale file for nvda
#The generate_character_set function is used to generate the character set for nvda
from utils.nvda import add_characters_to_nvda,generate_locale_file, generate_character_set

print("Please Choose a Language")
#This loop prints out the languages that are available for the user to choose from
#we use index+1 to make the index start at 1 instead of 0
for index,language in enumerate(languages):
    print(str(index+1)+": "+languages[index]["name"]+",",end=" ")
#The user is asked to choose a language
language_option=int(input("Choose a Language"))-1
print("Select one of the following options")
print("""
1: generate filtered spreadsheet,
2: generate Locale File for nvda,
3: generate Character Set for NVDA,
4: Generate braille table for LibLouis,
5: regenerate characters,
6: convert text characters to braille characters,
7: produce a braille test,
8: to add symbols to nvda
""")
option=int(input("enter a number one through 8"))
#option 1 creates the filtered csv file
if option == 1:
    create_filtered_csv()
#option 2 generates locale file for nvda
elif option==2:
    generate_locale_file(language_option)
#option 3 generates the character set for nvda
elif option==3:
    generate_character_set(language_option)
#option 4 creates the braille table for lib louis
elif option==4:
    create_braille_table(language_option)
#option 5 regenerates the characters in the language file
elif option==5:
    regenerate_characters_using_hex(language_option)
    #option 6 converts the text characters to braille characters in the source language file    
elif option == 6:
    get_braille_from_text_in_source(language_option)
#option 7 creates the braille tests for Lib Louis
elif option==7:
    create_braille_tests(language_option)
#option 8 adds the symbols to the nvda symbols file
elif option==8:
    add_characters_to_nvda(language_option)
#If the user enters an invalid option, they are told that the option is not valid
else:
    print("That was not a valid option")
