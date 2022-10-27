import base64

import bcrypt


def short_urn(uri: str) -> str:
    return str(
        base64.b64encode(
            bcrypt.hashpw(
                bytes(uri, encoding='utf-8'), bcrypt.gensalt()
            )
        ),
        encoding='utf-8'
    )[-7:]
