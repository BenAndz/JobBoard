from fastapi import HTTPException, status, Depends # utilisé pour gérer les exceptions HTTP et les dépendances (fonction écrite une fois et qui peut être réutilisée dans différentes parties de l'application) dans FastAPI
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm # utilisés pour implémenter l'authentification OAuth2 avec mot de passe
from jose import JWTError, jwt # Utilisés pour gérer les erreurs liées aux tokens JWT et pour créer/valider ces tokens.
from datetime import datetime, timedelta # Utilisés pour gérer les dates et les durées, notamment pour définir la durée de vie des tokens.
from db.models import TokenData # Un modèle Pydantic pour les données du token.
from db.session import get_db_connection # Une fonction pour obtenir une connexion à la base de données.

# SERVICE D'AUTHENTIFICATION AVEC TOKEN

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token") # classe fournie par FastAPI, tokenUrl="token" indique l'URL où le frontend enverra les données d'identification de l'utilisateur pour obtenir un token.OAuth2PasswordBearer: c'est une classe de FastAPI qui implémente le schéma d'authentification OAuth 2.0 "Password Flow". Ce schéma est souvent utilisé pour les applications qui ont un serveur backend et un client frontend, où les utilisateurs se connectent avec un nom d'utilisateur et un mot de passe.
# la varibale oauth2_scheme permettra d'obtenir le token envoyé par le client (frontend). Il s'attend à ce que le token soit inclus dans un en-tête d'autorisation avec le préfixe "Bearer"
# tokenUrl="token": l'argument tokenUrl spécifie l'URL où le client peut envoyer une requête POST pour obtenir un token JWT en échange de ses identifiants (nom d'utilisateur et mot de passe). Dans ce cas, l'URL est définie sur "token", ce qui signifie que vous devez avoir un endpoint dans votre API qui traite les requêtes POST à l'URL "/token" pour générer et renvoyer des tokens JWT.
# oauth2_scheme est une instance de OAuth2PasswordBearer qui aide à gérer l'authentification en utilisant le schéma "Password Flow" d'OAuth 2.0. 
# Il attend que le token JWT soit envoyé dans les en-têtes de la requête HTTP avec le préfixe "Bearer".
# Il rend le token JWT facilement accessible dans les fonctions et dépendances FastAPI.

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
# clé secrète utilisée pour signer les tokens JWT. Elle garantit que le token a été créé par le serveur (parce qu'il détient la clé secrète) et n'a pas été modifié.

ALGORITHM = "HS256"
# spécifie l'algorithme utilisé pour signer les tokens JWT (Json Web Tokens)
# "HS256" signifie "HMAC avec SHA-256". HMAC est un mécanisme d'authentification basé sur un hash, et SHA-256 est l'algorithme de hachage utilisé. Choix courant et sécurisé pour la signature des tokens JWT.

ACCESS_TOKEN_EXPIRE_MINUTES = 30
# détermine la durée de vie des tokens ; après ce délai, le token expirera ; bonne pratique en matière de sécurité

def get_user(email: str):
    with get_db_connection() as conn:
        cursor = conn.cursor(dictionary=True) # l'argument dictionary=True signifie que les résultats renvoyés seront sous forme de dictionnaires, où les clés sont les noms des colonnes et les valeurs sont les données de chaque colonne.
        query = "SELECT * FROM people WHERE email=%s"
        cursor.execute(query, (email,))
        user = cursor.fetchone() # cette ligne récupère le premier résultat (s'il existe) et le stocke dans la variable user.
        cursor.close()
        return user
    
def create_access_token(data: dict, expires_delta: timedelta = None): # cette ligne définit une fonction create_access_token qui prend deux paramètres : data (un dictionnaire) et expires_delta (un objet timedelta qui est optionnel et a une valeur par défaut de None).
    to_encode = data.copy() # creé une copie de data afin d'éviter des pb avec plusieurs utilisations
    user = get_user(email=data.get("sub")) # appelle la fonction get_user en passant la valeur associée à la clé "sub" dans le dictionnaire data comme argument. Cette fonction renvoie les informations de l'utilisateur correspondant à cet email, et le résultat est stocké dans la variable user. "Email" devient la valeur de la clé "sub"
    print(f"User de la DB : {user.get('role')}")
    if user and "role" in user:
        to_encode["role"] = user["role"] # dictionnaire qui contient les informations d'un utilisateur récupérées de la base de données. La clé "role" est utilisée pour accéder à la valeur du rôle de cet utilisateur. Par exemple, si user est {"name": "Alice", "email": "alice@example.com", "role": "admin"}, alors user["role"] donnera "admin".
        # to_encode["role"] = user["role"] : Cette expression ajoute une nouvelle paire clé-valeur au dictionnaire to_encode, où la clé est "role" et la valeur est le rôle de l'utilisateur récupéré à l'étape précédente. Si le rôle de l'utilisateur est "admin", cela revient à faire to_encode["role"] = "admin".
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=30)
    
    to_encode.update({"exp": expire}) # {"exp": expire}: autre dictionnaire (to_encore = dictionnaire déjà) qui contient une seule clé-valeur. La clé est "exp" (qui est une abréviation de "expire") et la valeur est la variable expire, qui contient le moment où le token doit expirer.
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM) # fonction provient de la bibliothèque python-jose, qui est utilisée pour créer des tokens JWT (JSON Web Tokens). Un token JWT est une chaîne de caractères encodée qui peut être utilisée pour authentifier et transmettre des informations entre différentes parties de manière sécurisée.
    # dictionnaire de données que l'on souhaite encoder dans le token JWT. Il contient toutes les informations que l'on souhaite inclure dans le token, comme l'identifiant de l'utilisateur, son rôle, et le moment d'expiration du token.
    return encoded_jwt

# Fonction pour obtenir le token actuel
def get_current_token(token: str = Depends(oauth2_scheme)): # Depends() est une dépendance. Dans FastAPI, dépendance = fonction qui est exécutée avant la fonction principale (ici, get_current_token)
    return token
# La fonction get_current_token elle-même est assez simple. Elle prend le token (qui est le résultat de l'exécution de oauth2_scheme) et le retourne simplement.
# Le type de token est spécifié comme str, ce qui signifie que cette fonction s'attend à recevoir une chaîne de caractères en tant que token.

def get_current_user(token: str = Depends(get_current_token)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Idenfiants incorrects",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try: # Ce bloc try-except est utilisé pour décoder le token JWT et extraire les informations de l'utilisateur. Si le token est invalide ou a expiré, une exception JWTError sera levée, et l'exception credentials_exception sera levée à la place.
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]) # Cette ligne décode le token JWT en utilisant la clé secrète et l'algorithme spécifié. Si le token est valide, payload contiendra un dictionnaire avec les informations de l'utilisateur.
        print(f"Role du token : {payload.get('role')}")

        email: str = payload.get("sub")
        role: str = payload.get("role") 
        if email is None or role is None:  
            raise credentials_exception
        token_data = TokenData(email=email, role=role) # Cette ligne crée une instance de TokenData (un modèle Pydantic) avec l'adresse e-mail et le rôle de l'utilisateur.
    except JWTError:
        raise credentials_exception
    user = get_user(email=token_data.email) # Cette ligne appelle la fonction get_user pour récupérer les informations de l'utilisateur à partir de la base de données en utilisant l'adresse e-mail extraite du token JWT.
    if user is None:
        raise credentials_exception
    return user

# Permet de vérifier le rôle de l'utilisateur

def get_current_role(user: dict = Depends(get_current_user)):
    return user.get("role")
