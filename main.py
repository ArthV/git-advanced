import http.client
from os import access
import ast
import csv
from  math import ceil, sqrt

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
def bsgs(g, h, p):
    '''
    Solve for x in h = g^x mod p given a prime p.
    If p is not prime, you shouldn't use BSGS anyway.
    '''
    N = ceil(sqrt(p - 1))  # phi(p) is p-1 if p is prime

    # Store hashmap of g^{1...m} (mod p). Baby step.
    tbl = {pow(g, i, p): i for i in range(N)}

    # Precompute via Fermat's Little Theorem
    c = pow(g, N * (p - 2), p)

    # Search for an equivalence in the table. Giant step.
    for j in range(N):
        y = (h * pow(c, j, p)) % p
        if y in tbl:
            return j * N + tbl[y]

    # Solution not found
    return None

def rshor(a, P):
    """recherche de la période r de la fonction f=pow(a,k,P)"""
 
    # calcul des premières valeurs de f(a,k,P) avec k de 1 à imax-1:
    M = [1] # car on sait que pow(a,0,P) = 1
    imax = 10000  # taille du motif de départ M
    for k in xrange(1, imax):
        f = pow(a, k, P)
        if f == 1:
            return k # on a trouvé la période r=k
        M.append(f)
 
    # définir un pas
    pas = (P-imax)//100000
    if pas<1:
        pas = 1
 
    k = imax
    while k<P:
        f = pow(a, k, P) # on calcule la valeur de f correspondante
        i = -1
        while True:
            try:
                i = M.index(f,i+1) # on cherche si f(k) se trouve dans le motif de départ
            except:
                break  # non, on passe au k suivant
 
            if pow(a,k-i,P)==1:
                r = k-i  # on a trouvé la période ou un multiple de la période
 
                # tentative de trouver un r plus petit si c'est un multiple de la période
                for j in xrange(10, 1, -1):
                    if r%j==0:
                        k = r//j
                        if pow(a,k,P)==1:
                            return k
 
                return r
        k += pas
    return 0  # c'est une condition d'échec: on n'a pas trouvé de r qui convienne

if __name__ == "__main__":
    client_id = ''
    client_secret = ''
    file_name = 'export.csv'
    conn = initiate_connection()

    token = authentication(conn, client_id, client_secret)

    define_csv_header()
    fetch_data(conn, token)
