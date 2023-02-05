def get_queries(filename):
    with open(filename, 'r') as f:
        queries = f.readlines()
    return [query.split(",")[0].strip() for query in queries]

# test the function
queries = get_queries('businesses.csv')
print(queries)