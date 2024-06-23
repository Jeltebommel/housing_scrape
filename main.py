from search import Search

if __name__ == "__main__":
    search = Search(
        city='barcelona--spain',
        move_in='2024-06-23',
        move_out='2024-07-29',
        budget='1000',
        property_type='apartments',
        bedrooms='2'
    )
    search.execute()
    for result in search.results:
        print(result)

