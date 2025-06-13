from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

AUTH_KEY = "CekaAuth999"

@app.route("/api/sorgu", methods=["GET", "POST", "OPTIONS"])
def sorgu():
    # Auth kontrol
    auth = request.args.get("auth")
    if auth != AUTH_KEY:
        return jsonify({"error": "Yetkisiz erişim. auth parametresi eksik ya da geçersiz."}), 401

    # Parametreleri al
    sec = request.args.get("sec")
    tc = request.args.get("tc")
    ad = request.args.get("ad")
    soyad = request.args.get("soyad")
    il = request.args.get("il")
    ilce = request.args.get("ilce")

    base_url = "http://api.ondex.uk/ondexapi/"

    endpoints = {
        "1": f"tcsorgu.php?tc={tc}",
        "2": f"tcprosorgu.php?tc={tc}",
        "3": f"adressorgu.php?tc={tc}",
        "4": f"hanesorgu.php?tc={tc}",
        "5": f"adsoyadsorgu.php?ad={ad}&soyad={soyad}&il={il}&ilce={ilce}",
        "6": f"ailesorgu.php?tc={tc}",
        "7": f"hayathikayesisorgu.php?tc={tc}",
        "8": f"sulalesorgu.php?tc={tc}",
        "9": f"isyerisorgu.php?tc={tc}",
        "10": f"isyeriarkadasisorgu.php?tc={tc}"
    }

    if sec not in endpoints:
        return jsonify({"error": "Geçersiz sec parametresi"}), 400

    try:
        full_url = base_url + endpoints[sec]
        response = requests.get(full_url)
        data = response.json()

        # İstenmeyen alanları sil
        for unwanted_key in ["telegram", "author", "api_ismi"]:
            data.pop(unwanted_key, None)

        return jsonify(data)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)
