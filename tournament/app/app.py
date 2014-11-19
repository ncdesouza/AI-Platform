

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/cram', methods=['GET', 'POST'])
def cram():
    if request.method == 'POST':
        CramServer.ClientChannel
