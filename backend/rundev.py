#! usr/bin/env python3

from zvms import create_app

app = create_app()

if __name__ == '__main__':
    app.run(
        port=11452,
        host='0.0.0.0'
    )