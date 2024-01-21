#include "sierrachart.h"
#include <string>
#include <fstream>
#include <sstream>
#include <map>

SCDLLName("CSV_LEVEL_IMPORTER")

/*
	Written by Ashton
 	@shlekht on discord
*/


struct DrawingData {
	// make sure csv follows this format
	float Price;
	std::string Color;
	int LineType; // 1 - 6
	int LineWidth;
	int TextAlignment; // 1 or 2
	std::string DateTime; // THIS FORMAT >> YYYY/MM/DD/HH/MM/SS 
						  // all in one string for easy manipulation
};

enum ColorCodes {
	eRed,
	eGreen,
	eBlue,
	eWhite,
	eBlack,
	ePurple,
	ePink,
	eYellow,
	eGold,
	eBrown,
	eCyan,
	eGray
};

SCSFExport scsf_CsvLevelImporter(SCStudyInterfaceRef sc)
{
	SCInputRef filePath = sc.Input[0];
	
	if (sc.SetDefaults)
	{
		sc.GraphName = "CSV Level Importer";

		sc.AutoLoop = 1; 
		sc.GraphRegion = 0;
		
		filePath.Name = "CSV File Path";
		filePath.SetPathAndFileName("C:\\Users\\*****\\OneDrive\\Desktop\\CSV_LEVELS_TEST.csv");
		
		return;
	}
	
	std::vector<DrawingData>* Drawings = (std::vector<DrawingData>*)sc.GetPersistentPointer(0);
	
	
	if (sc.LastCallToFunction) {
		Drawings->clear();
		delete Drawings;
		sc.SetPersistentPointer(0, NULL);
		return;
	}
	
	if (Drawings == NULL) {
		Drawings = new std::vector<DrawingData>;
		sc.SetPersistentPointer(0, Drawings);
	}
	
	if (sc.Index == 0 && sc.IsFullRecalculation) {
		Drawings->clear();
		
		std::ifstream file;
		std::string line = "";
		std::string garbage = ""; // using this to skip first line which is random header stuff
		
		file.open(filePath.GetPathAndFileName());
		getline(file, garbage);
		while(getline(file, line)) {
			// handling empty rows from excel
			if (line.find_first_not_of(", \t") == std::string::npos) {
				continue;
			}
			
			// create object to store data
			DrawingData s_Line;
			
			std::string temp = "";
			std::stringstream inputString(line);
			
			//price
			getline(inputString, temp, ',');
			s_Line.Price = atof(temp.c_str());
			
			//color
			getline(inputString, s_Line.Color, ',');
			
			// line style
			getline(inputString, temp, ',');
			s_Line.LineType = atoi(temp.c_str());
			
			// line width
			getline(inputString, temp, ',');
			s_Line.LineWidth = atoi(temp.c_str());
			
			// text alignment
			getline(inputString, temp, ',');
			s_Line.TextAlignment = atoi(temp.c_str());
			
			// date
			getline(inputString, s_Line.DateTime, ',');
			
			Drawings->push_back(s_Line);
			
			line = "";
		}
		
		file.close();
		
		for (auto it = Drawings->begin(); it != Drawings->end(); ++it) {
			// iterator in this case is == to a struct object holding our drawing data
			s_UseTool Tool;
			Tool.AddMethod = UTAM_ADD_OR_ADJUST;
			Tool.DrawingType = DRAWING_HORIZONTAL_RAY;
			Tool.BeginValue = it->Price;
			
			std::map<std::string, ColorCodes> mapColorCodes = {
				{"red", eRed},
				{"green", eGreen},
				{"blue", eBlue},
				{"white", eWhite},
				{"black", eBlack},
				{"purple", ePurple},
				{"pink", ePink},
				{"yellow", eYellow},
				{"gold", eGold},
				{"brown", eBrown},
				{"cyan", eCyan},
				{"gray", eGray}
			};
			
			
			// color
			switch (mapColorCodes[it->Color]) {
				case eRed:
					Tool.Color = COLOR_RED;
					break;
				case eCyan:
					Tool.Color = COLOR_CYAN;
					break;
				case eGreen:
					Tool.Color = COLOR_GREEN;
					break;
				case eBlue:
					Tool.Color = COLOR_BLUE;
					break;
				case eBlack:
					Tool.Color = COLOR_BLACK;
					break;
				case ePurple:
					Tool.Color = COLOR_PURPLE;
					break;
				case ePink:
					Tool.Color = COLOR_PINK;
					break;
				case eYellow:
					Tool.Color = COLOR_YELLOW;
					break;
				case eGold:
					Tool.Color = COLOR_GOLD;
					break;
				case eGray:
					Tool.Color = COLOR_GRAY;
					break;
				default:
					Tool.Color = COLOR_WHITE;
			}
			
			// linestyle
			switch (it->LineType) {
				case 2:
					Tool.LineStyle = LINESTYLE_DASH;
					break;
				case 3:
					Tool.LineStyle = LINESTYLE_DOT;
					break;
				case 4:
					Tool.LineStyle = LINESTYLE_DASHDOT;
					break;
				case 5:
					Tool.LineStyle = LINESTYLE_DASHDOTDOT;
					break;
				case 6:
					Tool.LineStyle = LINESTYLE_ALTERNATE;
					break;
				default:
					Tool.LineStyle = LINESTYLE_SOLID;
			
			}
			
			Tool.LineWidth = it->LineWidth;
			
			switch (it->TextAlignment) {
				case 2:
					Tool.TextAlignment = DT_LEFT;
					break;
				default:
					Tool.TextAlignment = DT_RIGHT;
			}
			
			// time to handle the date time and parse the input
			SCDateTime dateTime;
			std::vector<char*> tokens;
			
			char* cstr = new char[it->DateTime.size() + 1];
			std::strcpy(cstr, it->DateTime.c_str());
			char* t = std::strtok(cstr, "/");
			while (t != NULL) {
				tokens.push_back(t);
				t = strtok(NULL, "/");
			}
			
			dateTime.SetDateTimeYMDHMS(
				atoi(tokens[0]),
				atoi(tokens[1]),
				atoi(tokens[2]),
				atoi(tokens[3]),
				atoi(tokens[4]),
				atoi(tokens[5])
			);
			
			Tool.BeginIndex = sc.GetNearestMatchForSCDateTime(sc.ChartNumber, dateTime);
			sc.UseTool(Tool);

			delete[] cstr;
		}
	}
}
