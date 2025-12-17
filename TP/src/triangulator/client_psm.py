from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from .core import PSM_BASE_URL
from .execption import PointSetManagerUnavailable, PointSetNotFound


def get_pointset_bytes(pointset_id: str) -> bytes:
    """Récupère les données binaires PointSet auprès du PointSetManager."""
    url = f"{PSM_BASE_URL}/pointset/{pointset_id}"
    
    req = Request(url, method='GET')
    
    try:
        with urlopen(req, timeout=5) as response:
            if response.status != 200:
                 raise HTTPError(
                     url, response.status, 'PSM returned non-200 status', 
                     response.headers, response.fp
                    )

            return response.read()
            
    except HTTPError as e:
        if e.code == 404:
            raise PointSetNotFound("PointSet ID non trouvé sur le PSM.") from e
        
        raise PointSetManagerUnavailable(
            f"PSM a retourné l'erreur HTTP {e.code}."
        ) from e
        
    except URLError as e:
        raise PointSetManagerUnavailable(
            f"Connexion au PSM impossible: {e.reason}"
        ) from e
    
    except Exception as e:
        raise PointSetManagerUnavailable(
            f"Erreur inattendue lors de la communication avec le PSM: {e}"
        ) from e