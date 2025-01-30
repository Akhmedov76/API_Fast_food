# import asyncio
# from geolocation import get_coordinates_from_address
# from distance_calculation import calculate_distance, calculate_time
#
#
# async def calculate_delivery_time(address1, address2, num_of_dishes):
#     coords1 = await get_coordinates_from_address(address1)
#     coords2 = await get_coordinates_from_address(address2)
#
#     if coords1 and coords2:
#         lat1, lon1 = coords1
#         lat2, lon2 = coords2
#
#         distance = calculate_distance(lat1, lon1, lat2, lon2)
#
#         total_time = calculate_time(distance, num_of_dishes)
#
#         return f"Masofa: {distance:.2f} km, Vaqt: {total_time:.2f} minut"
#     return "Manzil topilmadi"
#
#
# async def main():
#     address1 = "Yunusabad, Tashkent"
#     address2 = "Chorsu, Tashkent"
#     num_of_dishes = 12
#     result = await calculate_delivery_time(address1, address2, num_of_dishes)
#     print(result)
#
#
# asyncio.run(main())
