from pathlib import Path

# define variables for paths to HTML files in project, change default encoding
html1 = Path.open(Path.cwd() / 'HTML1.html', 'r', encoding='utf-8')
html2 = Path.open(Path.cwd() / 'HTML2.html', 'r', encoding='utf-8')

# open the files, copy contents into strings
html1_str = html1.read()
html2_str = html2.read()

# tables[0] is the text before the first table
tables = html1_str.split("<table")

# tables[1] is first table up until next table opening tag "<table....>"
# there should only be one set of rows to analyze now
counter = 1

# analyze each table individually, starting at 1
while counter < len(tables):

    # move this to examine each row <tr> element
    # find index of first occurrence of <tr>, initialize
    index = tables[counter].find("<tr id=\"emoji")

    # index returns -1 when there are no more <tr> elements in this table
    while index != -1:

        # starting from index, find td element storing unicode, assign to variable
        sub_index = tables[counter].find("U+", index, -1)
        utf_code = "U+" + tables[counter][sub_index+2:sub_index+7]

        # starting from index, find first appearance of hex prefix "\x", copy hex code into variable
        sub_index = tables[counter].find("\\x", index, -1)
        hex_code = tables[counter][sub_index:sub_index+16]

        # starting from index, find first appearance of tag class identifier for name, read until /td
        # copy name into variable
        sub_index = tables[counter].find("\"name\">", index, -1)
        end_of_name = tables[counter].find("</td>", sub_index, -1)
        name = tables[counter][sub_index+7:end_of_name]

        print(utf_code)
        print(hex_code)
        print(name)

        # set index to somewhere below most recent assignment, so that find() finds the next occurrence
        index = tables[counter].find("<tr id=\"emoji", sub_index, -1)

    counter = counter + 1







