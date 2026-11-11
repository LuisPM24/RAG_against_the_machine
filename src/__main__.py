from classes import Parser, Indexer
import sys


def mi_decorador(func):
    def wrapper(*args, **kwargs):
        print("Antes de ejecutar la función")
        resultado = func(*args, **kwargs)
        print("Después de ejecutar la función")
        return resultado
    return wrapper


@mi_decorador
def saludar(nombre: str) -> str:
    """Devuelve un saludo personalizado."""
    mensaje = f"Hola, {nombre}!"
    return mensaje


def main() -> None:
    """Main function. Runs the application"""
    try:
        parser = Parser.get_args()
        indexer = Indexer(
            max_chunk_size=parser.max_chunk_size,
            indexing_method=parser.indexing_method
        )
        indexer.chunking()
    except Exception as e:
        print(f"Error - {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
