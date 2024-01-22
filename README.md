csv_importer.cpp documentation:

This study lets you draw horizontal rays on the chart based on data from a csv\n

The csv needs to have the following format:  
Price (float)| Color (string)| LineStyle (int)| LineWidth (int)| TextAlignment (int)| DateTime (string)  

Available colors:  
red, green, blue, white, black, purple, pink, yellow, gold, brown, cyan, gray  

LineStyles are integers ranging 1 - 6:  
Solid, Dash, Dot, DashDot, DashDotDot, Alternate  

Linewdith is pretty self-explanatory  

TextAlignment is either 1 or 2:  
Aligned to the left, Aligned to the right  

DateTime:  
Custom formated string with the following format >> YYYY/MM/DD/HH/MM/SS  
Very important that that exact format is followed or the rays will be drawn from the very first bar on the chart instead of the correct time  

TODO:  
Add the option for rectangles if given two price points  
Add the option to have notes be displayed  
Add the option to cut the drawing off after price touches the line  


