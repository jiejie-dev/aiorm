class AiormError(Exception):
    pass


class AiormQueryCompilerError(AiormError):
    pass


class AiormDbError(AiormError):
    pass


class TableError(AiormDbError):
    pass


class CreateTableError(TableError):
    pass


class DropTableError(TableError):
    pass
