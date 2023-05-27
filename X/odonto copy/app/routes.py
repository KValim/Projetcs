from flask import Flask, render_template, request, redirect, url_for


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/client')
def client():
    return render_template('client.html')
