from flask import Flask, render_template, request
import pandas as pd
import os

app = Flask(__name__)

def load_data():
    filepath = os.path.join('data', 'sample_data.csv')
    return pd.read_csv(filepath)

@app.route('/')
def index():
    try:
        data = load_data()
        return render_template('index.html', data=data.head(5))
    except Exception as e:
        return f"<h3>Error: {str(e)}</h3>"

@app.route('/predict', methods=['POST'])
def predict():
    try:
        ph = float(request.form['ph'])
        n = float(request.form['n'])
        p = float(request.form['p'])
        k = float(request.form['k'])

        # Prediksi sederhana
        if ph < 5.5:
            hasil = 3.8
        elif ph < 6.0:
            hasil = 4.3
        else:
            hasil = 4.8

        # Rekomendasi
        rekomendasi = []
        if ph < 5.5:
            rekomendasi.append("Tambahkan dolomit")
        if n < 25:
            rekomendasi.append("Butuh MOL untuk nitrogen")
        if p < 15:
            rekomendasi.append("Pupuk fosfat atau kompos tinggi P")
        if k < 0.30:
            rekomendasi.append("Butuh pupuk kalium")

        status = "🔴 Kritis" if ph < 5.5 or n < 20 or p < 10 else "🟡 Sedang" if ph < 5.8 else "🟢 Sehat"

        return render_template('result.html',
                               ph=ph, n=n, p=p, k=k,
                               hasil=round(hasil, 2),
                               status=status,
                               rekomendasi=rekomendasi)
    except Exception as e:
        return f"<h3>Error: {str(e)}</h3><br><a href='/'>Kembali</a>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))