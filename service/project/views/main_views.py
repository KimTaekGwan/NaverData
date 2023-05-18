# myproject/sesac/views/post_views.py
from flask import Flask, url_for, request, session, redirect, app, jsonify
from flask import Blueprint, render_template, jsonify

# from project.db import db
from project.module import *

import os
import json
from tqdm import tqdm


bp = Blueprint('main_views', __name__, url_prefix='/')


@bp.route('/')  
def main():  
    return render_template("pages/main.html")  