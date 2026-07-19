# coding=utf-8

estate_color_dict = {'cosmic': "#b7cece", 'spiritual': "#89408c", 'terrestrial': "#583e23"}
element_color_dict = {'fire': "#e03c13", 'water': "#61b5ff", 'earth': "#7b7554", 'air': "#efd28d"}
season_color_dict = {'winter': "#43acc7", 'spring': "#0d5945", 'summer': "#edd892", 'autumn': "#dd8c61"}

current_cycle = 0
name_of_calendar = "Age of Awakening"

# CONJ Table Structure, index is the step, returned list is the indices of the houses
CONJ_MERCURY = [{0, 1, 2, 3}, {0, 1, 2, 3}, {0, 1, 2, 3}, {0, 1, 2, 3}, {1, 2, 3, 4}, {1, 2, 3, 4}, {1, 2, 3, 4},
                {1, 2, 3, 4}, {2, 3, 4, 5}, {2, 3, 4, 5}, {2, 3, 4, 5}, {2, 3, 4, 5}, {3, 4, 5, 6}, {3, 4, 5, 6},
                {3, 4, 5, 6}, {3, 4, 5, 6}, {4, 5, 6, 7}, {4, 5, 6, 7}, {4, 5, 6, 7}, {4, 5, 6, 7}, {8, 5, 6, 7},
                {8, 5, 6, 7}, {8, 5, 6, 7}, {8, 5, 6, 7}, {8, 9, 6, 7}, {8, 9, 6, 7}, {8, 9, 6, 7}, {8, 9, 6, 7},
                {8, 9, 10, 7}, {8, 9, 10, 7}, {8, 9, 10, 7}, {8, 9, 10, 7}, {8, 9, 10, 11}, {8, 9, 10, 11},
                {8, 9, 10, 11}, {8, 9, 10, 11}, {0, 9, 10, 11}, {0, 9, 10, 11}, {0, 9, 10, 11}, {0, 9, 10, 11},
                {0, 1, 10, 11}, {0, 1, 10, 11}, {0, 1, 10, 11}, {0, 1, 10, 11}, {0, 1, 2, 11}, {0, 1, 2, 11},
                {0, 1, 2, 11}, {0, 1, 2, 11}]
CONJ_VENUS = [{0, 1, 2}, {0, 1, 2}, {0, 1, 2}, {0, 1, 2}, {1, 2, 3}, {1, 2, 3}, {1, 2, 3}, {1, 2, 3}, {2, 3, 4},
              {2, 3, 4}, {2, 3, 4}, {2, 3, 4}, {3, 4, 5}, {3, 4, 5}, {3, 4, 5}, {3, 4, 5}, {4, 5, 6}, {4, 5, 6},
              {4, 5, 6}, {4, 5, 6}, {5, 6, 7}, {5, 6, 7}, {5, 6, 7}, {5, 6, 7}, {8, 6, 7}, {8, 6, 7}, {8, 6, 7},
              {8, 6, 7}, {8, 9, 7}, {8, 9, 7}, {8, 9, 7}, {8, 9, 7}, {8, 9, 10}, {8, 9, 10}, {8, 9, 10}, {8, 9, 10},
              {9, 10, 11}, {9, 10, 11}, {9, 10, 11}, {9, 10, 11}, {0, 10, 11}, {0, 10, 11}, {0, 10, 11}, {0, 10, 11},
              {0, 1, 11}, {0, 1, 11}, {0, 1, 11}, {0, 1, 11}]
CONJ_MARS = [{0, 1}, {0, 1}, {0, 1}, {0, 1}, {1, 2}, {1, 2}, {1, 2}, {1, 2}, {2, 3}, {2, 3}, {2, 3}, {2, 3}, {3, 4},
             {3, 4}, {3, 4}, {3, 4}, {4, 5}, {4, 5}, {4, 5}, {4, 5}, {5, 6}, {5, 6}, {5, 6}, {5, 6}, {6, 7}, {6, 7},
             {6, 7}, {6, 7}, {8, 7}, {8, 7}, {8, 7}, {8, 7}, {8, 9}, {8, 9}, {8, 9}, {8, 9}, {9, 10}, {9, 10}, {9, 10},
             {9, 10}, {10, 11}, {10, 11}, {10, 11}, {10, 11}, {0, 11}, {0, 11}, {0, 11}, {0, 11}]
