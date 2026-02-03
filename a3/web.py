from flask import Flask, request, render_template_string
import pandas as pd
import numpy as np
import re
import smtplib
from email.message import EmailMessage

app=Flask(__name__)

def is_valid_email(email):
    pattern=r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email)
#Topsis
def topsis(data, weights, impacts):
    x=data.iloc[:,1:].astype(float)

    norm=x/np.sqrt((x** 2).sum())
    weighted=norm * weights

    best, worst =[], []
    for i in range(len(impacts)):
        if impacts[i] == '+':
            best.append(weighted.iloc[:, i].max())
            worst.append(weighted.iloc[:, i].min())
        else:
            best.append(weighted.iloc[:, i].min())
            worst.append(weighted.iloc[:, i].max())

    best=np.array(best)
    worst=np.array(worst)

    dis_best=np.sqrt(((weighted-best) ** 2).sum(axis=1))
    dis_worst=np.sqrt(((weighted-worst) ** 2).sum(axis=1))

    score=dis_worst/(dis_best + dis_worst)
    data["Topsis Score"]=score
    data["Rank"]=score.rank(ascending=False)

    return data

def send_email(receiver_email,file_path):
    sender_email="vedika.kapur@gmail.com"         
    app_password="aenzikewswohmopo"             

    msg=EmailMessage()
    msg["Subject"]="TOPSIS Result File"
    msg["From"]=sender_email
    msg["To"]=receiver_email
    msg.set_content("TOPSIS result file.")

    with open(file_path,"rb") as f:
        msg.add_attachment(
            f.read(),
            maintype="application",
            subtype="octet-stream",
            filename="result.csv"
        )
    with smtplib.SMTP_SSL("smtp.gmail.com",465) as server:
        server.login(sender_email, app_password)
        server.send_message(msg)

HTML = """
<h2>TOPSIS Web Service</h2>
<form method="post" enctype="multipart/form-data">
CSV File: <input type="file" name="file" required><br><br>
Weights: <input name="weights" placeholder="1,1,1,1" required><br><br>
Impacts: <input name="impacts" placeholder="+,+,-,+" required><br><br>
Email ID: <input name="email" required><br><br>
<input type="submit">
</form>
<p style="color:red;">{{ error }}</p>
<p style="color:green;">{{ success }}</p>
"""

@app.route("/", methods=["GET","POST"])
def index():
    error=success=""
    if request.method=="POST":
        file=request.files["file"]
        weights=request.form["weights"]
        impacts=request.form["impacts"]
        email=request.form["email"]

        if not is_valid_email(email):
            error="Invalid email format"
            return render_template_string(HTML,error=error)

        try:
            weights=list(map(float,weights.split(",")))
        except:
            error="Weights must be numeric and comma separated"
            return render_template_string(HTML, error=error)

        impacts=impacts.split(",")

        if len(weights)!=len(impacts):
            error="Number of weights must equal impacts"
            return render_template_string(HTML, error=error)

        if not all(i in ['+','-'] for i in impacts):
            error="Impacts must be + or - only"
            return render_template_string(HTML, error=error)

        data=pd.read_csv(file)
        result=topsis(data,weights,impacts)

        output_file="result.csv"
        result.to_csv(output_file,index=False)

        send_email(email, output_file)
        success=f"Result successfully sent to {email}"

    return render_template_string(HTML, error=error, success=success)

if __name__ =="__main__":
    app.run(debug=True)
