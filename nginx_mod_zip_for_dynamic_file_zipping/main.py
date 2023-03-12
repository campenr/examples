from fastapi import FastAPI
from fastapi.responses import PlainTextResponse


app = FastAPI()


@app.get('/zip/')
def zipfiles():
    return PlainTextResponse(
        content=build_content(),
        headers={
            'X-Archive-Files': 'zip',
            'Content-Disposition': 'attachment; filename=mod_zip_demo.zip',
        },
    )


def build_content():
    content = ''
    content += '098f1c6b 7 /test1.txt Test1.txt\r\n'
    content += '440a6aa5 12 /test2.txt Test2.txt\r\n'
    return content

