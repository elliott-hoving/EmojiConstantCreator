from pathlib import Path

# define variables for paths to HTML files in project, change default encoding
html1 = Path.open(Path.cwd() / 'HTML1.html', 'r', encoding='utf-8')
html2 = Path.open(Path.cwd() / 'HTML2.html', 'r', encoding='utf-8')

# open the files, copy contents into strings
html1_str = html1.read()
html2_str = html2.read()

index = 0
counter = 0

while counter < 3:
    # find index of next occurrence of HTML row element
    index = html1_str.find("<tr id=\"emoji", index, -1)

    # starting from index, find td element storing unicode, assign to variable
    sub_index = html1_str.find("U+", index, -1)
    utf_code = "U+" + html1_str[sub_index+2:sub_index+7]

    # starting from index, find first appearance of hex prefix "\x", copy hex code into variable
    sub_index = html1_str.find("\\x", index, -1)
    hex_code = html1_str[sub_index:sub_index+16]

    # starting from index, find first appearance of HTML class identifier for name, read until /td
    # copy name into variable
    sub_index = html1_str.find("\"name\">", index, -1)
    end_of_name = html1_str.find("/td", sub_index, -1)
    print("sub" + str(sub_index))
    print("end" + str(end_of_name))
    name = html1_str[sub_index+7:end_of_name-1]

    # TODO this does not work because there are multiple tables
    # TODO add criteria for beginning of each table and end of each table

    #print(index)
    #print(utf_code)
    #print(hex_code)
    print(name)

    index = html1_str.find("/tr", index, -1)
    counter = counter + 1









