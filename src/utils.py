import functools

from flask import session, redirect, url_for


def login_required(func):
    @functools.wraps(func)
    def secure_function(*args, **kwargs):
        if "username" not in session:
            return redirect(url_for("auth.index"))
        return func(*args, **kwargs)

    return secure_function


def save_file(file, filename):
    file.save(filename)
    return filename
