import re
import pandas as pd

raw_text = """
12:00 PM	124 New Mexico St. at 163 FIU ESPN+	FIU -0.9 79-78 (53%)	63	
02:00 PM	0 Alfred St. at 158 Cornell ESPN+	Cornell (100%)	0	
03:00 PM	291 Mount St. Mary's at 259 Merrimack ESPN+	Merrimack -5.3 71-65 (71%)	32	
04:00 PM	273 Fairfield at 347 Canisius ESPN+	Fairfield -2.4 68-66 (60%)	33	
04:00 PM	306 Sacred Heart at 357 Niagara ESPN+	Sacred Heart -2.7 71-68 (61%)	28	
05:00 PM	144 Sam Houston St. at 152 Western Kentucky ESPN+	Western Kentucky -3.5 85-81 (62%)	59	
07:00 PM	39 USC at 1 Michigan Peacock	Michigan -22.6 98-75 (95%)	75	
07:00 PM	173 Robert Morris at 243 Detroit Mercy ESPN+	Robert Morris -0.3 76-75 (51%)	54	
07:00 PM	161 Siena at 164 Iona ESPN+	Iona -3.6 74-71 (64%)	53	
07:00 PM	160 Kennesaw St. at 105 Liberty ESPNU	Liberty -8.9 82-73 (79%)	47	
07:00 PM	224 Jacksonville St. at 285 Delaware ESPN+	Delaware -0.1 64-63 (50%)	45	
07:00 PM	151 Marist at 286 Saint Peter's ESPN+	Marist -3.5 66-62 (65%)	42	
07:00 PM	264 Wagner at 333 Chicago St. NEC Front Row	Wagner -0.8 74-73 (53%)	42	
07:00 PM	130 Quinnipiac at 300 Manhattan ESPN+	Quinnipiac -7.4 84-77 (74%)	41	
07:00 PM	234 Lamar at 76 McNeese St. CBSSN	McNeese St. -16.3 77-61 (92%)	35	
07:00 PM	292 Le Moyne at 355 Saint Francis NEC Front Row	Le Moyne -3.0 81-78 (61%)	34	
07:00 PM	302 Central Connecticut at 210 LIU NEC Front Row	LIU -9.4 79-69 (81%)	29	
07:00 PM	344 New Haven at 341 Stonehill NEC Front Row	Stonehill -3.3 64-61 (65%)	25	
07:30 PM	62 Oregon at 111 Maryland Peacock	Oregon -0.9 76-75 (53%)	71	
07:30 PM	178 Louisiana Tech at 117 Middle Tennessee ESPN+	Middle Tennessee -7.0 66-59 (78%)	40	
07:30 PM	354 Fairleigh Dickinson at 321 Mercyhurst NEC Front Row	Mercyhurst -7.8 72-64 (79%)	15	
08:00 PM	11 Louisville at 82 Stanford ACC Network	Louisville -8.8 85-76 (78%)	71	
08:00 PM	37 Ohio St. at 192 Rutgers Peacock	Ohio St. -10.2 79-68 (83%)	48	
08:00 PM	232 UTEP at 215 Missouri St. ESPN+	Missouri St. -4.1 66-62 (68%)	38	
09:00 PM	16 Michigan St. at 26 Nebraska Peacock	Nebraska -1.0 72-71 (54%)	88	
09:00 PM	54 West Virginia at 8 Iowa St. ESPN2	Iowa St. -13.8 77-63 (91%)	61	
09:00 PM	107 Seattle at 5 Gonzaga ESPN+	Gonzaga -21.7 87-65 (96%)	57	
09:30 PM	126 Loyola Marymount at 153 Washington St. ESPN+	Washington St. -1.6 70-69 (57%)	58	
10:00 PM	171 Oregon St. at 143 Pacific ESPN+	Pacific -5.4 71-66 (71%)	44	
10:00 PM	220 Portland at 28 Saint Mary's ESPN+	Saint Mary's -23.4 86-62 (96%)	40	
10:00 PM	196 San Diego at 93 San Francisco ESPN+	San Francisco -12.7 80-67 (86%)	39	
10:00 PM	265 Pepperdine at 43 Santa Clara ESPN+	Santa Clara -23.7 86-62 (96%)	35	
11:00 PM	70 Notre Dame at 78 California ESPN2	California -3.0 70-67 (62%)	65	
"""

rows = []

for line in raw_text.strip().split("\n"):
    # Extract matchup
    matchup_match = re.search(r"\d+\s+(.*?)\s+at\s+\d+\s+(.*?)\s+(ESPN\+|Peacock|ESPNU|CBSSN|ACC Network|ESPN2|NEC Front Row)", line)
    if not matchup_match:
        continue

    away_team = matchup_match.group(1)
    home_team = matchup_match.group(2)

    # Extract spread and projected score
    line_match = re.search(r"([A-Za-z .']+)\s+(-?\d+\.\d)\s+(\d+)-(\d+)", line)

    if line_match:
        spread = float(line_match.group(2))
        total = int(line_match.group(3)) + int(line_match.group(4))
    else:
        # Games with no spread/score projection
        spread = None
        total = None

    rows.append({
        "home_team": home_team,
        "away_team": away_team,
        "projected_spread": spread,
        "projected_total": total
    })

df = pd.DataFrame(rows)
df.to_csv('lines.csv', index=True)
print(df)