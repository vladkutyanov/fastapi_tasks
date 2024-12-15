from fastapi import Body, Depends, FastAPI, Query
import uvicorn

app = FastAPI()

hotels = [
    {"id": 1, "title": "Sochi", "name": "sochi"},
    {"id": 2, "title": "Dubai", "name": "dubai"}
]




@app.get("/hotels")
def get_hotels(
    id: int | None = Query(None, description = 'Айдишник'),
    title: str | None = Query(None, description = 'Название отеля'),
):
    hotels_ = []
    
    for hotel in hotels:
        if id and hotel["id"] != id:
            continue
        if title and hotel["title"] != title:
            continue
        hotels_.append(hotel)
    return hotels_


@app.delete("/hotels/{hotel_id}")
def delete_hotel(
    hotel_id: int
):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": "OK"}


@app.post("/hotels")
def create_hotel(
    title: str = Body(embed = True)
):
    global hotels
    hotels.append({
        "id": hotels[-1]["id"] + 1,
        "title": title
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


@app.put("/hotels/{hotel_id}")
def put_hotel(
    hotel_id: int,
    title: str = Query(description = "Название отеля заглавное"),
    name: str = Query(description = "Название отеля обычное")
):
    global hotels 
    return update_hotels(hotels, hotel_id, title, name, method = "PUT")


@app.patch("/hotels/{hotel_id}")
def patch_hotel(
    hotel_id: int,
    title: str | None = Query(None, description = "Название отеля заглавное"),
    name: str | None =  Query(None, description = "Название отеля обычное")
):
    global hotels
    return update_hotels(hotels, hotel_id, title, name, method = "PATCH")



if __name__ == "__main__":
    uvicorn.run("main:app", host = "127.0.01", port = 8000, reload = True)