CONJ_JUPITER = [{0}, {0}, {0, 1}, {0, 1}, {1}, {1}, {1, 2}, {1, 2}, {2}, {2}, {2, 3}, {2, 3}, {3}, {3}, {3, 4}, {3, 4},
                {4}, {4}, {4, 5}, {4, 5}, {5}, {5}, {5, 6}, {5, 6}, {6}, {6}, {6, 7}, {6, 7}, {7}, {7}, {8, 7}, {8, 7},
                {8}, {8}, {8, 9}, {8, 9}, {9}, {9}, {9, 10}, {9, 10}, {10}, {10}, {10, 11}, {10, 11}, {11}, {11},
                {0, 11}, {0, 11}]
CONJ_SOL = [{0}, {1}, {2}, {3}, {4}, {5}, {6}, {7}, {8}, {9}, {10}, {11}]
CONJ_SATURN = [{0}, {0}, {0, 1}, {1}, {1}, {1, 2}, {2}, {2}, {2, 3}, {3}, {3}, {3, 4}, {4}, {4}, {4, 5}, {5}, {5},
               {5, 6}, {6}, {6}, {6, 7}, {7}, {7}, {7, 8}, {8}, {8}, {8, 9}, {9}, {9}, {9, 10}, {10}, {10}, {10, 11},
               {11}, {11}, {0, 11}]
CONJ_MARK = "\u260C"

MERCURY = '\u263F'
VENUS = '\u2640'
MARS = '\u2642'
JUPITER = '\u2643'
SATURN = '\u2644'
SOL = '\u2609'
SALT = '\U0001F714'

SUN_SIGN = '\u2609'
MOON_SIGN = '\u263E'
RISING_SIGN = '\u260A'

SIGNS = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 'Libra', 'Scorpio', 'Sagittarius', 'Capricorn',
         'Aquarius', 'Pisces']

moonphases = ["./resources/svg/new_moon.svg", "./resources/svg/visions.svg", "./resources/svg/planning.svg",
              "./resources/svg/story.svg", "./resources/svg/meeting.svg", "./resources/svg/quiet.svg"]
html = ["./resources/html/new_moon.html", "./resources/html/visions.html", "./resources/html/planning.html",
        "./resources/html/story.html", "./resources/html/meeting.html", "./resources/html/quiet.html"]


def sectors_covered_by_arc_snap_points(
        start_snap_point: int,
        arc_snap_points: int,
        snap_points_circle: int,
        sectors: int = 12,
) -> set[int]:
    """
    Arc includes snap points: start, start+1, ..., start+arc_snap_points-1 (inclusive),
    wrapping modulo snap_points_circle.

    A sector counts if at least one snap point in that arc falls inside it.
    Sector index mapping:
        sector(i) = floor( (i * sectors) / snap_points_circle )
    """
    if arc_snap_points <= 0 or snap_points_circle <= 0 or sectors <= 0:
        return set()

    n = snap_points_circle
    start = start_snap_point % n

    covered = set()
    for k in range(arc_snap_points):
        i = (start + k) % n
        sector = (i * sectors) // n
        if 0 <= sector < sectors:
            covered.add(sector)
    return covered


print("Mercury")
mercury_list = []
index = 0
while index < 48:
    mercury_list.append(sectors_covered_by_arc_snap_points(index, 13, 48))
    # print(sectors_covered_by_arc_snap_points(index,13,48))
    index += 1
print(mercury_list)

print("Venus")
venus_list = []
index = 0
while index < 48:
    venus_list.append(sectors_covered_by_arc_snap_points(index, 9, 48))
    # print(sectors_covered_by_arc_snap_points(index,13,48))
    index += 1
print(venus_list)

print("Mars")
mars_list = []
index = 0
while index < 48:
    mars_list.append(sectors_covered_by_arc_snap_points(index, 5, 48))
    # print(sectors_covered_by_arc_snap_points(index,13,48))
    index += 1
print(mars_list)

print("Jupiter")
jupiter_list = []
index = 0
while index < 48:
    jupiter_list.append(sectors_covered_by_arc_snap_points(index, 3, 48))
    # print(sectors_covered_by_arc_snap_points(index,13,48))
    index += 1
print(jupiter_list)
