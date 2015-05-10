from flask import Flask
import config

app = Flask(__name__)

if __name__ == '__main__':
    app.run(debug=True)


@app.before_request
def before_request():
    # handle something before request
    # like open database connection
    # check ip
    pass


@app.after_request
def after_request(r):
    # handle something after request
    # like close database connection
    return r

# config logging
if not app.debug:
    import logging
    from logging.handlers import RotatingFileHandler
    handler = RotatingFileHandler(
        config.PYTHON_LOG_FILEPATH,
        maxBytes=config.PYTHON_LOG_MAX_BYTES,
        backupCount=config.PYTHON_LOG_BACKUP_COUNT
    )
    formatter = logging.Formatter(config.PYTHON_LOG_FORMAT)
    handler.setFormatter(formatter)
    handler.setLevel(logging.ERROR)
    app.logger.setLevel(logging.ERROR)
    app.logger.addHandler(handler)
