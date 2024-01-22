csv_importer.cpp documentation:

This study lets you draw horizontal rays on the chart based on data from a csv\n

The csv needs to have the following format:\n
Price (float)| Color (string)| LineStyle (int)| LineWidth (int)| TextAlignment (int)| DateTime (string)\n

Available colors:\n
red, green, blue, white, black, purple, pink, yellow, gold, brown, cyan, gray\n

LineStyles are integers ranging 1 - 6:\n
Solid, Dash, Dot, DashDot, DashDotDot, Alternate\n

Linewdith is pretty self-explanatory\n

TextAlignment is either 1 or 2:\n
Aligned to the left, Aligned to the right\n

DateTime:\n
Custom formated string with the following format >> YYYY/MM/DD/HH/MM/SS\n
Very important that that exact format is followed or the rays will be drawn from the very first bar on the chart instead of the correct time\n

TODO:\n
Add the option for rectangles if given two price points\n
Add the option to have notes be displayed\n
Add the option to cut the drawing off after price touches the line\n


