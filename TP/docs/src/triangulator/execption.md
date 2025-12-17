Module src.triangulator.execption
=================================

Classes
-------

`InsufficientPointsError(*args, **kwargs)`
:   Levée si la triangulation est demandée avec moins de 3 points.

    ### Ancestors (in MRO)

    * src.triangulator.execption.TriangulatorError
    * builtins.ValueError
    * builtins.Exception
    * builtins.BaseException

`InvalidBinaryFormat(*args, **kwargs)`
:   Levée si les données binaires PointSet ou Triangles
    sont mal formées ou incomplètes.

    ### Ancestors (in MRO)

    * src.triangulator.execption.TriangulatorError
    * builtins.ValueError
    * builtins.Exception
    * builtins.BaseException

`PointSetManagerUnavailable(*args, **kwargs)`
:   Levée en cas d'erreur réseau ou si le PointSetManager retourne 503/5xx.

    ### Ancestors (in MRO)

    * src.triangulator.execption.TriangulatorError
    * builtins.Exception
    * builtins.BaseException

`PointSetNotFound(*args, **kwargs)`
:   Levée lorsque le PointSetManager retourne une erreur 404 (ID non trouvé).

    ### Ancestors (in MRO)

    * src.triangulator.execption.TriangulatorError
    * builtins.Exception
    * builtins.BaseException

`TriangulatorError(*args, **kwargs)`
:   Classe de base pour toutes les
    exceptions du Triangulator.

    ### Ancestors (in MRO)

    * builtins.Exception
    * builtins.BaseException

    ### Descendants

    * src.triangulator.execption.InsufficientPointsError
    * src.triangulator.execption.InvalidBinaryFormat
    * src.triangulator.execption.PointSetManagerUnavailable
    * src.triangulator.execption.PointSetNotFound