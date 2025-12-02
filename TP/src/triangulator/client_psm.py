from urllib.request import urlopen, Request
from urllib.error import HTTPError, URLError
from .exceptions import PointSetNotFound, PointSetManagerUnavailable
from .core import PSM_BASE_URL 

def get_pointset_bytes(pointset_id: str) -> bytes:
    """Récupère les données binaires PointSet auprès du PointSetManager."""
    url = f"{PSM_BASE_URL}/pointset/{pointset_id}"
    
    try:
        with urlopen(url) as response:
            if response.status != 200:
                pass 
            return response.read()
            
    except HTTPError as e:
        if e.code == 404:
            raise PointSetNotFound(f"PointSet {pointset_id} non trouvé.") from e
        raise PointSetManagerUnavailable(f"PSM a retourné l'erreur HTTP {e.code}.") from e
        
    except URLError as e:
        raise PointSetManagerUnavailable(f"Connexion au PSM impossible: {e.reason}") from e

    raise NotImplementedError()