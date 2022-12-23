import sys

from zvms import app, db, migrate
import zvms.views
import zvms.tokenlib as tk

tk.init_app(app)

if __name__ == '__main__':
    port = 1145
    for i in sys.argv[1:]:
        try:
            port = int(i)
        except ValueError:
            pass
    app.run(host='0.0.0.0', port=port)