from search import Search

if __name__ == "__main__":
    search = Search(city='Madrid', availability='2021-09-01', budget='1000', property_type='apartment')
    search.execute()
    print(search.results)
