import tempfile

from funix import funix
from funix.hint import Markdown, BytesFile
from funix.session import set_default_global_variable

from vectara import vectara, post_process_query_result

vectara_client: vectara | None = None

def __get_vectara_client() -> vectara:
    if vectara_client is None:
        raise Exception("Vectara client not set. Please run set_api first.")
    return vectara_client


@funix()
def set_api(
    customer_id: str,
    client_id: str,
    client_secret: str,
):
    global vectara_client
    vectara_client = vectara(customer_id, client_id, client_secret, from_cli=False)


@funix()
def create_corpus(
    corpus_name: str,
    corpus_description: str = ""
) -> str:
    api = __get_vectara_client()
    corpus_id = api.create_corpus(corpus_name, corpus_description)
    if corpus_id is None:
        return "Corpus creation failed."
    return f"New corpus created, corpus ID is: {corpus_id}"


@funix()
def reset_corpus(
    corpus_id: int,
) -> str:
    api = __get_vectara_client()
    if api.reset_corpus(corpus_id):
        return f"Resetting corpus {corpus_id} successful."
    else:
        return f"Failed resetting corpus {corpus_id}."


@funix()
def query(
    corpus_id: int,
    query: str,
    top_k: int = 5,
    lang: str = 'auto'
) -> Markdown:
    api = __get_vectara_client()
    resp: dict = api.query(corpus_id, query, top_k, lang)
    if resp == {}:
        return "Vectara server error"
    else:
        return post_process_query_result(resp)


@funix()
def upload_file(
    corpus_id: int,
    file: BytesFile,
    description: str = "",
) -> str:
    api = __get_vectara_client()
    with tempfile.NamedTemporaryFile('wb') as temp:
        temp.write(file)
        if api.upload_file(corpus_id, temp.name, description):
            return "Upload successfully!"
        else:
            return "Upload failed!"
