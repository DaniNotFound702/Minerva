from .api import ZermeloAPIClient

def get_year_id(api_client: ZermeloAPIClient):
    if not isinstance(api_client, ZermeloAPIClient):
        raise TypeError("api_client must be a ZermeloAPIClient instance")
    fields = ("year", "id")

    data = api_client.get_endpoint("schoolsinschoolyears", "fields=" + ",".join(fields))
    rows = data
    year_id = {}
    for row in rows:
        year_id[row["year"]] = row["id"]

    startYear = rows[0]["year"]
    endYear = rows[-1]["year"]

    return startYear, endYear, year_id
 
def convert_id_to_year(api_client: ZermeloAPIClient, school_year_id: int):
    if not isinstance(api_client, ZermeloAPIClient):
        raise TypeError("api_client must be a ZermeloAPIClient instance")
    if not isinstance(school_year_id, int):
        raise TypeError("school_year_id must be an integer")

    fields = ("archived", "archivedTime", "id", "name", "school","year")
    data = api_client.get_endpoint("schoolsinschoolyears","id=" + str(school_year_id) + "&fields=" + ",".join(fields))
    return data[0]['year']