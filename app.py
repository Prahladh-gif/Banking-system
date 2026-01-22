from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

accounts = {}

@app.route("/")
def home():
    return "HOME ROUTE WORKING"

@app.route("/ui")
def ui():
    return render_template("index.html")

@app.route("/create_account", methods=["POST"])
def create_account():
    data = request.get_json()
    acc = data["account_number"]

    if acc in accounts:
        return jsonify({"message": "Account already exists"}), 400

    accounts[acc] = {
        "name": data["name"],
        "balance": data["balance"]
    }
    return jsonify({"message": "Account created"})

@app.route("/deposit", methods=["POST"])
def deposit():
    data = request.get_json()
    acc = data["account_number"]

    if acc not in accounts:
        return jsonify({"message": "Account not found"}), 404

    accounts[acc]["balance"] += data["amount"]
    return jsonify({"balance": accounts[acc]["balance"]})

@app.route("/withdraw", methods=["POST"])
def withdraw():
    data = request.get_json()
    acc = data["account_number"]

    if acc not in accounts:
        return jsonify({"message": "Account not found"}), 404

    if accounts[acc]["balance"] < data["amount"]:
        return jsonify({"message": "Insufficient balance"}), 400

    accounts[acc]["balance"] -= data["amount"]
    return jsonify({"balance": accounts[acc]["balance"]})

@app.route("/balance/<int:acc>")
def balance(acc):
    if acc not in accounts:
        return jsonify({"message": "Account not found"}), 404

    return jsonify(accounts[acc])

# ---------------- NEW CODE FOR 5 & 6 ----------------

@app.route("/accounts")
def view_all_accounts():
    return jsonify(accounts)

@app.route("/highest_balance")
def highest_balance_account():
    if not accounts:
        return jsonify({"message": "No accounts available"}), 404

    highest_acc = max(accounts, key=lambda x: accounts[x]["balance"])
    return jsonify({highest_acc: accounts[highest_acc]})

# ---------------------------------------------------

if __name__ == "__main__":
    app.run(debug=True)
