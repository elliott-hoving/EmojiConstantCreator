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

# list that will store unicode, hex code, and name from HTML1
list_of_tuples = []

# analyze each table individually, starting at 1
for i in range(len(tables)):

    # move this to examine each row <tr> element
    # find index of first occurrence of <tr>, initialize
    index = tables[i].find("<tr id=\"emoji")

    # index returns -1 when there are no more <tr> elements in this table
    while index != -1:

        # starting from index, find td element storing unicode, assign to variable
        sub_index = tables[i].find("U+", index, -1)
        end_of_unicode = ""
        if tables[i].find(" ", sub_index, -1) < tables[i].find("\"", sub_index, -1):
            end_of_unicode = tables[i].find(" ", sub_index, -1)
        else:
            end_of_unicode = tables[i].find("\"", sub_index, -1)
        unicode = tables[i][sub_index:end_of_unicode]

        # starting from index, find first appearance of hex prefix "\x", copy hex code into variable
        sub_index = tables[i].find("\\x", index, -1)
        end_of_hex = tables[i].find("<", sub_index, -1)
        hex_code = tables[i][sub_index:end_of_hex]

        # starting from index, find first appearance of tag class identifier for name, read until /td
        # copy name into variable
        sub_index = tables[i].find("\"name\">", index, -1)
        end_of_name = tables[i].find("</td>", sub_index, -1)
        name = tables[i][sub_index + 7:end_of_name]

        # create a tuple with each bit of extracted data, then add to list for later
        list_of_tuples.append((unicode, hex_code, name))

        # print(unicode)
        # print(hex_code)
        # print(name)

        # set index to somewhere below most recent assignment, so that find() finds the next occurrence
        index = tables[i].find("<tr id=\"emoji", sub_index, -1)

    i = i + 1

# at this point, HTML1 is fully analyzed and appropriate data is stored in tuples

unicode_hash = {}
# cut off the first bit of CSS, just makes it easier
html2_str = html2_str.split("</style>")[1]

rows = html2_str.split("<tr>")
for i in range(2, len(rows)):

    lines = rows[i].splitlines();
    name = ""
    unicode_found = False
    unicode = 0

    for tag in lines:

        first_colon = tag.find(":", 0, -1)
        if first_colon != -1:

            second_colon = tag.find(":", first_colon+1, -1)
            if second_colon != -1:
                name = tag[first_colon:second_colon+1]

        if unicode_found == False:
            sub_index = tag.find("U+", 0, -1)
            if sub_index != -1:
                if tag.find(" ", sub_index, -1) != -1:
                    end_of_unicode = tag.find(" ", sub_index, -1)
                else:
                    end_of_unicode = tag.find("<", sub_index, -1)
                unicode = tag[sub_index:end_of_unicode]
                unicode_found = True

    print(unicode)
    unicode_hash[unicode] = name

# at this point, HTML2 is fully analyzed and values are stored in an associative array

output_file = open("output.txt", "w+")


# write a PHP define in which a keyword defines a string
def write_define_str(arg_1, arg_2):
    return "define(\"" + arg_1 + "\"" + "," + "\"" + arg_2 + "\");"


# write a PHP define in which a keyword defines a number
def write_define_num(arg_1, arg_2):
    return "define(\"" + arg_1 + "\"" + "," + arg_2 + ");"


# iterate over each emoji tuple in the list
for emoji in list_of_tuples:
    # [0] is the unicode in tuple
    # [1] is hex code in tuple
    # [2] is the index of the name in the tuple
    name = emoji[2].upper().replace(" ", "_")
    hex_code = emoji[1]
    output_file.write(write_define_str(name, hex_code) + "\n")

    # shortname is found by taking substring which excludes opening and ending colon, uppercasing, and removing spaces
    shortname = unicode_hash[emoji[0]][1:-1].upper().replace(" ", "_")

    # replace manually, just easier than using and retaining delimiter
    shortname = "COLON_" + shortname + "_COLON"

    output_file.write(write_define_num(shortname, name))
    # newline between each pair of lines
    output_file.write("\n\n")






