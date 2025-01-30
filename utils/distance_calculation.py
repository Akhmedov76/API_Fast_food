# from math import radians, sin, cos, sqrt, atan2
#
#
# def calculate_distance(lat1, lon1, lat2, lon2):
#     R = 6371.0
#
#     lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
#
#     dlon = lon2 - lon1
#     dlat = lat2 - lat1
#
#     a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
#     c = 2 * atan2(sqrt(a), sqrt(1 - a))
#
#     distance = R * c
#     return distance
#
#
# def calculate_time(distance, num_of_dishes):
#     prepare_time = (num_of_dishes / 4) * 5
#
#     delivery_time = distance * 3
#
#     total_time = prepare_time + delivery_time
#     return total_time
