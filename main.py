import http.client
from os import access
import ast
import csv
from queue import PriorityQueue


def initiate_connection():
    conn = http.client.HTTPSConnection('api.linkedin.com')

    return conn


def authentication(conn, client_id, client_secret):
    client_id = ''
    client_secret = ''
    data = f'grant_type=client_credentials&client_id={client_id}&client_secret={client_secret}'

    conn.request('POST', 'api.linkedin.com/oauth/v2/accessToken',
                 body=data,
                 headers={'Content-Type': 'application/x-www-form-urlencoded'})

    response = conn.getresponse()

    if response.status != 200:
        raise http.client.HTTPException(response.read().decode("utf-8"))

    token = ast.literal_eval(response.read().decode(
        "UTF-8")).get('access_token', None)

    return token

def define_csv_header():
    with open(file_name, 'a', encoding='utf-8') as writer:
        csv_writer = csv.writer(writer)
        csv_writer.writerow(['title', 'description', 'URL', 'categorization', 'urn'])

def write_data_into_csv(response_dict: dict):
    with open(file_name, 'a', encoding='utf-8') as writer:
        csv_writer = csv.writer(writer)
        for el in response_dict['elements']:
            csv_row = format_data(el)
            csv_writer.writerow(csv_row)


def format_data(el:dict) -> str:
    values: list = []
    values.append(el['title']['value'])
    values.append(el['details']['description']['value'])
    values.append(el['details']['urls']['webLaunch'])
    values.append(el['detais']['classifications'][0]['associatedClassification']['name']['value'])
    values.append(el['urn'])

    return values



def fetch_data(conn, token):
    # df.append()
    params = 'q=localeAndType&assetType=COURSE&sourceLocale.language=en&sourceLocale.country=US&expandDepth=1&includeRetired=false&start=0&count=100'
    href = f'/v2/learningAssets?{params}'
    while href:
        conn.request('GET', f'api.linkedin.com/{href}', headers={
                    'Authorization': f'Bearer {token}'})

        response: bytes = conn.getresponse()

        response_dict: dict = ast.literal_eval(response.read().decode('utf-8'))
        
        write_data_into_csv(response_dict)

        href = None
        for link in response_dict['paging']['links']:
            if link['rel'] == 'next':
                href = link['href']
                break

def dijkstra(self, start_vertex):
    D = {v:float('inf') for v in range(self.v)}
    D[start_vertex] = 0

    pq = PriorityQueue()
    pq.put((0, start_vertex))

    while not pq.empty():
        (dist, current_vertex) = pq.get()
        self.visited.append(current_vertex)

        for neighbor in range(self.v):
            if self.edges[current_vertex][neighbor] != -1:
                distance = self.edges[current_vertex][neighbor]
                if neighbor not in self.visited:
                    old_cost = D[neighbor]
                    new_cost = D[current_vertex] + distance
                    if new_cost < old_cost:
                        pq.put((new_cost, neighbor))
                        D[neighbor] = new_cost
    return D

if __name__ == "__main__":
    client_id = ''
    client_secret = ''
    file_name = 'export.csv'
    conn = initiate_connection()

    token = authentication(conn, client_id, client_secret)

    define_csv_header()
    fetch_data(conn, token)
