from fastapi import Body, Depends, FastAPI, Query, APIRouter
from schemas.hotels import Hotel, HotelPatch


router = APIRouter(prefix = "/hotels", tags = ["Отели"])

hotels = [
    {"id": 1, "title": "Sochi", "name": "sochi"},
    {"id": 2, "title": "Дубай", "name": "dubai"},
    {"id": 3, "title": "Мальдивы", "name": "maldivi"},
    {"id": 4, "title": "Геленджик", "name": "gelendzhik"},
    {"id": 5, "title": "Москва", "name": "moscow"},
    {"id": 6, "title": "Казань", "name": "kazan"},
    {"id": 7, "title": "Санкт-Петербург", "name": "spb"},
]





@router.get("")
def get_hotels(
    id: int | None = Query(None, description = 'Айдишник'),
    title: str | None = Query(None, description = 'Название отеля'),
    page: int | None = Query(None),
    per_page: int | None = Query(None)
):
    hotels_ = []
    
    if page is None:
        page = 1
    if per_page is None:
        per_page = 3
    left = (page-1)*per_page
    right = (page)*per_page
    
    for hotel in hotels[left:right]:
        if id and hotel["id"] != id:
            continue
        if title and hotel["title"] != title:
            continue
        hotels_.append(hotel)
    return hotels_


@router.delete("/{hotel_id}")
def delete_hotel(
    hotel_id: int
):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": "OK"}


@router.post("")
def create_hotel(
    hotel_data: Hotel
):
    global hotels
    hotels.append({
        "id": hotels[-1]["id"] + 1,
        "title": Hotel.title,
        "name": Hotel.name
    })
    return {"status": "OK"}


def update_hotels(
    hotels: list,
    hotel_id: int,
    title: str,
    name: str,
    method: str
) -> dict:
    if method == "PUT" and (title is None or name is None):
        return {"status": "Error! Provide both title and name"}
    
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            if title is not None:
                hotel["title"] = title
            if name is not None:
                hotel["name"] = name
    return {"status": "OK"}


@router.put("/{hotel_id}")
def put_hotel(
    hotel_id: int,
    hotel_data: Hotel
):
    global hotels 
    return update_hotels(hotels, hotel_id, hotel_data.title, hotel_data.name, method = "PUT")


@router.patch("/{hotel_id}")
def patch_hotel(
    hotel_id: int,
    hotel_data: HotelPatch
):
    global hotels
    return update_hotels(hotels, hotel_id, hotel_data.title, hotel_data.name, method = "PATCH")