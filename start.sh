#!/bin/bash

gunicorn welcome_home.wsgi:application
